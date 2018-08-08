#!/usr/bin/env python3

import tkinter as tk
import tkinter.ttk as ttk
import ctypes
import platform
import re
import subprocess

from .panel import Panel


class CapsPanel(Panel):
    """Status-bar panel that displays "CAPS" when the Caps Lock key is on."""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.config(width = 5, anchor = tk.CENTER)
        self.platform = platform.system()
        self.refresh()

    def refresh(self, event=None):
        if self._caps_state():
            self.text.set("CAPS")
        else:
            self.text.set("")
        self.after(250, self.refresh)

    def _caps_state(self):
        if self.platform == 'Windows':
            return self._windows_caps_state()
        else:
            return self._unix_caps_state()

    def _unix_caps_state(self):
        # Works on Linux. Should also work on Mac OS X, but this isn't tested.
        try:
            pipe = subprocess.Popen("xset -q | grep Caps", shell=True,
                                    bufsize=200, stdout=subprocess.PIPE).stdout
            output = pipe.readline().strip()
            line = output.decode("utf-8")
            line = re.sub(r'\s+', ' ', line)
            words = line.split(" ")
            if words[1].lower() == 'caps' and words[3].lower() == 'on':
                return True
        except OSError:
            pass
        return False

    def _windows_caps_state(self):
        try:
            hllDll = ctypes.WinDLL("User32.dll")
            VK_CAPITAL = 0x14
            keystate = hllDll.GetKeyState(VK_CAPITAL)
            return bool(keystate & 0xFFFF)
        except OSError:
            pass
        return False

