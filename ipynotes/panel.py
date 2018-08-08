#!/usr/bin/env python3

import tkinter as tk
import tkinter.ttk as ttk

if __name__ == "__main__":
    from label import Label
else:
    from .label import Label


class Panel(Label):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.config(border = True, relief = tk.SUNKEN)


class StatusPanel(Panel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

    def get_text(self):
        return self.text.get()

    def set_text(self, new_text):
        self.text.set(new_text)

    def clear_text(self):
        self.text.set("")


if __name__ == "__main__":
    # run test suite
    root = tk.Tk()
    label = StatusPanel(root)
    label.pack()
    label.set_text("Right, so it works")
    print(label.get_text())
    root.mainloop()

