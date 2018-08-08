#!/usr/bin/env python3

import tkinter as tk
import tkinter.ttk as ttk


class Label(ttk.Label):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.text = tk.StringVar()
        self.config(textvariable = self.text)

