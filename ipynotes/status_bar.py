#!/usr/bin/env python3

import tkinter as tk
import tkinter.ttk as ttk

from .panel import StatusPanel
from .caps_panel import CapsPanel


class StatusBar(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.unsaved_panel = StatusPanel(self, width=8, anchor=tk.CENTER)
        self.unsaved_panel.pack(side = tk.RIGHT)
        
        self.caps_panel = CapsPanel(self)
        self.caps_panel.refresh()
        self.caps_panel.pack(side = tk.RIGHT)

        self.note_count = StatusPanel(self, width=20, anchor=tk.W)
        self.note_count.pack(side = tk.LEFT)

        self.message = StatusPanel(self)
        self.message.set_text("This is the status bar.")
        self.message.pack(side = tk.LEFT, fill=tk.X, expand=True)
        
        self.pack(side = tk.BOTTOM, fill=tk.X)

    def set_message(self, new_text):
        self.message.set_text(new_text)

    def clear_message(self):
        self.message.clear_text()

    def set_note_count(self, count, total):
        message = ("{:,}".format(count) + " of " +
                   "{:,}".format(total) + " notes")
        self.note_count.set_text(message)

    def set_note_count_refreshing(self):
        self.note_count.set_text("Refreshing...")
        self.update_idletasks()

    def show_saved(self):
        self.unsaved_panel.clear_text()

    def show_unsaved(self):
        self.unsaved_panel.set_text("Unsaved")

