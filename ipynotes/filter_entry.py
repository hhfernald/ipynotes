#!/usr/bin/env python3

import tkinter as tk

from .entry import Entry


class FilterEntry(Entry):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self._bind_events()
        self._poll_for_change()

    def _bind_events(self):
        events = {
            }
        for trigger in events:
            self.master.bind(trigger, events[trigger])

    def _poll_for_change(self, event=None):
        """Fire "<<FilterChanged>>" if the entry text has changed.

           Do not run this every time a letter is added to or removed
           from the entry. Run this once a second, so that the user has
           time to type several letters before firing the event.
        """
        if self.changed():
            self.mark_unchanged()
            self.event_generate("<<FilterChanged>>")
        self.master.after(1000, self._poll_for_change)

