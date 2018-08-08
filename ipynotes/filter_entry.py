#!/usr/bin/env python3

import tkinter as tk

from .entry import Entry


class FilterEntry(Entry):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self._bind_events()

    def _bind_events(self):
        events = {
            }
        for trigger in events:
            self.master.bind(trigger, events[trigger])

