import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from pytube import YouTube
import instaloader
import yt_dlp
import os
import threading
import requests
import time
from urllib.error import URLError
from pytube.exceptions import VideoUnavailable

class VideoDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("400x400")
        
        # URL Entry
        self.url_label = tk.Label(root, text="Video URL:")
        self.url_label.pack(pady=5)
        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.pack(pady=5)
        
        # Options
        self.video_var = tk.BooleanVar(value=True)
        self.audio_var = tk.BooleanVar(value=False)
        self.convert_audio_var = tk.BooleanVar(value=False)
        self.thumbnail_var = tk.BooleanVar(value=False)
        self.video_audio_var = tk.BooleanVar(value=False)
        
        self.video_check = tk.Checkbutton(root, text="Video", variable=self.video_var)
        self.video_check.pack()
        self.audio_check = tk.Checkbutton(root, text="Audio (MP3/WAV)", variable=self.audio_var)
        self.audio_check.pack()
        self.convert_audio_check = tk.Checkbutton(root, text="Convert Audio to WAV", variable=self.convert_audio_var)
        self.convert_audio_check.pack()
        self.thumbnail_check = tk.Checkbutton(root, text="Thumbnail", variable=self.thumbnail_var)
        self.thumbnail_check.pack()
        self.video_audio_check = tk.Checkbutton(root, text="Video + Audio", variable=self.video_audio_var)
        self.video_audio_check.pack()
        
        # Video Quality Selection
        self.quality_label = tk.Label(root, text="Select Video Quality:")
        self.quality_label.pack(pady=5)
        self.quality_var = tk.StringVar(value="highest")
        self.quality_dropdown = ttk.Combobox(root, textvariable=self.quality_var, values=["highest", "720p", "480p", "360p", "240p"])
        self.quality_dropdown.pack(pady=5)
        
        # Download Button
        self.download_button = tk.Button(root, text="Download", command=self.start_download)
        self.download_button.pack(pady=10)
        
        # Progress Bar
        self.progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=10)
        
        # Status Label
        self.status_label = tk.Label(root, text="")
        self.status_label.pack(pady=5)

    def start_download(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Error", "Please enter a valid URL")
            return
        
        # Disable download button during download
        self.download_button.config(state=tk.DISABLED)
        
        # Start download in a separate thread
        threading.Thread(target=self.download_video, args=(url,)).start()
        
    def download_video(self, url):
        try:
            self.status_label.config(text="Downloading...")
            self.progress.start(10)
            
            if "youtube.com" in url or "youtu.be" in url:
                self.download_youtube_video(url)
            elif "instagram.com" in url:
                self.download_instagram_video(url)
            elif "tiktok.com" in url or "facebook.com" in url:
                self.download_other_video(url)
            else:
                messagebox.showerror("Error", "Unsupported URL")
                self.status_label.config(text="")
                self.progress.stop()
        except VideoUnavailable:
            messagebox.showerror("Error", "The requested YouTube video is unavailable.")
        except URLError:
            messagebox.showerror("Error", "Network error. Please check your internet connection.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
        finally:
            self.status_label.config(text="Download Complete")
            self.progress.stop()
            self.download_button.config(state=tk.NORMAL)

    def download_youtube_video(self, url):
        try:
            yt = YouTube(url, on_progress_callback=self.on_progress)
            if self.video_var.get():
                # Video Quality Selection
                quality = self.quality_var.get()
                if quality == "highest":
                    stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
                else:
                    stream = yt.streams.filter(progressive=True, file_extension='mp4', res=quality).first()
                
                if stream:
                    file_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
                    if file_path:
                        stream.download(output_path=os.path.dirname(file_path), filename=os.path.basename(file_path))
                else:
                    messagebox.showerror("Error", "No suitable video stream found.")
            if self.audio_var.get():
                audio_stream = yt.streams.filter(only_audio=True).first()
                if audio_stream:
                    file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3"), ("WAV files", "*.wav")])
                    if file_path:
                        audio_stream.download(output_path=os.path.dirname(file_path), filename=os.path.basename(file_path))
                        if self.convert_audio_var.get() and file_path.endswith(".mp3"):
                            self.convert_to_wav(file_path)
                else:
                    messagebox.showerror("Error", "No suitable audio stream found.")
            if self.thumbnail_var.get():
                thumbnail_url = yt.thumbnail_url
                self.download_thumbnail(thumbnail_url)
        except VideoUnavailable:
            messagebox.showerror("Error", "The requested YouTube video is unavailable.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while downloading YouTube video: {str(e)}")
        finally:
            self.progress.stop()

    def download_instagram_video(self, url):
        try:
            loader = instaloader.Instaloader()
            loader.download_profile(url, profile_pic_only=False)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while downloading Instagram video: {str(e)}")
        finally:
            self.progress.stop()

    def download_other_video(self, url):
        try:
            ydl_opts = {
                'progress_hooks': [self.ydl_progress_hook],
                'noprogress': False
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while downloading video: {str(e)}")
        finally:
            self.progress.stop()
        
    def download_thumbnail(self, url):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")])
            if file_path:
                with open(file_path, 'wb') as file:
                    file.write(response.content)
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"An error occurred while downloading thumbnail: {str(e)}")

    def on_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = (bytes_downloaded / total_size) * 100
        self.progress["value"] = percentage_of_completion
        self.root.update_idletasks()

    def ydl_progress_hook(self, d):
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes', 0)
            downloaded_bytes = d.get('downloaded_bytes', 0)
            if total_bytes > 0:
                percentage = (downloaded_bytes / total_bytes) * 100
                self.progress["value"] = percentage
                self.root.update_idletasks()
        elif d['status'] == 'finished':
            self.status_label.config(text="Download Complete")

    def convert_to_wav(self, file_path):
        try:
            from pydub import AudioSegment
            audio = AudioSegment.from_mp3(file_path)
            wav_path = file_path.replace(".mp3", ".wav")
            audio.export(wav_path, format="wav")
            messagebox.showinfo("Conversion Complete", f"Audio converted to WAV: {wav_path}")
        except ImportError:
            messagebox.showerror("Error", "pydub library is required for audio conversion. Please install it using 'pip install pydub'.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during audio conversion: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoDownloaderApp(root)
    root.mainloop()
