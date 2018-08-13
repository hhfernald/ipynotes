#!/usr/bin/env python3

import tkinter as tk
import os
import re

from .entry import Entry


class NameEntry(Entry):
    def __init__(self, parent, **kwargs):
        vcmd = (parent.register(self._validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        super().__init__(parent,
                         validate = 'key',
                         validatecommand = vcmd)
        self._bind_events()

    def _bind_events(self):
        events = {
            '<KP_Enter>': self.on_enter,
            '<Return>':   self.on_enter,
            }
        for trigger in events:
            self.bind(trigger, events[trigger])

    def _validate(self, action, index, value_if_allowed, prior_value, text,
                  validation_type, trigger_type, widget_name):
        DELETING_TEXT = 0
        if action == DELETING_TEXT:
            return True

        # Forbid most characters forbidden on Windows --- even on Linux
        # (in case you need to back up your notes onto an NTFS volume).
        # (But do permit slashes and backslashes, on both Windows and Linux.)
        if text in '|"*<>?:':
            return False
        return True

    def on_enter(self, event=None):
        self.event_generate("<<NewNameAccepted>>")

