from tkinter import *
from tkinter.ttk import Progressbar
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import OIE
import os
from multiprocessing import Process

# App dimensions
WIDTH = 720
HEIGHT = 480

class App:

    def __init__(self):

        # --------- Main Window --------- #

        self.window = Tk()
        self.window.title("Image Encryptor")
        self.window.iconbitmap("logo.ico")
        screenWidth = self.window.winfo_screenwidth()
        screenHeight = self.window.winfo_screenheight()
        positionX = (screenWidth//2) - (WIDTH//2)
        positionY = (screenHeight//2) - (HEIGHT//2)
        self.window.geometry("{}x{}+{}+{}".format(WIDTH,HEIGHT,positionX,positionY-30))
        self.window.resizable(width=FALSE, height=FALSE)
        background = ImageTk.PhotoImage(Image.open("background.png"))
        self.frame = Label(self.window, image=background)
        self.frame.place(relwidth=1, relheight=1)

        # --------- Menu Bar --------- #

        self.menuBar = Menu(self.window)
        self.window.config(menu=self.menuBar)
        file = Menu(self.menuBar, tearoff=False)
        file.add_command(label='Open image...', command=self.browse)
        file.add_separator()
        file.add_command(label='Encrypt', command=self.encrypt)
        file.add_command(label='Decrypt', command=self.decrypt)
        file.add_separator()
        file.add_command(label='Exit', command=self.window.destroy)
        self.menuBar.add_cascade(label='File', menu=file)
        about = Menu(self.menuBar, tearoff=False)
        about.add_command(label='About Image Encryptor', command=self.infos)
        self.menuBar.add_cascade(label='About', menu=about)

        # --------- Window Components --------- #

        self.filePath = Entry(self.frame, width=50, font=("dubai",13))
        self.filePath.place(x=90, y=180)
        self.filePath.insert(0, " Enter image path here...")
        self.browseButton = Button(self.frame, text="Browse for image...", padx=2, pady=6, cursor="hand2", relief='ridge', bd=1, command=self.browse)
        self.browseButton.place(x=560, y=179)
        self.encryptButton = Button(self.frame, text="Encrypt", cursor="hand2", bg="#003C8B", fg="white", relief='ridge', font=("canvas", 10, "bold"), bd=1, padx=25, pady=10, command=self.encrypt)
        self.encryptButton.place(x=180, y=272)
        self.encryptButton.bind("<Enter>", self.enteredBtn1)
        self.encryptButton.bind("<Leave>", self.leftBtn1)
        self.decryptButton = Button(self.frame, text="Decrypt", cursor="hand2", bg="#0062E2", fg="white", relief='ridge', font=("canvas", 10, "bold"), bd=1, padx=25, pady=10, command=self.decrypt)
        self.decryptButton.place(x=400, y=272)
        self.decryptButton.bind("<Enter>", self.enteredBtn2)
        self.decryptButton.bind("<Leave>", self.leftBtn2)

        self.window.mainloop()


    def browse(self):
        self.window.filename = filedialog.askopenfilename(initialdir=os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'), title="Browse", filetypes=(("JPG Files","*.jpg"),("All Files","*.*")))
        if self.window.filename!="":
            self.filePath.delete(0, 'end')
            self.filePath.insert(0, self.window.filename)

    def disable(self):
        return

    def workingOnIt(self, x):
        self.window.wm_attributes("-disabled", True)
        self.processing = Toplevel()
        screenWidth = self.window.winfo_screenwidth()
        screenHeight = self.window.winfo_screenheight()
        posX = (screenWidth//2) - (200)
        posY = (screenHeight//2) - (25)
        self.processing.geometry("{}x{}+{}+{}".format(400, 50, posX, posY-30))
        self.processing.resizable(width=FALSE, height=FALSE)
        self.processing.iconbitmap("logo.ico")
        self.processing.protocol("WM_DELETE_WINDOW", self.disable)
        self.processing.focus()
        pgbar = Progressbar(self.processing, orient=HORIZONTAL, length=350, mode='indeterminate')
        pgbar.pack()
        pgbar.start(10)
        if x==0:
            text = Label(self.processing, text="Encrypting....")
        else:
            text = Label(self.processing, text="Decrypting....")
        text.pack()
        return self.processing

    def encrypt(self):
        if os.path.exists(self.filePath.get()):
            self.encrypting = Process(target=OIE.encryptImage, args=(self.filePath.get(),))
            self.processing = self.workingOnIt(0)
            self.browseButton['state']='disabled'
            self.encryptButton['state']='disabled'
            self.decryptButton['state']='disabled'
            self.encrypting.start()
            self.window.after(5, self.check)
        else:
            messagebox.showerror("Error", "Invalid path !!")

    def decrypt(self):
        if os.path.exists(self.filePath.get()):
            self.encrypting = Process(target=OIE.decryptImage, args=(self.filePath.get(),))
            self.processing = self.workingOnIt(1)
            self.browseButton['state']='disabled'
            self.encryptButton['state']='disabled'
            self.decryptButton['state']='disabled'
            self.encrypting.start()
            self.window.after(5, self.check)
        else:
            messagebox.showerror("Error", "Invalid path !!")

    def check(self):
        if self.encrypting.is_alive():
            self.window.after(5, self.check)
        else:
            self.processing.destroy()
            self.browseButton['state']='normal'
            self.encryptButton['state']='normal'
            self.decryptButton['state']='normal'
            self.window.wm_attributes("-disabled", False)

    def enteredBtn1(self,event):
        self.encryptButton.config(bg="#0052BD")

    def leftBtn1(self,event):
        self.encryptButton.config(bg="#003C8B")

    def enteredBtn2(self,event):
        self.decryptButton.config(bg="#187DFF")

    def leftBtn2(self,event):
        self.decryptButton.config(bg="#0062E2")

    def infos(self):
        messagebox.showinfo("About Image Encryptor", "Developer: Sharaf Eddine OUTIFAOUT\nVersion: 1.0\nDate: 2019-12-29")


if __name__=='__main__':
    App()