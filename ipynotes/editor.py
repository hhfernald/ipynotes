#!/usr/bin/env python3

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import font
import platform

from .settings import Settings


class Editor(tk.Text):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.config(wrap = tk.WORD,
                    undo = True, autoseparators = True,
                    selectbackground = "#c0c0c0")

        # Set font, font size, tab size
        font_ = self._get_default_font()
        tab_width = font_.measure("e") * 4
        tab_settings = (tab_width, "left")
        self.config(font = font_,
                           tabs = tab_settings,
                           tabstyle = "wordprocessor")

        self._starting_text = ""
        self.tag_configure("current_line", background="#e4e4f8")
        self._highlight_current_line()
        self.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
        self._bind_events()
        
    def _get_default_font(self):
        family = "Courier New"
        OS = platform.system().lower()
        if OS == 'linux':
            family = "DejaVu Sans Mono"
        elif OS == 'darwin':
            family = "Monaco"
        elif OS == 'windows':
            family = "Consolas"

        font_ = font.Font(family=family, size=9)
        return font_

    def _get_charwidth(self):
        family = self.cget("font")
        font_ = font.Font(family=family)
        return font_.measure("0")

    def _highlight_current_line(self):
        '''Re-highlights the current line every 100 milliseconds.'''
        self.tag_remove("current_line", 1.0, "end")

        # If text is selected, DON'T highlight the current line.
        try:
            text = self.get(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            self.tag_add("current_line",
                         "insert linestart", "insert lineend+1c")

        interval = 100 # milliseconds
        self.after(interval, self._highlight_current_line)

    def _bind_events(self):
        # Remove most keybindings that the Text widget has by default.
        for char in "abdefghijklmnopqrstuwyz":
            sequence = '<Control-' + char + '>'
            self.unbind(sequence)
            self.unbind_class('Text', sequence)

        events = {
            '<Control-a>': self.select_all,
            '<Control-v>': self.paste,
            '<Control-y>': self.redo,
            '<Control-z>': self.undo,
            '<KP_Enter>':  self.newline,
            }
        for trigger in events:
            self.master.bind(trigger, events[trigger])

    def select_all(self, event=None):
        self.tag_add(tk.SEL, "1.0", tk.END)
        self.mark_set(tk.INSERT, "1.0")
        self.see(tk.INSERT)
        return 'break'

    def newline(self, event=None):
        self.event_generate('<Return>')

    def undo(self, event=None):
        try:
            self.edit_undo()
        except tk.TclError:
            self.event_generate("<<UndoFailed>>")

    def redo(self, event=None):
        try:
            self.edit_redo()
        except tk.TclError:
            self.event_generate("<<RedoFailed>>")
        return "break"

    def paste(self, event=None):
        """Delete selected text, then insert text from the clipboard."""
        try:
            start = self.index("sel.first")
            end = self.index("sel.last")
            self.delete(start, end)
        except tk.TclError:
            pass
        #self.event_generate("<<Paste>>")

    def set_text(self, text, mark_unchanged = False):
        self.delete('1.0', tk.END)
        if text:
            self.insert(tk.END, text)

        # Clear the undo stack.
        self.edit_reset()

        # Move the cursor to the top of the note.
        self.mark_set(tk.INSERT, '1.0')

        # Scroll to the top of the note.
        self.xview(tk.MOVETO, 0.0)

        if mark_unchanged:
            self.edit_modified(False)

    def get_text(self):
        text = self.get('0.0', 'end-1c')
        return text

