from pytube import YouTube
try:
    from tkinter import *
    from tkinter.filedialog import *
except ImportError:
    from Tkinter import *
    from Tkinter.filedialog import *
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
        self.err.grid(row=6, column =0)
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
    def save_path(self):
        self.filename = askdirectory(title="Where saved the MP4 file")
        if self.filename == "":
            self.error.configure(text="")
            self.but.configure(bg="red")
            self.OK.configure(text="")
            print("The video will be saved in: Downloaded Videos")
            self.err.configure(text="The video will be saved in: Downloaded Videos")
        else:
            return self.filename
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
                self.filename="Downloaded Videos" # The file Downloaded Videos should be created in the root 
            else:
                link = self.link.get()
                try:
                     yt = YouTube(link).streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
                except:
                    print("Connexion Error")
                    self.err.configure(text="Connexion Error")
                try:
                    yt.download(self.filename)
                except:
                    print("Some ERROR")
                    self.error.configure(text="Some ERROR")
                self.err.configure(text="")
                self.error.configure(text="")
                print("Done !!!")
                self.OK.configure(text="Done !! ", fg="green")
                self.but.configure(bg="green")

t = Tk()
t.title("*** Youtube Video Downloader ***")
t.geometry("415x300")
Downloader()
t.mainloop()