#!/usr/bin/env python3

import tkinter as tk


class Entry(tk.Entry):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self._starting_text = ""
        self.bind("<Control-a>", self._callback_select_all)
        self.bind('<Control-v>', self.paste)
        self.bind('<Control-y>', self.redo)
        self.bind('<Control-z>', self.undo)
        self.bind("<Escape>", self._rollback)

    def _callback_select_all(self, event):
        self.after(50, self.select_all)

    def _rollback(self, event):
        self.set_text(self._starting_text, mark_unchanged = True)

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

    def set_text(self, new_text, mark_unchanged = False):
        self.delete(0, tk.END)
        if new_text:
            self.insert(0, new_text)
        if mark_unchanged:
            self.mark_unchanged()

    def get_text_before_change(self):
        return self._starting_text

    def changed(self):
        text = self.get()
        return bool(text != self._starting_text)

    def mark_unchanged(self):
        self._starting_text = self.get()

    def select_all(self):
        self.select_range(0, tk.END)
        self.icursor(tk.END)

