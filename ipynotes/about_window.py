import tkinter as tk
import tkinter.ttk as ttk

from .app_version import *


class AboutWindow(ttk.Frame):
    """Display window with app name, author, copyright, version info."""
    
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.master.title(APP_NAME + ": About")

        text = APP_NAME
        self._label(text, True).pack()

        text = "Version " + APP_VERSION + " (" + APP_DATE + ")"
        self._label(text).pack()

        text = "A cross-platform application for organizing your notes."
        self._label(text).pack()

        text = "Written by Howard Fernald. Free and open-source."
        self._label(text).pack()

        self._padding().pack()
        self.quit_button = ttk.Button(self, text = 'OK',
                                      width = 10, command = self.close)
        self.quit_button.pack()
        self._padding().pack()
        
        self.pack()

        for sequence in ['<Return>', '<KP_Enter>', '<Escape>']:
            self.master.bind(sequence, (lambda e: self.event_generate('<space>')))
        self.quit_button.focus_set()

    def _label(self, text, heading=False):
        label = tk.Label(self, text=text, padx=32, pady=4)
        if heading:
            label.config(font=("Helvetica", 18, "bold"))
        return label

    def _padding(self):
        return tk.Canvas(self, width=10, height=8)

    def close(self, event=None):
        self.master.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    window = AboutWindow(root)
    root.mainloop()

