import customtkinter as ctk
import yt_dlp
import threading
from tkinter import filedialog

app = ctk.CTk()
app.title("Video Downloader")
app.geometry("600x600")

# العنوان
title_label = ctk.CTkLabel(app, text="Video Downloader", font=("Arial", 24, "bold"))
title_label.pack(pady=30)

# مربع اللينك
url_entry = ctk.CTkEntry(app, placeholder_text="Write the link here...", width=400)
url_entry.pack(pady=10)

# اختيار النوع (Video / Audio)
type_var = ctk.StringVar(value="Video")

def on_type_change(choice):
    if choice == "Audio (MP3)":
        quality_menu.configure(state="disabled")
    else:
        quality_menu.configure(state="normal")

type_menu = ctk.CTkOptionMenu(app, values=["Video", "Audio (MP3)"], variable=type_var, width=200, command=on_type_change)
type_menu.pack(pady=10)

# قائمة الجودة
quality_var = ctk.StringVar(value="1080p")
quality_menu = ctk.CTkOptionMenu(app, values=["2160p (4K)", "1440p", "1080p", "720p", "480p", "360p"], variable=quality_var, width=200)
quality_menu.pack(pady=10)

# اختيار مجلد الحفظ
save_path_var = ctk.StringVar(value="No folder selected")

def choose_folder():
    folder = filedialog.askdirectory()
    if folder:
        save_path_var.set(folder)

folder_btn = ctk.CTkButton(app, text="Choose Save Folder", width=200, command=choose_folder)
folder_btn.pack(pady=10)

folder_label = ctk.CTkLabel(app, textvariable=save_path_var, wraplength=400)
folder_label.pack()

# شريط البروغريس
progress_bar = ctk.CTkProgressBar(app, width=400)
progress_bar.set(0)
progress_bar.pack(pady=10)

# ليبل النسبة
percent_label = ctk.CTkLabel(app, text="0%")
percent_label.pack()

# ليبل حالة التحميل
status_label = ctk.CTkLabel(app, text="")
status_label.pack(pady=10)

def get_format(quality):
    formats = {
        "2160p (4K)": "bestvideo[height<=2160]+bestaudio/best",
        "1440p":      "bestvideo[height<=1440]+bestaudio/best",
        "1080p":      "bestvideo[height<=1080]+bestaudio/best",
        "720p":       "bestvideo[height<=720]+bestaudio/best",
        "480p":       "bestvideo[height<=480]+bestaudio/best",
        "360p":       "bestvideo[height<=360]+bestaudio/best",
    }
    return formats[quality]

def progress_hook(d):
    if d['status'] == 'downloading':
        percent_str = d.get('_percent_str', '0%').strip()
        try:
            percent = float(percent_str.replace('%', '').replace('\x1b[0;94m', '').replace('\x1b[0m', ''))
            progress_bar.set(percent / 100)
            percent_label.configure(text=f"{percent:.1f}%")
        except:
            pass
    elif d['status'] == 'finished':
        progress_bar.set(1)
        percent_label.configure(text="100%")

def download_thread():
    url = url_entry.get()
    save_path = save_path_var.get()
    download_type = type_var.get()

    if download_type == "Audio (MP3)":
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{save_path}/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'extractor_args': {
                'youtube': {
                    'js_runtimes': ['node:C:\\Program Files\\nodejs\\node.exe'],
                }
            },
            'remote_components': ['ejs:github'],
            'progress_hooks': [progress_hook],
        }
    else:
        ydl_opts = {
            'format': get_format(quality_var.get()),
            'outtmpl': f'{save_path}/%(title)s.%(ext)s',
            'merge_output_format': 'mp4',
            'extractor_args': {
                'youtube': {
                    'js_runtimes': ['node:C:\\Program Files\\nodejs\\node.exe'],
                }
            },
            'remote_components': ['ejs:github'],
            'progress_hooks': [progress_hook],
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    status_label.configure(text="Download complete! ✅")
    download_btn.configure(state="normal")

def start_download():
    url = url_entry.get()

    if url == "":
        status_label.configure(text="Please enter a link first!")
        return

    if save_path_var.get() == "No folder selected":
        status_label.configure(text="Please choose a save folder first!")
        return

    status_label.configure(text="Downloading...")
    progress_bar.set(0)
    percent_label.configure(text="0%")
    download_btn.configure(state="disabled")

    thread = threading.Thread(target=download_thread)
    thread.start()

# زرار التحميل
download_btn = ctk.CTkButton(app, text="Download", width=200, command=start_download)
download_btn.pack(pady=20)

app.mainloop()