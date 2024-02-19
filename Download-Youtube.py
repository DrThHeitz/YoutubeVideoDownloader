from pytube import YouTube
from tkinter import *
from tkinter.filedialog import *
from tkinter import ttk
import os
import requests

class Downloader(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.grid()
        self.master.title("YouTube Video Downloader")
        self.master.geometry("550x300")
        self.master.resizable(True, True)
        self.configure(bg="#f0f0f0")  # Set background color

        # Checkbutton to toggle between day and dark mode
        self.dark_mode_var = IntVar()
        self.dark_mode_checkbox = Checkbutton(self, text="Dark Mode", variable=self.dark_mode_var, command=self.toggle_dark_mode, bg="#f0f0f0", font=("Arial", 10))
        self.dark_mode_checkbox.grid(row=0, column=1, sticky=E, pady=10)

        Label(self, text="Where do you want to save the MP4 file:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, pady=10)
        Button(self, text="Browse", width=25, command=self.save_path, font=("Arial", 10)).grid(row=1, column=1)
        Label(self, text="Paste the link of the YouTube video:", font=("Arial", 12), bg="#f0f0f0").grid(row=2, column=0, sticky=W, pady=10)
        self.link = Entry(self, width=30, font=("Arial", 10))
        self.link.grid(row=2, column=1)
        self.link.insert(0, "Paste the link here!")
        self.but = Button(self, text="Download", width=25, bg="#4CAF50", fg="white", font=("Arial", 12), command=self.done)
        self.but.grid(row=3, column=1, pady=20)
        self.filename = ""
        self.progress = ttk.Progressbar(self, orient="horizontal", length=300, mode="determinate")
        self.progress.grid(row=4, columnspan=2, pady=10)
        self.co = Label(self, text="", font=("Arial", 10), bg="#f0f0f0")  # Label for downloaded size
        self.co.grid(row=5, columnspan=2, pady=5)

    def toggle_dark_mode(self):
        if self.dark_mode_var.get() == 1:
            # Dark mode background color for the main frame
            self.configure(bg="#333333")
            # Dark mode text color for all widgets
            text_color = "#b0b0b0"
            # Update background and text color for specific widgets
            for widget in self.winfo_children():
                if isinstance(widget, Button):
                    # Keep button colors the same (replace with your desired color)
                    widget.configure(bg="#4CAF50", fg="#2e2e2e")
                elif isinstance(widget, Label):
                    widget.configure(bg="#333333", fg=text_color)
                elif isinstance(widget, Checkbutton):
                    widget.configure(bg="#333333", fg=text_color)
            # Set the background color for the main window
            self.master.configure(bg="#333333")
        else:
            # Day mode background color for the main frame
            self.configure(bg="#f0f0f0")
            # Day mode text color for all widgets
            text_color = "black"
            # Update background and text color for specific widgets
            for widget in self.winfo_children():
                if isinstance(widget, Button):
                    # Keep button colors the same (replace with your desired color)
                    widget.configure(bg="#4CAF50", fg="#2e2e2e")
                elif isinstance(widget, Label):
                    widget.configure(bg="#f0f0f0", fg=text_color)
                elif isinstance(widget, Checkbutton):
                    widget.configure(bg="#f0f0f0", fg=text_color)
            # Set the background color for the main window
            self.master.configure(bg="#f0f0f0")


    def save_path(self):
        self.filename = askdirectory(title="Where to save the MP4 file")
        if self.filename == "":
            print("The video will be saved in: Downloaded Videos")
        else:
            if not os.path.exists(self.filename):
                os.makedirs(self.filename)

    def download_progress_callback(self, total, downloaded, status):
        downloaded_mb = downloaded / (1024 * 1024)  # Convert bytes to megabytes
        total_mb = total / (1024 * 1024)  # Convert bytes to megabytes
        percentage = (downloaded / total) * 100.0

        # Update the progress bar and display the downloaded size
        self.progress['value'] = percentage
        self.co.configure(text=f"Downloaded: {downloaded_mb:.2f} MB / {total_mb:.2f} MB")
        self.update_idletasks()

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
        if self.link.get() == "":
            print("!! No Links !!")
        else:
            if self.filename == "":
                print("No PATH_FILE selected, so default chosen.")
                self.filename = "Downloaded Videos"
            else:
                link = self.link.get()
                try:
                    yt = YouTube(link).streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
                except Exception as e:
                    print(f"Error: {e}")
                    return

                filename = f"{yt.title}.mp4"
                full_path = os.path.join(self.filename, filename)
                print(f"Video will be saved to: {full_path}")

                try:
                    self.download_video(yt.url, full_path)
                except Exception as e:
                    print(f"Error during download: {e}")
                    return

                print("Done !!!")

t = Tk()
app = Downloader()
t.mainloop()
