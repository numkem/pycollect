#!/usr/bin/env python2
from Tkinter import *
from ttk import Frame, Label, Entry
from tinydb import TinyDB
import tkFileDialog
import Tkconstants


class MainView(Frame):
    def __init__(self, parent):
        "docstring"
        Frame.__init__(self, parent)

        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("Pycollect")
        self.pack(fill=BOTH)

        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        filemenu = Menu(menubar)
        filemenu.add_command(label="Open", command=self.open_database)
        filemenu.add_command(label="Exit", command=self.on_exit)
        menubar.add_cascade(label="File", menu=filemenu)

        frame1 = Frame(self)
        frame1.pack(fill=X)
        self.game_count = StringVar()
        game_count_label = Label(frame1, textvariable=self.game_count).pack()

        frame2 = Frame(self)
        frame2.pack(fill=X, side=LEFT, expand=True)
        self.game_list = Listbox(frame2)
        self.game_list.pack(fill=Y, side=LEFT, expand=True)

        # Events
        self.bind('<<update_game_count>>', self.update_game_count)
        self.bind('<<update_game_list>>', self.update_game_list)

    def on_exit(self):
        self.quit()

    def open_database(self):
        filename = tkFileDialog.askopenfilename(filetypes=[('Database files', '.db'), ('All files', '.*')])
        self.db = TinyDB(filename)
        self.games = self.db.table('games')
        print len(self.games)
        self.event_generate('<<update_game_count>>')
        self.event_generate('<<update_game_list>>')

    def update_game_count(self, args):
        self.game_count.set('Game total: {}'.format(len(self.games)))

    def update_game_list(self, args):
        self.game_list.delete(0, END)
        game_titles = [g['name'] for g in self.games.all()]
        for title in game_titles:
            self.game_list.insert(END, title)

def main():
    try:
        root = Tk()
        app = MainView(root)
        root.mainloop()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
