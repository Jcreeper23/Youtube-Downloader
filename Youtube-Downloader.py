import customtkinter as ctk
import os, threading, sys
import yt_dlp
from tkinter import messagebox

def get_download_path():
    path = os.path.join(os.path.expanduser("~"), "Documents", "YoutubeVideos")
    os.makedirs(path, exist_ok=True)
    return path


class YTDLApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Jcreepers YouTube Downloader (No ffmpeg)")
        self.geometry("500x300")
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        ctk.CTkLabel(self, text="Enter YouTube URL:", font=("Arial", 16)).pack(pady=10)

        self.url = ctk.CTkEntry(self, width=400)
        self.url.insert(0, "Paste YouTube link here...")
        self.url.pack(pady=5)

        self.audio_only = ctk.CTkCheckBox(self, text="Audio Only (MP3)")
        self.audio_only.pack(pady=5)

        self.status = ctk.CTkLabel(self, text="", text_color="lime", font=("Arial", 14))
        self.status.pack(pady=10)

        ctk.CTkButton(self, text="Download", command=self.start_download).pack(pady=10)
        ctk.CTkButton(self, text="Open Download Folder", command=self.open_folder).pack(pady=5)

    def start_download(self):
        url = self.url.get().strip()
        if not url or url == "Paste YouTube link here...":
            messagebox.showerror("Error", "Please enter a valid YouTube URL.")
            return
        self.status.configure(text="Starting download...", text_color="yellow")
        threading.Thread(target=self.download, args=(url,), daemon=True).start()

    def download(self, url):
        try:
            if self.audio_only.get():
                ydl_opts = {
                    'format': 'bestaudio[ext=m4a]/bestaudio',
                    'outtmpl': os.path.join(get_download_path(), '%(title)s.%(ext)s'),
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'ffmpeg_location': 'skip',
                }
            else:
                ydl_opts = {
                    'format': 'best[ext=mp4]/best',
                    'outtmpl': os.path.join(get_download_path(), '%(title)s.%(ext)s'),
                    'ffmpeg_location': 'skip',
                }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            self.status.configure(text="✅ Download completed!", text_color="lime")

        except Exception as e:
            print(f"[ERROR]: {e}")
            self.status.configure(text="❌ Download failed!", text_color="red")
            messagebox.showerror("Download Error", f"An error occurred:\n{e}")

    def open_folder(self):
        folder = get_download_path()
        if sys.platform == "win32":
            os.startfile(folder)
        elif sys.platform == "darwin":
            os.system(f"open '{folder}'")
        else:
            os.system(f"xdg-open '{folder}'")


if __name__ == "__main__":
    app = YTDLApp()
    app.mainloop()
