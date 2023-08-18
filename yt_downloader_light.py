import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pytube import YouTube
import webbrowser
import os

class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video Downloader")

        self.url_label = ttk.Label(root, text="Enter YouTube URL:")
        self.url_label.pack(pady=10)

        self.url_entry = ttk.Entry(root, width=50)
        self.url_entry.pack(pady=5)

        self.download_button = ttk.Button(root, text="Download", command=self.download_video)
        self.download_button.pack(pady=10)

        self.metadata_label = ttk.Label(root, text="Video Metadata:")
        self.metadata_label.pack(pady=10)

        self.metadata_text = tk.Text(root, wrap="word", height=10, width=60)
        self.metadata_text.pack(pady=5)

    def download_video(self):
        url = self.url_entry.get()

        try:
            yt = YouTube(url)
            video_stream = yt.streams.get_highest_resolution()

            video_length_minutes = yt.length // 60
            video_length_seconds = yt.length % 60
            views_with_commas = "{:,}".format(yt.views)

            metadata = f"Title: {yt.title}\n"
            metadata += f"URL: {url}\n"
            metadata += f"Views: {views_with_commas}\n"
            metadata += f"Length: {video_length_minutes} min {video_length_seconds} sec\n"
            metadata += f"Quality: {video_stream.resolution}\n"

            self.metadata_text.delete("1.0", tk.END)
            self.metadata_text.insert("1.0", metadata)

            save_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")], initialfile=yt.title + ".mp4")
            if save_path:
                video_stream.download(output_path=os.path.dirname(save_path))
                messagebox.showinfo("Download Complete", "Video downloaded successfully!")
                self.play_video(save_path)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def play_video(self, video_path):
        webbrowser.open(video_path)

def main():
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
