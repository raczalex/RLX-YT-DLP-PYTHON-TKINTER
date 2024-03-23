import sv_ttk
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from io import BytesIO
from threading import Thread
from view.View import View
from model.Model import Model
from urllib.parse import urlparse
import html
import requests
import subprocess
import queue
import os
import time

class Controller:
    def __init__(self, root, model:Model):
        self.root = root
        self.model = model
        self.view = View(self.root, self.model)
        self.sys_os = self.model.get_os()
        self.set_os_theme_style_name()
        self.apply_3rd_party_theme()
        self.bind_events()
        self.queue = queue.Queue()

    def bind_events(self):
        self.root.bind("<Configure>", self.update_info_window_position)
        self.root.protocol("WM_DELETE_WINDOW", self.on_root_window_close)
        self.view.info_window.protocol("WM_DELETE_WINDOW", self.on_info_window_close)
        self.view.download_bin_window.protocol('WM_DELETE_WINDOW',self.on_download_bin_window_close)
        self.view.required_video_url_entry.bind('<FocusIn>', lambda e: self.view.required_video_url_entry.delete('0', 'end'))
        self.view.required_download_path_browse_button.bind('<Button-1>', self.required_browse_button_clicked)
        self.view.required_download_format_combo.bind("<<ComboboxSelected>>", self.required_download_format_selected)
        self.view.optional_download_custom_args_entry.bind('<FocusIn>', lambda e: self.view.optional_download_custom_args_entry.delete('0', 'end'))
        self.view.controls_add_button.bind('<Button-1>', self.controls_add_button_clicked)
        self.view.controls_remove_button.bind('<Button-1>', self.controls_remove_button_clicked)
        self.view.controls_download_selected_button.bind('<Button-1>', self.controls_download_selected_button_clicked)
        self.view.controls_download_all_button.bind('<Button-1>', self.controls_download_all_button_clicked)
        self.view.optional_download_sponsorblock_combo.bind("<<ComboboxSelected>>", self.optional_download_sponsorblock_selected)
        self.view.include_metadata_checkBox.bind('<Button-1>', self.include_metadata_clicked)
        self.view.include_thumbnail_checkBox.bind('<Button-1>', self.include_thumbnail_clicked)
        self.view.include_subtitles_checkBox.bind('<Button-1>', self.include_subtitles_clicked)
        self.view.theme_checkBox.bind('<Button-1>', self.theme_checkbox_clicked)
        self.view.status_treeView.bind('<<TreeviewSelect>>', self.status_treeview_item_selected)

    def apply_3rd_party_theme(self):
        #if self.sys_os == 'Windows':
        sv_ttk.set_theme(self.model.get_theme_name(),self.root)
        #elif self.sys_os == 'Darwin':
            #self.root.tk.call('source','themes/azure.tcl')
            #self.root.tk.call('set_theme',self.model.get_theme_name())
        #    from themes.MacTheme import MacTheme
        #    MacTheme(self.root).set_theme(self.model.get_theme_name())
            #self.model.get_theme_name(),self.root)
        #elif self.sys_os == 'Linux':
        #    sv_ttk.set_theme(self.model.get_theme_name(),self.root)
        #else:
        #    sv_ttk.set_theme(self.model.get_theme_name(),self.root)

    def set_os_theme_style_name(self):
        theme_name_to_set = ''

        if self.sys_os == 'Windows':
            try:
                reg_query_command = ['reg', 'query', 'HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize', '/v', 'AppsUseLightTheme']
                result = subprocess.run(reg_query_command, capture_output=True, text=True, check=True)
                theme = result.stdout.split()[-1]  # Extracting the value from the output
                theme_name_to_set = "light" if theme == "0x1" else "dark" if theme == "0x0" else 'light'
                self.model.set_theme_name(theme_name_to_set)
            except Exception:
                theme_name_to_set = 'light'
                self.model.set_theme_name(theme_name_to_set)
            
        elif self.sys_os == 'Linux':
            try:
                result = subprocess.run(["gsettings", "get", "org.gnome.desktop.interface", "gtk-theme"], capture_output=True, text=True)
                theme = result.stdout.strip().replace("'", "").lower() if result.returncode == 0 else 'light'
                theme_name_to_set = "light" if 'light' in theme else "dark" if 'dark' in theme else 'light'
                self.model.set_theme_name(theme_name_to_set)
            except Exception:
                theme_name_to_set = 'light'
                self.model.set_theme_name(theme_name_to_set)

        elif self.sys_os == 'Darwin':
            try:
                result = subprocess.run(["defaults", "read", "-g", "AppleInterfaceStyle"], capture_output=True, text=True)
                theme = result.stdout.strip() if result.returncode == 0 else 'light'
                theme_name_to_set = "light" if theme == "Light" else "dark" if theme == "Dark" else 'light'
                self.model.set_theme_name(theme_name_to_set)
            except Exception:
                theme_name_to_set = 'light'
                self.model.set_theme_name(theme_name_to_set)
        else:
            theme_name_to_set = 'light'
            self.model.set_theme_name(theme_name_to_set)

        if theme_name_to_set.lower() == 'dark':
            self.view.theme_checkBox.state(['selected'])
            self.model.set_theme_checked(self.view.theme_checkBox.instate(['selected']))

    def update_gui(self):
        # Update the GUI with data from the queue
        while not self.queue.empty():
            update_type,data = self.queue.get()
            if update_type == 'process_output':
                line, item_to_edit = data
                self.process_video_download_output(line, item_to_edit)
            elif update_type == 'download_progress_bar':
                download_bin_progress_bar, download_bin_progress_label,download_bin_progress,download_bin_speed_label,download_bin_download_speed = data
                download_bin_progress_bar.set_progress(download_bin_progress)
                download_bin_progress_bar.update_idletasks()
                download_bin_progress_label.config(text=f'Progress: {download_bin_progress:.2f}%')
                download_bin_speed_label.config(text=f'Download Speed: {download_bin_download_speed:.2f} MB/s')
            elif update_type == 'download_bin_finished':
                if len(self.model.get_download_bin_missings()) == 0:
                    self.download_bin_finished_init_state()
                
        self.root.after(100, self.update_gui)

    def update_info_window_position(self, event=None):
        if self.view.info_window:
            x, y = self.view.root.winfo_x(), self.view.root.winfo_y()
            self.view.info_window.geometry("+{}+{}".format(x+5 + self.view.root.winfo_width(), y))

    def on_root_window_close(self):
        # Additional cleanup or actions before closing the window
        self.view.info_window.destroy()
        self.view.download_bin_window.destroy()
        self.root.destroy()  # Close the window

    def on_info_window_close(self):
        self.view.info_window.withdraw()

    def on_download_bin_window_close(self):
        self.view.download_bin_window.destroy()

    def resize_selected_video_thumbnail_canvas_image(self, event):
        # Resize the video_thumbnail_image to match the canvas dimensions
        self.video_thumbnail_resized = self.video_thumbnail_original.resize((event.width, event.height), Image.LANCZOS)
        self.video_thumbnail_photo = ImageTk.PhotoImage(self.video_thumbnail_resized)
        self.view.video_thumbnail_canvas.itemconfig(self.video_thumbnail_item, image=self.video_thumbnail_photo)

    def load_selected_video_thumbnail_canvas_image(self):
        # Load and resize the video_thumbnail_original_image
        self.video_thumbnail_original = Image.open(BytesIO(self.model.get_selected_video_thumbnail_image()))
        self.video_thumbnail_resized = self.video_thumbnail_original.resize((650, 500), Image.LANCZOS)
        self.video_thumbnail_photo = ImageTk.PhotoImage(self.video_thumbnail_resized)

        # Create a video_thumbnail_image item on the video_thumbnail_canvas and make it fill the canvas
        self.video_thumbnail_item = self.view.video_thumbnail_canvas.create_image(0, 0, anchor='nw', image=self.video_thumbnail_photo)
        self.view.video_title_label.config(text=self.model.get_selected_video_title())

        self.view.video_thumbnail_canvas.bind('<Configure>', self.resize_selected_video_thumbnail_canvas_image)

    def required_browse_button_clicked(self, event):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.model.set_required_download_path(folder_path)
            self.view.required_download_path_entry.delete('0', 'end')
            self.view.required_download_path_entry.insert(0, folder_path)

    def required_download_format_selected(self, event):
        self.model.set_required_download_format(self.view.required_download_format_combo.get())

    def optional_download_sponsorblock_selected(self, event):
        self.model.set_optional_download_sponsorblock(self.view.optional_download_sponsorblock_combo.get())

    def include_metadata_clicked(self, event):
        self.model.set_include_metadata_checked(self.view.include_metadata_checkBox.instate(['!selected']))

    def include_thumbnail_clicked(self, event):
        self.model.set_include_thumbnail_checked(self.view.include_thumbnail_checkBox.instate(['!selected']))

    def include_subtitles_clicked(self, event):
        self.model.set_include_subtitles_checked(self.view.include_subtitles_checkBox.instate(['!selected']))

    def theme_checkbox_clicked(self, event):
        theme = "light" if self.view.theme_checkBox.instate(['selected']) else "dark"
        self.model.set_theme_name(theme)
        self.model.set_theme_checked(self.view.theme_checkBox.instate(['selected']))
        self.apply_3rd_party_theme()

    def req_get_video_title(self,url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                video_title = self.find_string_between(response.text,'<title>','</title>').replace('- YouTube','').upper()

                return html.unescape(video_title)
            else:
                return 'NOT FOUND'
        except Exception as e:
            return 'ERROR LOADING TITLE'

    def controls_add_button_clicked(self,event):
        self.model.set_optional_download_filename(self.view.optional_download_filename_entry.get())
        self.model.set_optional_download_custom_args(self.view.optional_download_custom_args_entry.get())
        video_url = self.view.required_video_url_entry.get()
        if self.model.check_required_video_url(video_url):
            if self.model.check_required_video_duplicate(video_url):
                self.model.check_set_video_type(video_url,False)
                self.model.set_required_video_title(self.req_get_video_title(self.model.get_required_video_url()))
                self.model.set_required_video_url(video_url)
                self.model.add_added_video_url(video_url)
                self.view.status_treeView.insert('', tk.END, values=(
                        self.model.get_required_video_title(), self.model.get_required_video_url(),
                        self.model.get_required_video_type(), self.model.get_required_download_format(),
                        self.model.get_required_video_size(), self.model.get_required_video_progress(),
                        self.model.get_required_video_status(), self.model.get_required_video_speed(),
                        self.model.get_required_video_eta())
                    )

    def count_treeview_items(self):
        return len(self.view.status_treeView.get_children())

    def controls_remove_button_clicked(self, event):
        status_treeview_items_count = self.count_treeview_items()
        selection = self.view.status_treeView.selection()
        if selection:
            self.model.remove_added_video_url(self.model.get_selected_video_url())
            self.view.status_treeView.delete(selection[0])
            self.model.set_selected_video_title('N/A')
            self.model.set_selected_video_url('N/A')
            self.model.set_selected_video_type('N/A')
            self.model.set_selected_video_format('N/A')
            self.model.set_selected_video_size('N/A')
            self.model.set_selected_video_progress('N/A')
            self.model.set_selected_video_status('N/A')
            self.model.set_selected_video_speed('N/A')
            self.model.set_selected_video_eta('N/A')

            if status_treeview_items_count == 1:
                self.model.set_required_video_title('N/A')
                self.model.set_required_video_url('N/A')
                self.model.set_required_video_type('N/A')
                self.model.set_required_download_format('N/A')
                self.model.set_required_video_size('N/A')
                self.model.set_required_video_progress('N/A')
                self.model.set_required_video_status('N/A')
                self.model.set_required_video_speed('N/A')
                self.model.set_required_video_eta('N/A')

    def update_status_treeview_item(self,item, column_name, new_value):
        column_index = self.view.status_cols.index(column_name)
        values = list(self.view.status_treeView.item(item, "values"))
        values[column_index] = new_value
        self.view.status_treeView.item(item, values=values)

    def process_output(self,build_command,item_to_edit):
        currOs = self.model.get_os()

        if currOs == "Windows":
            creationflag = subprocess.CREATE_NO_WINDOW
        else:
            creationflag = None

        with subprocess.Popen(build_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,creationflags=creationflag,text=True, universal_newlines=True) as p:
            for line in p.stdout:
                self.queue.put(('process_output',(line, item_to_edit)))  # Put output line and item in the queue

    def execute_video_download_output_command(self, build_command, item_to_edit):
        Thread(target=self.process_output,args=(build_command,item_to_edit),daemon=True).start()

    def process_video_download_output(self, line_to_process:str, selected_item):
        line_to_process_lower = line_to_process.lower()
        if line_to_process_lower.startswith('{'):
            self.update_status_treeview_item(selected_item,'Status','Processing')
        elif line_to_process_lower.startswith('downloading'):
            download_data = line_to_process_lower.split()
            #est size updating returns invalid value for example the first estimated size
            #79.81 mib the last is 2.91 mib idk why
            self.update_status_treeview_item(selected_item,'Est Size',download_data[1])
            self.update_status_treeview_item(selected_item,'Progress',download_data[2])
            self.update_status_treeview_item(selected_item,'Speed',download_data[3])
            self.update_status_treeview_item(selected_item,'ETA',download_data[4])
            self.update_status_treeview_item(selected_item,'Status','Downloading')
        elif line_to_process_lower.startswith('error'):
            self.model.set_download_error(True)
            self.update_status_treeview_item(selected_item,'Est Size','ERROR')
            self.update_status_treeview_item(selected_item,'Status','ERROR')
            self.update_status_treeview_item(selected_item,'Speed','ERROR')
        elif '"[Merger]", "[ExtractAudio]"' in line_to_process_lower:
            self.update_status_treeview_item(selected_item,'Status','Converting')

        if line_to_process_lower.startswith('finished'):
            self.update_status_treeview_item(selected_item,'Status','Done')
        
        if 'has already been downloaded' in line_to_process_lower:
            self.update_status_treeview_item(selected_item,'Status','Done')

    def controls_download_selected_button_clicked(self,event):
        selected = self.view.status_treeView.selection()
        if selected:
            build_command = self.model.init_build_command(self.model.get_selected_video_url())
            selected_item = selected[0]
            self.execute_video_download_output_command(build_command,selected_item)

    def controls_download_all_button_clicked(self,event):
        video_urls = self.model.get_added_video_urls()
        for i,video_url in enumerate(video_urls):
            build_command = self.model.init_build_command(video_url)
            item_to_edit = self.view.status_treeView.get_children()[i]
            self.execute_video_download_output_command(build_command,item_to_edit)

    def status_treeview_item_selected(self,event):
        selection = self.view.status_treeView.selection()
        if selection:
            selected_item_id = selection[0]
            selected_video_title = self.view.status_treeView.item(selected_item_id, 'values')[0]
            self.model.set_selected_video_title(selected_video_title)

            selected_video_url = self.view.status_treeView.item(selected_item_id, 'values')[1]
            self.model.set_selected_video_url(selected_video_url)

            selected_video_type = self.view.status_treeView.item(selected_item_id, 'values')[2]
            self.model.set_selected_video_type(selected_video_type)

            selected_video_format = self.view.status_treeView.item(selected_item_id, 'values')[3]
            self.model.set_selected_video_format(selected_video_format)

            selected_video_size = self.view.status_treeView.item(selected_item_id, 'values')[4]
            self.model.set_selected_video_size(selected_video_size)

            selected_video_progress = self.view.status_treeView.item(selected_item_id, 'values')[5]
            self.model.set_selected_video_progress(selected_video_progress)

            selected_video_status = self.view.status_treeView.item(selected_item_id, 'values')[6]
            self.model.set_selected_video_status(selected_video_status)

            selected_video_speed = self.view.status_treeView.item(selected_item_id, 'values')[7]
            self.model.set_selected_video_speed(selected_video_speed)

            selected_video_eta = self.view.status_treeView.item(selected_item_id, 'values')[8]
            self.model.set_selected_video_eta(selected_video_eta)

            selected_video_thumbnail_url = self.req_get_youtube_thumbnail_url(selected_video_url,selected_video_type)
            self.model.set_selected_video_thumbnail_url(selected_video_thumbnail_url)
            self.model.set_selected_video_thumbnail_image(self.req_get_youtube_thumbnail_image(selected_video_thumbnail_url))
            self.view.info_window.deiconify()
            self.view.create_info_window_widgets()
            self.load_selected_video_thumbnail_canvas_image()

    def req_get_youtube_thumbnail_url(self,selected_video_url,selected_video_type):
        selected_video_thumbnail_url = 'https://brighammscenter.org/media/14872/placeholder-dark.jpg?mode=crop&width=1200&height=630'
        if selected_video_type == 'YouTube':
            video_id = selected_video_url.split('=')[1].split('&')[0]
            selected_video_thumbnail_url = f'https://img.youtube.com/vi/{video_id}/maxresdefault.jpg'
            return selected_video_thumbnail_url
        elif selected_video_type == 'Playlist':
            try:
                response = requests.get(selected_video_url)
                if response.status_code == 200:
                    html_content = response.text
                    if 'maxresdefault.jpg' in html_content:
                        id = self.find_string_between(html_content, '<meta property="og:image:height" content="640"><meta property="og:image" content="https://i9.ytimg.com/s_p/', '/maxresdefault.jpg?sqp=')
                        sqp = self.find_string_between(html_content, '"url":"https://i9.ytimg.com/s_p/{0}/maxresdefault.jpg?sqp='.format(id), 'maxRatio":').replace('\\u0026', '&')
                        real_sqp = sqp.split('&')[0]
                        rs = self.find_string_between(sqp, '&rs=', '&v')
                        v = self.find_string_between(sqp, '&v=', '"')
                        selected_video_thumbnail_url = f'https://i9.ytimg.com/s_p/{id}/maxresdefault.jpg?sqp={real_sqp}&rs={rs}&v={v}'
                        return selected_video_thumbnail_url
                    elif 'hqdefault.jpg' in html_content:
                        id = self.find_string_between(html_content, '"url":"https://i.ytimg.com/vi/', '/hqdefault.jpg?sqp=')
                        sqp = self.find_string_between(html_content, '"url":"https://i.ytimg.com/vi/{0}/hqdefault.jpg?sqp='.format(id), 'maxRatio":').replace('\\u0026', '&')
                        real_sqp = sqp.split('&')[0]
                        rs = self.find_string_between(sqp, '&rs=', '&v')
                        v = self.find_string_between(sqp, '&v=', '"')
                        selected_video_thumbnail_url = f'https://i.ytimg.com/vi/{id}/hqdefault.jpg?sqp={real_sqp}&rs={rs}&v={v}'
                        return selected_video_thumbnail_url
                else:
                    return selected_video_thumbnail_url
            except Exception as e:
                return selected_video_thumbnail_url
        else:
            return selected_video_thumbnail_url
        
    def req_get_youtube_thumbnail_image(self,selected_video_thumbnail_url):
        try:
            response = requests.get(selected_video_thumbnail_url)
            selected_video_thumbnail_image = response.content
            return selected_video_thumbnail_image
        except Exception as e:
            return None

    def req_download_bin(self,download_bin_url,download_bin_filename,download_bin_progress_bar,download_bin_progress_label,download_bin_speed_label):
        if not download_bin_filename:
            parsed_url = urlparse(download_bin_url)
            self.model.set_download_bin_filename_basename(os.path.basename(parsed_url.path))

        response = requests.get(download_bin_url, stream=True)
        if response.status_code == 200:
            total_size = int(response.headers.get('content-length', 0))
            chunk_size = 1024 * 1024  # 1 MB chunk size
            download_bin_downloaded = 0
            start_time = time.time()
            with open(download_bin_filename, 'wb') as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    download_bin_downloaded += len(data)
                    
                    # Calculate progress percentage
                    download_bin_progress = (download_bin_downloaded / total_size) * 100 if total_size > 0 else 0
                    download_bin_elapsed_time = time.time() - start_time
                    download_bin_download_speed = download_bin_downloaded / (1024 * 1024 * download_bin_elapsed_time)  # in MB/s

                    self.queue.put(('download_progress_bar',(download_bin_progress_bar, download_bin_progress_label,download_bin_progress,download_bin_speed_label,download_bin_download_speed)))  # Put progress into the queue   
            
            if download_bin_downloaded >= total_size:
                self.queue.put(("download_bin_finished", None))
                self.model.add_download_bin_execute_permission(download_bin_filename)
                self.model.remove_download_bin_missing([download_bin_url,download_bin_filename])
            else:
                os.remove(download_bin_filename)

    def download_bin_finished_init_state(self):
        if self.model.check_download_bin_missings() == True:
            if self.model.check_download_bin_downloaded_files_exist() == False:
                self.view.download_bin_window.deiconify()
                self.root.withdraw()
        else:
            self.view.download_bin_window.withdraw()
            self.root.deiconify()

    def download_bin_start(self):
        self.download_bin_finished_init_state()
        download_bin_missing_files = self.model.get_download_bin_missings()
        col_index = 0
        for download_bin_url, download_bin_filename in download_bin_missing_files:
            download_bin_progress_bar, download_bin_progress_label, download_bin_speed_label = self.view.create_download_bin_window_widgets(col_index,download_bin_filename.split("/")[-1] if "/" in download_bin_filename else download_bin_filename.split("\\")[-1])
            col_index += 1
            download_thread = Thread(target=self.req_download_bin, args=(download_bin_url, download_bin_filename, download_bin_progress_bar, download_bin_progress_label, download_bin_speed_label),daemon=True)
            download_thread.start()

    @staticmethod
    def find_string_between(string, start, end):
        try:
            start_index = string.index(start)
            if start_index >= 0:
                start_index += len(start)
                end_index = string.index(end, start_index)
                return string[start_index:end_index]
        except ValueError:
            return None