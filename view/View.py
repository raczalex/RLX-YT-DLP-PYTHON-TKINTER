import tkinter as tk
from tkinter import ttk
from model.Model import Model
from CustomControls.CustomProgressBar import CustomProgressBar

class View():
    def __init__(self,root,model:Model):
        self.root = root
        self.model = model
        self.root = self.create_root_window()
        self.download_bin_window = self.create_download_bin_window()
        self.info_window = self.create_info_window()

    def create_root_window(self):
        self.root.title(self.model.get_root_window_title())
        self.root.resizable(False,False)
        self.root.iconbitmap('RLX.ico')
        self.create_root_window_widgets()
        return self.root
    
    def create_info_window(self):
        self.info_window = tk.Toplevel(self.root)
        self.info_window.title(self.model.get_info_window_title())
        self.info_window.geometry('650x500')
        self.info_window.withdraw()
        self.info_window.resizable(False,False)
        self.info_window.iconbitmap('RLX.ico')
        self.info_window.columnconfigure(0, weight=1)
        self.info_window.rowconfigure(0, weight=1)
        return self.info_window
    
    def create_download_bin_window(self):
        self.download_bin_window = tk.Toplevel(self.root)
        self.download_bin_window.resizable(False,False)
        self.download_bin_window.iconbitmap('RLX.ico')
        self.download_bin_window.title(self.model.get_download_bin_window_title())
        return self.download_bin_window

    def create_download_bin_window_widgets(self,col_index,title_text):
        frame = tk.Frame(self.download_bin_window)
        frame.grid(row=0,column=col_index,padx=10,pady=10,sticky='nsew')
        frame.columnconfigure(0,weight=1)
        frame.rowconfigure(0,weight=1)
        title_label = tk.Label(frame, text=title_text, font=self.model.get_custom_font(),anchor='center')
        title_label.grid(row=0, column=0, sticky='nsew', pady=(0, 5))

        progress_bar = CustomProgressBar(frame,width=200,height=20,progress=0.0)
        progress_bar.grid(row=1, column=0, sticky='nsew', pady=(0, 5))

        progress_label = tk.Label(frame, text="Progress: 00.00%", anchor="center")
        progress_label.grid(row=2, column=0, sticky='nsew', pady=(0, 5))

        speed_label = tk.Label(frame, text="Download Speed: 00.00 MB/s", anchor="center")
        speed_label.grid(row=3, column=0, sticky='nsew', pady=(0, 5))

        return [progress_bar,progress_label,speed_label]
    
    def create_info_window_widgets(self):
        self.clear_widgets(self.info_window)

        self.video_thumbnail_canvas = tk.Canvas(self.info_window, background='black', bd=0, highlightthickness=0, relief='ridge')
        self.video_thumbnail_canvas.grid(row=0, column=0, sticky='nsew')
        
        self.video_title_label = tk.Label(self.info_window, text='TITLE', wraplength=450, font=self.model.get_custom_font())
        self.video_title_label.grid(row=1, column=0, sticky='ew')
        
    def clear_widgets(self,handle_window):
        for widget in handle_window.winfo_children():
            widget.pack_forget()
            widget.destroy()

    def create_root_window_widgets(self):
        # Main Frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.required_frame = ttk.Labelframe(self.main_frame, text='Required')
        self.required_frame.grid(row=0, column=0, padx=5, pady=5)

        self.required_video_url_label = ttk.Label(self.required_frame, text='URL:')
        self.required_video_url_label.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        self.required_video_url_entry = ttk.Entry(self.required_frame, width=30)
        self.required_video_url_entry.insert(0, self.model.get_required_video_url())
        self.required_video_url_entry.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

        self.required_download_path_label = ttk.Label(self.required_frame, text='PATH:')
        self.required_download_path_label.grid(row=2, column=0, padx=5, pady=5, sticky='ew')

        self.required_download_path_entry = ttk.Entry(self.required_frame)
        self.required_download_path_entry.insert(0, self.model.get_required_download_path())
        self.required_download_path_entry.grid(row=3, column=0, padx=5, pady=5, sticky='ew')

        self.required_download_path_browse_button = ttk.Button(self.required_frame, text='BROWSE')
        self.required_download_path_browse_button.grid(row=4, column=0, padx=5, pady=5, sticky='ew')

        self.required_video_format_label = ttk.Label(self.required_frame, text='FORMAT')
        self.required_video_format_label.grid(row=5, column=0, padx=5, pady=5, sticky='ew')

        self.required_download_format_combo = ttk.Combobox(self.required_frame, values=self.model.get_required_download_format_values(), state='readonly')
        self.required_download_format_combo.current(1)
        self.required_download_format_combo.grid(row=6, column=0, padx=5, pady=5, sticky='ew')

        # Optional Frame
        self.optional_frame = ttk.Labelframe(self.main_frame, text='Optional')
        self.optional_frame.grid(row=0, column=1, padx=5, pady=5)

        self.optional_download_filename_label = ttk.Label(self.optional_frame, text='FILENAME:')
        self.optional_download_filename_label.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

        self.optional_download_filename_entry = ttk.Entry(self.optional_frame, width=30)
        self.optional_download_filename_entry.insert(0, self.model.get_optional_download_filename())
        
        self.optional_download_filename_entry.grid(row=2, column=0, padx=5, pady=5, sticky='ew')

        self.optional_download_custom_args_label = ttk.Label(self.optional_frame, text='CUSTOM ARGS:')
        self.optional_download_custom_args_label.grid(row=3, column=0, padx=5, pady=5, sticky='ew')

        self.optional_download_custom_args_entry = ttk.Entry(self.optional_frame)
        self.optional_download_custom_args_entry.insert(0, self.model.get_optional_download_custom_args())
        self.optional_download_custom_args_entry.grid(row=4, column=0, padx=5, pady=5, sticky='ew')

        self.optional_download_sponsorblock_label = ttk.Label(self.optional_frame, text='SponsorBlock')
        self.optional_download_sponsorblock_label.grid(row=5, column=0, padx=5, pady=5, sticky='ew')

        self.optional_download_sponsorblock_combo = ttk.Combobox(self.optional_frame, values=self.model.get_optional_download_sponsorblock_values(), state='readonly')
        self.optional_download_sponsorblock_combo.current(0)
        self.optional_download_sponsorblock_combo.grid(row=6, column=0, padx=5, pady=5, sticky='ew')

        # Controls Frame
        self.controls_frame = ttk.LabelFrame(self.main_frame, text='Controls')
        self.controls_frame.grid(row=0, column=2, padx=5, pady=5)

        self.controls_add_button = ttk.Button(self.controls_frame, text='ADD')
        self.controls_add_button.grid(row=1, column=2, padx=5, pady=5, sticky='nsew')

        self.controls_remove_button = ttk.Button(self.controls_frame, text='REMOVE')
        self.controls_remove_button.grid(row=2, column=2, padx=5, pady=5, sticky='nsew')

        self.controls_download_selected_button = ttk.Button(self.controls_frame, text='DOWNLOAD')
        self.controls_download_selected_button.grid(row=3, column=2, padx=5, pady=5, sticky='nsew')

        self.controls_download_all_button = ttk.Button(self.controls_frame, text='DOWNLOAD ALL')
        self.controls_download_all_button.grid(row=4, column=2, padx=5, pady=5, sticky='nsew')

        # Include Frame
        self.include_frame = ttk.Labelframe(self.main_frame, text='Include')
        self.include_frame.grid(row=0, column=3, padx=5, pady=5)
        
        self.include_metadata_checkBox = ttk.Checkbutton(self.include_frame, text='Metadata')
        self.include_metadata_checkBox.state(self.model.get_include_metadata_checked())
        self.include_metadata_checkBox.grid(row=1, column=3, padx=5, pady=5, sticky='ew')

        self.include_thumbnail_checkBox = ttk.Checkbutton(self.include_frame, text='Thumbnail')
        self.include_thumbnail_checkBox.state(self.model.get_include_thumbnail_checked())
        self.include_thumbnail_checkBox.grid(row=2, column=3, padx=5, pady=5, sticky='ew')

        self.include_subtitles_checkBox = ttk.Checkbutton(self.include_frame, text='Subtitles')
        self.include_subtitles_checkBox.state(self.model.get_include_subtitles_checked())
        self.include_subtitles_checkBox.grid(row=3, column=3, padx=5, pady=5, sticky='ew')

        # Theme Frame
        self.theme_frame = ttk.LabelFrame(self.main_frame, text='Theme')
        self.theme_frame.grid(row=0, column=4, padx=5, pady=5)

        self.theme_checkBox = ttk.Checkbutton(self.theme_frame, text='Dark')        
        self.theme_checkBox.state(self.model.get_theme_checked())
        self.theme_checkBox.grid(row=1, column=4, padx=5, pady=5, sticky='ew')

        # Status Frame
        self.status_frame = ttk.Frame(self.main_frame)
        self.status_frame.grid(row=1, column=0, columnspan=5, pady=10, sticky='ew')

        self.status_labelFrame = ttk.LabelFrame(self.status_frame, text='Status')
        self.status_labelFrame.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        self.status_frameScroll = ttk.Scrollbar(self.status_labelFrame)
        self.status_frameScroll.grid(row=0, column=2, sticky='nsew')

        self.status_cols = self.model.get_status_cols()

        self.status_treeView = ttk.Treeview(self.status_labelFrame, show='headings', columns=self.status_cols, height=13, yscrollcommand=self.status_frameScroll.set)
        self.status_treeView.heading('Title', text='Title')
        self.status_treeView.column('Title', width=200, anchor='center')
        
        for col in self.status_cols[1:]:
            self.status_treeView.heading(col, text=col)
            self.status_treeView.column(col, width=84, anchor='center')

        self.status_treeView.grid(row=0, column=1, sticky='ew')
        self.status_frameScroll.config(command=self.status_treeView.yview)