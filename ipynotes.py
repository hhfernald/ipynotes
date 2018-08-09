#!/usr/bin/env python3

import tkinter as tk
from ipynotes import *
from ipynotes.app import App

root = tk.Tk()

# Add icon to application.
img = tk.PhotoImage(file = "ipynotes/ipynotes.gif")
root.iconphoto(True, img)

# Run application.
App(root)
root.mainloop()

