#!/usr/bin/env python3

import tkinter as tk
import tkinter.ttk as ttk


class VerticalScrollbar(ttk.Scrollbar):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        super().config(orient = "vertical")

    def attach(self, widget):
        self.config(command = widget.yview)
        widget.config(yscrollcommand = self.set)

