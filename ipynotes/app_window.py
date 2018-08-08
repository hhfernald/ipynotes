#!/usr/bin/env python3

import tkinter as tk
import tkinter.ttk as ttk
import os
import platform

from .editor import Editor
from .filter_entry import FilterEntry
from .listbox import Listbox, NO_ITEM
from .path_entry import PathEntry
from .status_bar import StatusBar
from .scrollbar import VerticalScrollbar
from .time_me import time_me


class AppWindow(ttk.PanedWindow):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._master = master
        self.os = platform.system()
        self._halo_width = 4
        self.config(width = 600, height = 400)

        self._set_gui_style()
        self.status_bar = StatusBar(self.master)
        self._build_left_pane()
        self._build_right_pane()
        self._build_menus()
        self._bind_events()
        self._set_gui_size()
        
        self.pack(expand = 1, fill = tk.BOTH)
        self.filter_entry.focus_set()

    def _set_gui_style(self):
        style = ttk.Style()
        if self.os == 'Linux':
            style.theme_use("clam")

    def _build_left_pane(self):
        self.left_pane = ttk.Frame(self)
        
        self.filter_entry = FilterEntry(self.left_pane)
        self.filter_entry.config(bg = "#ddddcc",
                                 highlightthickness = self._halo_width)
        # filter_text = self.settings.get_filter_text()
        # self.filter_entry.set_text(filter_text)
        self.filter_entry.pack(side = tk.TOP, fill = tk.X)

        self.listbox_scrollbar = VerticalScrollbar(self.left_pane)
        self.listbox_scrollbar.pack(side = tk.RIGHT, fill = tk.Y)

        self.listbox = Listbox(self.left_pane)
        self.listbox.config(highlightthickness = self._halo_width)
        self.listbox.pack(side = tk.BOTTOM, fill = tk.BOTH, expand = True)

        self.listbox_scrollbar.attach(self.listbox)
        
        self.add(self.left_pane)

    def _build_right_pane(self):
        self.right_pane = ttk.Frame(self)
        
        self.path_entry = PathEntry(self.right_pane)
        self.path_entry.config(highlightthickness = self._halo_width)
        self.path_entry.pack(side = tk.TOP, fill = tk.X)
        
        self.editor_scrollbar = VerticalScrollbar(self.right_pane)
        self.editor_scrollbar.pack(side = tk.RIGHT, fill = tk.Y)

        self.editor = Editor(self.right_pane)
        self.editor.config(highlightthickness = self._halo_width)
        self.editor.pack(side = tk.BOTTOM, fill = tk.BOTH, expand = True)

        self.editor_scrollbar.attach(self.editor)
        
        self.add(self.right_pane)

    def _set_gui_size(self):
        self.master.resizable(True, True)
        try:
            self.master.state('zoomed') # works on Windows
        except tk.TclError:
            self.master.attributes('-zoomed', True) # works on Linux

        width = self.master.winfo_screenwidth()
        width_in_characters = width / 8 # approximate
        listbox_width = int(width_in_characters * 0.60)
        self.listbox.width(listbox_width)

    #### Setting up the menus ##################################################

    def _build_menus(self):

        # Note that the commands called by menu items only generate events,
        # which are handled by the App object.
        
        menubar = tk.Menu(self.master, border = False)
        self.master.config(menu = menubar)

        # "File" menu

        self.file_menu = tk.Menu(menubar, tearoff = False)
        menubar.add_cascade(label = "File",
                            menu = self.file_menu,
                            underline = 0)
        
        self.file_menu.add_command(label = "New Note",
                                   underline = 0,
                                   command = self.req_create_note,
                                   accelerator = "Ctrl+N")
        self.file_menu.add_command(label = "Delete Note",
                                   underline = 0,
                                   command = self.req_delete_note,
                                   accelerator = "Ctrl+D")
        self.file_menu.add_separator()
        self.file_menu.add_command(label = "Exit",
                                   underline = 1,
                                   command = self.req_close,
                                   accelerator = "Ctrl+W")

        # "View" menu

        self.view_menu = tk.Menu(menubar, tearoff = False)
        menubar.add_cascade(label = "View",
                            menu = self.view_menu,
                            underline = 0)

        self.view_menu.add_command(label = "Refresh",
                                   underline = 0,
                                   command = self.req_refresh_list,
                                   accelerator = "Ctrl+R")

        # "Go" menu

        self.go_menu = tk.Menu(menubar, tearoff = False)
        menubar.add_cascade(label = "Go",
                            menu = self.go_menu,
                            underline = 0)

        self.go_menu.add_command(label = "Filter Bar",
                                 underline = 0,
                                 command = self.filter_entry.focus_set,
                                 accelerator = "Alt+1")
        self.go_menu.add_command(label = "Note List",
                                 underline = 5,
                                 command = self.listbox.focus_set,
                                 accelerator = "Alt+2")
        self.go_menu.add_command(label = "Note Path Editor",
                                 underline = 5,
                                 command = self.path_entry.focus_set,
                                 accelerator = "Alt+3")
        self.go_menu.add_command(label = "Note Text Editor",
                                 underline = 10,
                                 command = self.editor.focus_set,
                                 accelerator = "Alt+4")

        # "Help" menu

        self.help_menu = tk.Menu(menubar, tearoff = False)
        menubar.add_cascade(label = "Help",
                            menu = self.help_menu,
                            underline = 0)
        
        self.help_menu.add_command(label = "About",
                                   underline = 0,
                                   command = self.about_this_app)

    #### Setting up keyboard shortcuts and other events ########################

    def _bind_all(self, sequence, function):
        self.master.bind(sequence, function)
        self.master.unbind_class('Text', sequence)
        self.editor.unbind(sequence)

    def _bind_events(self):
        self.master.bind('<Key>', self.on_key)

        events = {
            '<Control-d>': self.req_delete_note,
            '<Control-j>': self.req_next_note,
            '<Control-k>': self.req_prev_note,
            '<Control-n>': self.req_create_note,
            '<Control-r>': self.req_refresh_list,
            '<Control-s>': self.req_save,
            '<Control-w>': self.req_close,
            '<Alt-1>':     self.filter_entry.focus_set,
            '<Alt-2>':     self.listbox.focus_set,
            '<Alt-3>':     self.path_entry.focus_set,
            '<Alt-4>':     self.editor.focus_set,
            }
        for trigger in events:
            self._bind_all(trigger, events[trigger])

    def on_key(self, event):
        # This looks redundant, but Tkinter seems to have issues with
        # "<Alt+digit>" keypresses on both Windows and Linux. If the
        # above code doesn't work, the below code will.
                       
        alt_handlers = {'1': self.filter_entry.focus_set,
                        '2': self.listbox.focus_set,
                        '3': self.path_entry.focus_set,
                        '4': self.editor.focus_set}
        if self._alt_pressed(event):
            if event.keysym in alt_handlers:
                alt_handlers[event.keysym]()

    def _alt_pressed(self, event):
        if self.os == 'Windows':
            return bool(event.state & 0x20000)
        return bool(event.state & 0x0008)

    #### Event handlers ########################################################

    def on_redo_failure(self, event):
        self.status_bar.set_message("Nothing to redo.")

    def on_undo_failure(self, event):
        self.status_bar.set_message("Nothing to undo.")

    #### Commands available to the user ########################################

    def req_create_note(self, event=None):
        self.event_generate("<<CreateNote>>")

    def req_next_note(self, event=None):
        self.event_generate("<<NextNote>>")

    def req_prev_note(self, event=None):
        self.event_generate("<<PreviousNote>>")

    def req_delete_note(self, event=None):
        self.event_generate("<<DeleteNote>>")

    def req_refresh_list(self, event=None):
        self.event_generate("<<RefreshList>>")

    def req_save(self, event=None):
        self.event_generate("<<SaveNow>>")

    def req_close(self, event=None):
        self.event_generate("<<CloseApplication>>")

    def about_this_app(self, event=None):
        # Put up splashy dialog box???
        self.status_bar.set_message("MENU: About IPyNotes... "
                                    "(should have 'About' dialog here)")
        pass

