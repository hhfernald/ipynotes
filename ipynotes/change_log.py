#!/usr/bin/env python3

import datetime
import glob
import os

from .settings import Settings


class ChangeLog():
    def __init__(self, settings):
        self._settings = settings
        self._max_log_size = 1024 * 1024 * 2

    def _timestamp(self, filename_safe=False):
        now = datetime.datetime.now()
        pattern = '%Y-%m-%d %H:%M:%S'
        if filename_safe:
            pattern = '%Y-%m-%d_%H-%M-%S'
            
        stamp = datetime.datetime.strftime(now, pattern)
        return stamp

    def _log_path(self):
        """Return the path to the latest change log.

        If the latest change log is too big, create a new one and
        return its path.
        """

        log_folder = self._settings.change_path()
        latest_log = ""
        extension = ".log"
        
        logs = sorted(glob.glob(os.path.join(log_folder, "*" + extension)))
        if logs:
            latest_log = logs[-1]
            size = os.path.getsize(latest_log)
            if size >= self._max_log_size:
                latest_log = ""

        if not latest_log:
            name = self._timestamp(True) + extension
            latest_log = os.path.join(log_folder, name)

        return latest_log

    def _grab_file_content(self, lines, file_path):
        try:
            with open(file_path, encoding='utf-8') as f:
                lines.append("--- REPLACED TEXT FOLLOWS:\n")
                for line in f:
                    lines.append('\t' + line)
                lines.append('\n')
        except FileNotFoundError:
            lines.append("--- FILE NOT FOUND: " + file_path + "\n")

    def record_change(self, action, path, old_path=""):
        """Record in the log what will happen with a note.

        The canonical values for `action` are "CLONE", "CREATE", "DELETE",
        "ERROR", "RENAME", and "SAVE." Only CLONE and RENAME need a value
        for `old_path`.
        """
        
        line = '{:#<80}'.format("### " + self._timestamp() + ' ') + '\n'
        lines = [line]
        action = action.upper().strip()
        prefix = "--- "

        if action in ['CLONE', 'RENAME']:
            spec = '<8'
            lines.append(prefix + format(action + ':', spec) + old_path + '\n')
            lines.append(prefix + format("TO:", spec) + path + '\n')
        else:
            lines.append(prefix + action + ": " + path + '\n')

        if action in ['SAVE', 'DELETE']:
            self._grab_file_content(lines, path)
        
        if lines:
            with open(self._log_path(), mode='a', encoding='utf-8') as f:
                for line in lines:
                    f.write(line)

