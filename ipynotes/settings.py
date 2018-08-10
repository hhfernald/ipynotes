#!/usr/bin/env python3

import os
import configparser

from .app_version import *

# Obligatorily (on every OS):
# - config files go in $HOME/.config/IPyNotes
#
# By default (on every OS):
# - note files   go in $HOME/IPyNotes/notes
# - change files go in $HOME/IPyNotes/changes

# TODO: Add a way to save settings, e.g., at program close.

TESTING_IPYNOTES = True


class Settings:
    FILES = "files"
    NOTES = "notes"
    CHANGES = "changes"
    PLUGINS = "plugins"
    
    def __init__(self):
        home = os.path.expanduser("~")
        path = os.path.join(home, ".config", APP_NAME)
        os.makedirs(path, exist_ok = True)
        
        file = APP_NAME + ".conf"
        self._config_path = os.path.join(path, file)
        self._config = configparser.ConfigParser()

        root = os.path.join(home, APP_NAME)
        if TESTING_IPYNOTES:
            root = os.path.join(home, "Projects", APP_NAME)
            
        if not os.path.exists(self._config_path):
            self._config[APP_NAME] = {'root': root,
                                           'halo_width': 4}
            self.save()

        self._config.read(self._config_path)
        self._modified = False

        # Make sure the data folders exist.
        self._root = self.get(APP_NAME, 'root', root)
        os.makedirs(self.file_path(), exist_ok = True)
        os.makedirs(self.note_path(), exist_ok = True)
        os.makedirs(self.change_path(), exist_ok = True)

    def get(self, section, option, default_value=None):
        """Returns, as a string, the value of the option in the given section.

        If the option is not set, then the default_value is returned.
        In addition, if the existing value is None but the default_value is not,
        then the default_value is saved as the new value for the option.
        """
        
        value = None
        if self._config.has_section(section):
            if self._config.has_option(section, option):
                value = self._config.get(section, option)

        if default_value and not value:
            value = default_value
            self.set(section, option, value)
        
        return value

    def set(self, section, option, value):
        """Adds the option-value pair to the config file.

        If the section is not in the config file, the section is added also.

        All three arguments must be strings, or TypeError will be raised.
        """
        
        if not self._config.has_section(section):
            self._config.add_section(section)
        
        # option and value must be strings, or TypeError will be raised.
        self._config.set(section, option, value)
        self._modified = True

    def modified(self):
        return self._modified

    def save(self):
        """Saves the config data to the config file. Returns True on success."""
        
        success = True
        try:
            with open(self._config_path, mode='w') as f:
                self._config.write(f)
        except (OSError, IOError):
            success = False

        if success:
            self._modified = False
        return success

    def file_path(self):
        return os.path.join(self._root, self.FILES)

    def note_path(self):
        return os.path.join(self._root, self.NOTES)

    def change_path(self):
        return os.path.join(self._root, self.CHANGES)

    def plugin_path(self):
        return os.path.join(self._root, self.PLUGINS)

    def filter_plugin_path(self):
        return os.path.join(self.plugin_path(), "filters")

    def note_extension(self):
        return '.md'

    def note_name_to_path(self, name):
        if name:
            return os.path.join(self.note_path(), name + self.note_extension())
        return ""

    def note_path_to_name(self, path):
        prefix = self.note_path() + os.sep
        if prefix.startswith(os.sep):
            prefix = prefix[len(os.sep):]
        if path.startswith(os.sep):
            path = path[len(os.sep):]
        
        if path.startswith(prefix):
            path = path[len(prefix):]

        ext = self.note_extension()
        if path.endswith(ext):
            path = path[:-len(ext)]

        return path

    def app_name(self):
        return "IPyNotes"

    def max_list_size(self):
        # To keep the app from growing sluggish once the number of notes
        # in your collection grows into the tens of thousands, limit the
        # number of items that can be added to the listbox.
        return 4096


if __name__ == '__main__':
    settings = Settings()
    print("NOTE PATH:  ", settings.note_path())
    print("CHANGE PATH:", settings.change_path())

