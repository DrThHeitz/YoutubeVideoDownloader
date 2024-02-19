from pytube import YouTube
try:
    from tkinter import *
    from tkinter.filedialog import *
    from tkinter import ttk
except ImportError:
    from Tkinter import *
    from Tkinter.filedialog import *
    import ttk
import os
import requests
from tqdm import tqdm  # Add this import for tqdm

class Downloader(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.grid()
        Label(self, text="Where Do you want to save the MP4 file : ").grid(row=0, column=0)
        Button(self, text="Browse", width=25, command=self.save_path).grid(row=1, column=1)
        Label(self, text="The link of the Youtube Video : ").grid(row=2, column=0, sticky=W)
        self.error = Label(self)
        self.error.grid(row=5, column=0)
        self.err = Label(self)
        self.err.grid(row=6, column=0)
        self.co = Label(self)
        self.co.grid(row=6, column=1)
        self.OK = Label(self)
        self.OK.grid(row=7, column=0)
        self.link = Entry(self, width=30)
        self.link.grid(row=2, column=1)
        self.link.insert(0, "Paste the link here !")
        self.but = Button(self, text="Done !! ", width=25, bg="red", fg="white", command=self.done)
        self.but.grid(row=3, column=1)
        self.filename = ""
        self.progress = ttk.Progressbar(self, orient="horizontal", length=100, mode="determinate")
        self.progress.grid(row=4, columnspan=2, pady=10)

    def save_path(self):
        self.filename = askdirectory(title="Where to save the MP4 file")
        if self.filename == "":
            self.error.configure(text="")
            self.but.configure(bg="red")
            self.OK.configure(text="")
            print("The video will be saved in: Downloaded Videos")
            self.err.configure(text="The video will be saved in: Downloaded Videos")
        else:
            if not os.path.exists(self.filename):
                os.makedirs(self.filename)
            return self.filename

    def download_progress_callback(self, total, downloaded, status):
        downloaded_mb = downloaded / (1024 * 1024)  # Convert bytes to megabytes
        total_mb = total / (1024 * 1024)  # Convert bytes to megabytes
        percentage = (downloaded / total) * 100.0

        # Update the progress bar and display the downloaded size
        self.progress['value'] = percentage
        self.co.configure(text=f"Downloaded: {downloaded_mb:.2f} MB / {total_mb:.2f} MB")
        self.update_idletasks() 
        self.update()

    def download_video(self, link, full_path):
        response = requests.get(link, stream=True)
        total_size = int(response.headers.get('content-length', 0))

        with open(full_path, 'wb') as file:
            downloaded = 0
            for data in response.iter_content(chunk_size=1024):
                size = file.write(data)
                downloaded += size
                self.download_progress_callback(total_size, downloaded, None)


    def done(self):
        self.OK.configure(text="")
        self.but.configure(bg="red")
        self.OK.configure(text="")

        if self.link.get() == "":
            print("!! No Links !!")
            self.err.configure(text="")
            self.error.configure(text="!! No Links !!")
        else:
            if self.filename == "":
                print("No PATH_FILE selected, so default chosen.")
                self.error.configure(text="")
                self.err.configure(text="The video will be saved in: Downloaded Videos")
                self.filename = "Downloaded Videos"
            else:
                link = self.link.get()
                try:
                    yt = YouTube(link).streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
                except Exception as e:
                    print(f"Error: {e}")
                    self.err.configure(text=f"Error: {e}")
                    return

                filename = f"{yt.title}.mp4"
                full_path = os.path.join(self.filename, filename)
                print(f"Video will be saved to: {full_path}")

                try:
                    self.download_video(yt.url, full_path)
                except Exception as e:
                    print(f"Error during download: {e}")
                    self.error.configure(text=f"Error during download: {e}")
                    return

                self.err.configure(text="")
                self.error.configure(text="")
                print("Done !!!")
                self.OK.configure(text="Done !! ", fg="green")
                self.but.configure(bg="green")

t = Tk()
t.title("*** Youtube Video Downloader ***")
t.geometry("415x350")
Downloader()
t.mainloop()
