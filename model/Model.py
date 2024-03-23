import os
import platform
import shutil
import stat

class Model:
    def __init__(self):
        self.root_window_title = 'RLX - YT-DLP - DOWNLOAD'
        self.info_window_title = 'RLX - YT-DLP - INFO'
        self.download_bin_window_title = 'RLX - YT-DLP - BINARIES'
        self.required_video_prev_url = ''
        self.required_video_title = 'N/A'
        self.required_video_url = 'N/A'
        self.required_video_type = 'N/A'
        self.required_video_size = 'N/A'
        self.required_video_progress = 'N/A'
        self.required_video_status = 'N/A'
        self.required_video_speed = 'N/A'
        self.required_video_eta = 'N/A'
        self.required_video_thumbnail_url = ''
        self.required_video_thumbnail_image = None
        self.download_error = False
        self.required_download_path = self.init_required_download_path()
        self.optional_download_filename = r'%(title)s.%(ext)s'
        self.required_download_format = 'MP4'
        self.optional_download_custom_args = 'N/A'
        self.optional_download_sponsorblock = 'None'
        self.include_metadata_checked = ['!alternate']
        self.include_thumbnail_checked = ['!alternate']
        self.include_subtitles_checked = ['!alternate']
        self.theme_checked = ['!alternate']
        self.theme_name = ''
        self.selected_video_title = 'N/A'
        self.selected_video_url = 'N/A'
        self.selected_video_type = 'N/A'
        self.selected_video_format = 'N/A'
        self.selected_video_size = 'N/A'
        self.selected_video_progress = 'N/A'
        self.selected_video_status = 'N/A'
        self.selected_video_speed = 'N/A'
        self.selected_video_eta = 'N/A'
        self.selected_video_thumbnail_url = ''
        self.selected_video_thumbnail_image = b''
        self.bin_path = ''
        self.yt_dlp_full_path = ''
        self.video_types = ['YouTube','Playlist','Other']
        self.required_download_format_values = ['BEST', 'MP4', 'MP3', "M4A" ,'WAV', 'FLAC']
        self.optional_download_sponsorblock_values = ['None', 'Remove', 'Mark']
        self.status_cols = ('Title', 'Url', 'Type', 'Format', 'Est Size', 'Progress', 'Status', 'Speed', 'ETA')
        self.custom_font = ("Helvetica", 15,'bold')
        self.download_bin_url = ''
        self.download_bin_filename = ''
        self.download_bin_filename_basename = ''
        self.download_bin_missings = []
        self.download_bin_binaries = {
                                        "Linux": {"ffmpeg": "ffmpeg-linux64-v4.1", "ffprobe": "ffprobe-linux64-v4.1", "yt-dlp": "yt-dlp_linux"},
                                        "Darwin": {"ffmpeg": "ffmpeg-osx64-v4.1", "ffprobe": "ffprobe-osx64-v4.1", "yt-dlp": "yt-dlp_macos"},
                                        "Windows": {"ffmpeg": "ffmpeg-win64-v4.1.exe", "ffprobe": "ffprobe-win64-v4.1.exe", "yt-dlp": "yt-dlp.exe"}
                                    }
        self.download_bin_required_files = ['ffmpeg','ffprobe','yt-dlp']
        self.os = self.init_os()
        self.added_video_urls = []

    # Getters and setters for model attributes
    def get_root_window_title(self):
        return self.root_window_title
    
    def set_root_window_title(self,root_window_title):
        self.root_window_title = root_window_title

    def get_info_window_title(self):
        return self.info_window_title
    
    def set_info_window_title(self,info_window_title):
        self.info_window_title = info_window_title

    def get_download_bin_window_title(self):
        return self.download_bin_window_title
    
    def set_download_bin_window_title(self,download_bin_window_title):
        self.download_bin_window_title = download_bin_window_title

    def get_required_video_prev_url(self):
        return self.required_video_prev_url
    
    def set_required_video_prev_link(self,required_video_prev_url):
        self.required_video_prev_url = required_video_prev_url

    def get_required_video_title(self):
        return self.required_video_title
    
    def set_required_video_title(self,required_video_title):
        self.required_video_title = required_video_title

    def get_required_video_url(self):
        return self.required_video_url
    
    def set_required_video_url(self,get_required_video_url):
        self.required_video_url = get_required_video_url

    def get_required_video_type(self):
        return self.required_video_type
    
    def set_required_video_type(self,required_video_type):
        self.required_video_type = required_video_type
    
    def get_required_download_format(self):
        return self.required_download_format
    
    def set_required_download_format(self,required_download_format):
        self.required_download_format = required_download_format

    def get_required_video_size(self):
        return self.required_video_size
    
    def set_required_video_size(self,required_video_size):
        self.required_video_size = required_video_size

    def get_required_video_progress(self):
        return self.required_video_progress
    
    def set_required_video_progress(self,required_video_progress):
        self.required_video_progress = required_video_progress

    def get_required_video_status(self):
        return self.required_video_status
    
    def set_required_video_status(self,required_video_status):
        self.required_video_status = required_video_status

    def get_required_video_speed(self):
        return self.required_video_speed
    
    def set_required_video_speed(self,required_video_speed):
        self.required_video_speed = required_video_speed

    def get_required_video_eta(self):
        return self.required_video_eta
    
    def set_required_video_eta(self,required_video_eta):
        self.required_video_eta = required_video_eta

    def get_required_video_thumbnail_url(self):
        return self.required_video_thumbnail_url
    
    def set_required_video_thumbnail_url(self,required_video_thumbnail_url):
        self.required_video_thumbnail_url = required_video_thumbnail_url

    def get_required_video_thumbnail_image(self):
        return self.required_video_thumbnail_image
    
    def set_required_video_thumbnail_image(self,required_video_thumbnail_image):
        self.required_video_thumbnail_image = required_video_thumbnail_image

    def get_download_error(self):
        return self.download_error
    
    def set_download_error(self,download_error):
        self.download_error = download_error
    
    def get_required_download_path(self):
        return self.required_download_path
    
    def set_required_download_path(self,required_download_path):
        self.required_download_path = required_download_path

    def get_optional_download_filename(self):
        return self.optional_download_filename
    
    def set_optional_download_filename(self,optional_download_filename):
        self.optional_download_filename = optional_download_filename

    def get_optional_download_custom_args(self):
        return self.optional_download_custom_args
    
    def set_optional_download_custom_args(self,optional_download_custom_args):
        self.optional_download_custom_args = optional_download_custom_args

    def get_optional_download_sponsorblock(self):
        return self.optional_download_sponsorblock
    
    def set_optional_download_sponsorblock(self,optional_download_sponsorblock):
        self.optional_download_sponsorblock = optional_download_sponsorblock

    def get_include_metadata_checked(self):
        return self.include_metadata_checked
    
    def set_include_metadata_checked(self,include_metadata_checked):
        self.include_metadata_checked = include_metadata_checked

    def get_include_thumbnail_checked(self):
        return self.include_thumbnail_checked
    
    def set_include_thumbnail_checked(self,include_thumbnail_checked):
        self.include_thumbnail_checked = include_thumbnail_checked

    def get_include_subtitles_checked(self):
        return self.include_subtitles_checked
    
    def set_include_subtitles_checked(self,include_subtitles_checked):
        self.include_subtitles_checked = include_subtitles_checked

    def get_theme_checked(self):
        return self.theme_checked
    
    def set_theme_checked(self,theme_checked):
        self.theme_checked = theme_checked

    def get_theme_name(self):
        return self.theme_name
    
    def set_theme_name(self,theme_name):
        self.theme_name = theme_name

    def get_selected_video_title(self):
        return self.selected_video_title
    
    def set_selected_video_title(self,selected_video_title):
        self.selected_video_title = selected_video_title

    def get_selected_video_url(self):
        return self.selected_video_url
    
    def set_selected_video_url(self,selected_video_url):
        self.selected_video_url = selected_video_url

    def get_selected_video_type(self):
        return self.selected_video_type

    def set_selected_video_type(self,selected_video_type):
        self.selected_video_type = selected_video_type
    
    def get_selected_video_format(self):
        return self.selected_video_format
    
    def set_selected_video_format(self,selected_video_format):
        self.selected_video_format = selected_video_format

    def get_selected_video_size(self):
        return self.selected_video_size
    
    def set_selected_video_size(self,selected_video_size):
        self.selected_video_size = selected_video_size

    def get_selected_video_progress(self):
        return self.selected_video_progress
    
    def set_selected_video_progress(self,selected_video_progress):
        self.selected_video_progress = selected_video_progress

    def get_selected_video_status(self):
        return self.selected_video_status
    
    def set_selected_video_status(self,selected_video_status):
        self.selected_video_status = selected_video_status

    def get_selected_video_speed(self):
        return self.selected_video_speed
    
    def set_selected_video_speed(self,selected_video_speed):
        self.selected_video_speed = selected_video_speed

    def get_selected_video_eta(self):
        return self.selected_video_eta
    
    def set_selected_video_eta(self,selected_video_eta):
        self.selected_video_eta = selected_video_eta

    def get_selected_video_thumbnail_url(self):
        return self.selected_video_thumbnail_url
    
    def set_selected_video_thumbnail_url(self,selected_video_thumbnail_url):
        self.selected_video_thumbnail_url = selected_video_thumbnail_url

    def get_selected_video_thumbnail_image(self):
        return self.selected_video_thumbnail_image

    def set_selected_video_thumbnail_image(self,selected_video_thumbnail_image):
        self.selected_video_thumbnail_image = selected_video_thumbnail_image   

    def get_bin_path(self):
        return self.bin_path

    def set_bin_path(self,bin_path):
        self.bin_path = bin_path 

    def get_yt_dlp_full_path(self):
        return self.yt_dlp_full_path
    
    def set_yt_dlp_full_path(self,yt_dlp_full_path):
        self.yt_dlp_full_path = yt_dlp_full_path

    def get_added_video_urls(self):
        return self.added_video_urls
    
    def add_added_video_url(self,video_url):
        self.added_video_urls.append(video_url)
    
    def remove_added_video_url(self,video_url):
        self.added_video_urls.remove(video_url)
    
    def clear_added_video_urls(self):
        self.added_video_urls.clear()

    def get_download_bin_missings(self):
        return self.download_bin_missings
    
    def add_download_bin_missing(self,download_bin_missing):
        self.download_bin_missings.append(download_bin_missing)

    def remove_download_bin_missing(self,download_bin_missing):
        self.download_bin_missings.remove(download_bin_missing)

    def clear_download_bin_missings(self):
        self.download_bin_missings.clear()

    def get_required_download_format_values(self):
        return self.required_download_format_values
    
    def add_required_download_format_value(self,required_download_format_value):
        self.optional_download_sponsorblock_values.append(required_download_format_value)

    def remove_required_download_format_value(self,required_download_format_value):
        self.required_download_format_values.remove(required_download_format_value)

    def clear_required_download_format_values(self):
        self.added_video_urls.clear()

    def get_optional_download_sponsorblock_values(self):
        return self.optional_download_sponsorblock_values
    
    def add_optional_download_sponsorblock_value(self,optional_download_sponsorblock_value):
        self.optional_download_sponsorblock_values.append(optional_download_sponsorblock_value)

    def remove_optional_download_sponsorblock_value(self,optional_download_sponsorblock_values):
        self.optional_download_sponsorblock_values.remove(optional_download_sponsorblock_values)

    def clear_optional_download_sponsorblock_valuess(self):
        self.optional_download_sponsorblock_values.clear()

    def get_download_bin_required_files(self):
        return self.download_bin_required_files
    
    def add_download_bin_required_file(self,required_file):
        self.download_bin_required_files.append(required_file)

    def remove_download_bin_required_file(self,download_bin_required_file):
        self.download_bin_required_files.remove(download_bin_required_file)

    def clear_download_bin_required_files(self):
        self.download_bin_required_files.clear()

    def get_status_cols(self):
        return self.status_cols
    
    def add_status_col(self,status_col):
        self.status_cols = self.status_cols + (status_col,)

    def remove_status_col(self,status_col):
        self.status_cols = self.status_cols[:self.status_cols.index(status_col)] + self.status_cols[self.status_cols.index(status_col)+1:]

    def get_custom_font(self):
        return self.custom_font
    
    def get_download_bin_url(self):
        return self.download_bin_url
    
    def set_download_bin_url(self,download_bin_url):
        self.download_bin_url = download_bin_url

    def get_download_bin_filename(self):
        return self.download_bin_filename
    
    def set_download_bin_filename(self,download_bin_filename):
        self.download_bin_filename = download_bin_filename

    def get_download_bin_filename_basename(self):
        return self.download_bin_filename_basename
    
    def set_download_bin_filename_basename(self,download_bin_filename_basename):
        self.download_bin_filename_basename = download_bin_filename_basename

    def get_os(self):
        return self.os
    
    def set_os(self,os):
        self.os = os

    def init_os(self):
        return platform.system()

    def check_download_bin_missings(self):
        self.init_download_bin_missing_dep()
        if self.get_download_bin_missings():
            return True
        else:
            return False

    def check_required_video_url(self,url:str):
        if url.startswith(('https://','http://')):
            return True
        else:
            return False
        
    def check_required_video_duplicate(self,url:str):
        prev_url = self.get_required_video_prev_url()
        if url != prev_url:
            self.set_required_video_prev_link(url)
            self.set_required_video_url(url)
            return True
        else:
            return False

    def check_set_video_type(self,url:str,selected=False):
        if url.startswith('https://www.youtube.com/watch?v='):
            if selected:
                self.set_selected_video_type(self.video_types[0])
            else:
                self.set_required_video_type(self.video_types[0])
        elif url.startswith('https://www.youtube.com/playlist?list='):
            if selected:
                self.set_selected_video_type(self.video_types[1])
            else:
                self.set_required_video_type(self.video_types[1])
        else:
            if selected:
                self.set_selected_video_type(self.video_types[2])
            else:
                self.set_required_video_type(self.video_types[2])

    def check_required_video_format(self):
        required_video_format = self.get_required_download_format().lower()
        if required_video_format == 'best':
            return []
        if required_video_format == 'mp4':
            return ['-f', r'bv*[vcodec^=avc]+ba[ext=m4a]/b']
        elif required_video_format == "m4a":
            return ['-f', r'ba[ext=m4a]']
        else:
            return ['--extract-audio', '--audio-format', required_video_format, '--audio-quality', '0']
        
    def check_optional_download_custom_args(self):
        optional_download_custom_args = self.get_optional_download_custom_args().lower()

        if optional_download_custom_args != '' and optional_download_custom_args != 'n/a' and optional_download_custom_args != 'your custom arguments':
            return optional_download_custom_args.split()
        else:
            return None
        
    def check_include_metadata(self):
        if self.get_include_metadata_checked() == True:
            return ['--embed-metadata']
        else:
            return None
        
    def check_include_thumbnail(self):
        if self.get_include_thumbnail_checked() == True:
            return ['--embed-thumbnail']
        else:
            return None
        
    def check_include_subtitles(self):
        if self.get_include_subtitles_checked() == True:
            return ['--write-auto-subs']
        else:
            return None
        
    def check_optional_download_sponsorblock(self):
        optional_download_sponsorblock = self.get_optional_download_sponsorblock()
        if optional_download_sponsorblock == 'remove':
            return ['--sponsorblock-remove', 'all']
        elif optional_download_sponsorblock == 'mark':
            return ['--sponsorblock-mark', 'all']
        else:
            return None
        
    def init_required_download_path(self):
        return os.path.join(os.path.expanduser('~'), 'Downloads')

    def init_yt_dlp_name_path(self):
        exes = [exe for exe in self.get_download_bin_required_files() if shutil.which(exe)]
        if exes and exes[2] == 'yt-dlp':
            self.set_yt_dlp_full_path(exes[2])
        else:
            self.set_yt_dlp_full_path(str(self.get_bin_path() / ('yt-dlp.exe' if self.get_os() == "Windows" else 'yt-dlp')))

    def init_download_bin_missing_dep(self):
        exes = [exe for exe in self.get_download_bin_required_files() if not shutil.which(exe)]

        if exes:
            if not os.path.exists(self.get_bin_path()):
                os.makedirs(self.get_bin_path())
            
            for exe in exes:
                self.set_download_bin_filename(os.path.join(self.get_bin_path(),f'{exe}.exe' if self.get_os() == 'Windows' else exe))

                if not os.path.exists(self.get_download_bin_filename()):
                    if exe == 'yt-dlp':
                        self.set_download_bin_url(f'https://github.com/yt-dlp/yt-dlp/releases/latest/download/{self.download_bin_binaries[self.get_os()][exe]}')
                    else:
                        self.set_download_bin_url(f'https://github.com/imageio/imageio-binaries/raw/master/ffmpeg/{self.download_bin_binaries[self.get_os()][exe]}')
                    
                    self.add_download_bin_missing([self.get_download_bin_url(),self.get_download_bin_filename()])

    def add_download_bin_execute_permission(self,download_bin_filename):
        st = os.stat(download_bin_filename)
        os.chmod(download_bin_filename,st.st_mode | stat.S_IEXEC)

    def check_download_bin_downloaded_files_exist(self):
        download_bin_missings = self.get_download_bin_missings()
        if all(os.path.exists(download_req_filename) for _,download_req_filename in download_bin_missings):
            return True
        else:
            return False

    def init_build_command(self, video_url):
        self.init_yt_dlp_name_path()
        self.build_command =  [
            self.get_yt_dlp_full_path(), 
            video_url,
            '--hls-prefer-native',
            '--newline', 
            '--ignore-errors', 
            '--ignore-config', 
            '--no-simulate',
            '--progress',
            '--progress-template',
            '%(progress.status)s %(progress._total_bytes_str)s %(progress._percent_str)s %(progress._speed_str)s %(progress._eta_str)s',
            '--dump-json', 
            '-v',
            '-o',
            f'{self.get_required_download_path()}/{self.get_optional_download_filename()}'
        ]
        
        required_video_format = self.check_required_video_format()
        self.build_command += required_video_format

        optional_download_custom_args = self.check_optional_download_custom_args()

        if optional_download_custom_args is not None:
            self.build_command += optional_download_custom_args

        include_metadata = self.check_include_metadata()
        if include_metadata is not None:
            self.build_command += include_metadata
        
        include_thumbnail = self.check_include_thumbnail()
        if include_thumbnail is not None:
            self.build_command += include_thumbnail

        include_subtitles = self.check_include_subtitles()
        if include_subtitles is not None:
            self.build_command += include_subtitles

        optional_download_sponsorblock = self.check_optional_download_sponsorblock()
        if optional_download_sponsorblock is not None:
            self.build_command += optional_download_sponsorblock
        
        return self.build_command