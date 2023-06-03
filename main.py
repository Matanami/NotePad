from tkinter import *
import os
import sqlite3
from tkinter.messagebox import *
from tkinter.filedialog import *

class Notepad:
    _root = Tk()

    # default window width and height
    _thisWidth = 300
    _thisHeight = 300
    _thisTextArea = Text(_root)
    _thisMenuBar = Menu(_root)
    _thisFileMenu = Menu(_thisMenuBar, tearoff=0)
    _thisEditMenu = Menu(_thisMenuBar, tearoff=0)
    _thisHelpMenu = Menu(_thisMenuBar, tearoff=0)

    # to add scrollbar
    _thisScrollBar = Scrollbar(_thisTextArea)
    _file = None

    def __init__(self, **kwargs):
        # set icon
        try:
            self._root.wm_iconbitmap("Notepad.ico")
        except KeyError:
            pass
        # set window size
        try:
            self._thisWidth = kwargs['width']
        except KeyError:
            pass
        try:
            self._thisHeight = kwargs['height']
        except KeyError:
            pass
        # set the window title
        self._root.title("Untitled - Notepad")
        # center the window
        screenWidth = self._root.winfo_screenwidth()
        screenHeight = self._root.winfo_screenheight()

        # for left align
        left = (screenWidth / 2) - (self._thisWidth / 2)
        # for right align
        top = (screenHeight / 2) - (self._thisWidth / 2)
        self._root.geometry('%dx%d+%d+%d' % (self._thisWidth,
                                              self._thisHeight,
                                              left, top))

        # to make the text auti resizable
        self._root.grid_rowconfigure(0, weight=1)
        self._root.grid_columnconfigure(0, weight=1)

        # Add controls
        self._thisTextArea.grid(sticky=N + E + S + W)

        # to open new file, already existing, save
        self._thisFileMenu.add_command(label="New", command=self._newFile)
        self._thisFileMenu.add_command(label="Open", command=self._openFile)
        self._thisFileMenu.add_command(label="Save", command=self._saveFile)

        # to create a line in the dialog
        self._thisFileMenu.add_separator()
        self._thisFileMenu.add_command(label="Exit", command=self._quitApplication)
        self._thisMenuBar.add_cascade(label="File", menu=self._thisFileMenu)

        self._thisEditMenu.add_command(label="Cut", command=self._cut)
        self._thisEditMenu.add_command(label="Copy", command=self._copy)
        self._thisEditMenu.add_command(label="Paste", command=self._paste)

        self._thisMenuBar.add_cascade(label="Edit", menu=self._thisEditMenu)
        self._thisHelpMenu.add_command(label="About Notepad", command=self._showAbout)
        self._thisMenuBar.add_cascade(label="Help", menu=self._thisHelpMenu)

        self._thisScrollBar.pack(side=RIGHT, fill=Y)

        self._thisScrollBar.config(command=self._thisTextArea.yview)
        self._thisTextArea.config(yscrollcommand=self._thisScrollBar.set)

        # Create a table if it doesn't exist
        self._createTable()

    def _quitApplication(self):
        self._root.destroy()

    def _showAbout(self):
        showinfo("Notepad, Mrinal Verma")

    def _openFile(self):
        self._file = askopenfile(defaultextension=".txt",
                                 filetypes=[("All Files", "*.*"),
                                            ("Text Documents", "*.txt")])
        if self._file == "":
            self._file = None
        else:
            self._root.title(os.path.basename(self._file) + " - Notepad")
            self._thisTextArea.delete(1.0, END)
            file = open(self._file, "r")
            self._thisTextArea.insert(1.0, file.read())
            file.close()

    def _newFile(self):
        self._root.title("Untitled - Notepad")
        self._file = None
        self._thisTextArea.delete(1.0, END)

    def _saveFile(self):
        if self._file is None:
            self._file = asksaveasfilename(initialfile="Untitled.txt",
                                           defaultextension=".txt",
                                           filetypes=[("All Files", "*.*"),
                                                      ("Text Documents", "*.txt")])
            if self._file == "":
                self._file = None
            else:
                file = open(self._file, "w")
                file.write(self._thisTextArea.get(1.0, END))
                file.close()

                self._root.title(os.path.basename(self._file) + " - Notepad")
        else:
            file = open(self._file, "w")
            file.write(self._thisTextArea.get(1.0, END))
            file.close()

    def _cut(self):
        self._thisTextArea.event_generate("<<Cut>>")

    def _copy(self):
        self._thisTextArea.event_generate("<<Copy>>")

    def _paste(self):
        self._thisTextArea.event_generate("<<Paste>>")

    def _createTable(self):
        conn = sqlite3.connect("notepad.db")
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS notepad_data (text_content TEXT)")
        conn.commit()
        conn.close()

    def run(self):
        self._root.mainloop()


notepad = Notepad(width=600, height=600)
notepad.run()
