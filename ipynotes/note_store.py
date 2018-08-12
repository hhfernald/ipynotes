#!/usr/bin/env python3

import glob
import os
import re
import shutil

from .change_log import ChangeLog
from .note_finder import NoteFinder
from .settings import Settings
from .time_me import time_me
from .utils import get_file_text


class NoteStore(object):
    def __init__(self, settings):
        self._settings = settings
        self._finder = NoteFinder(settings)
        self._log = ChangeLog(settings)
        self._EXT = '.md'
        self._names = []
        # self.refresh_name_cache()
        self._max_log_size = 1024 * 1024 * 2

    @time_me("NoteStore: Reading paths of all notes:")
    def refresh_name_cache(self):
        """Refreshes the internal list of files in the note folder."""
        
        matches = []
        top = self._settings.note_path()
        
        for root, __, filenames in os.walk(top):
            for filename in filenames:
                if filename.endswith(self._EXT):
                    path = os.path.join(root, filename)
                    matches.append(self._settings.note_path_to_name(path))

        self._names = sorted(matches)

    def total_files(self):
        if not len(self._names):
            self.refresh_name_cache()
        return len(self._names)

    def load_text(self, name):
        path = self._settings.note_name_to_path(name)
        text = get_file_text(path)
        return text

    #### Writing to files ######################################################

    def make_filename(self, name):
        """Generates from the given name the name of a nonexistent file."""

        stem = name
        number = 0
        pattern = r'\-\d+$'
        match = re.search(pattern, name)
        if match:
            text = match.group()
            number = int(text[1:])
            stem = name[:-len(text)]
        
        while True:
            path = self._settings.note_name_to_path(name)
            if not os.path.exists(path):
                break
            number += 1
            name = "-".join([stem, str(number)])
        
        return name

    def correct_name(self, name):
        """Remove objectionable characters from path; return the result.
        
        If the name is blank, return the name "note".
        """

        fixed = name.strip('\\/ \t\r\n')
        
        # Remove characters forbidden in filenames on Windows
        for char in '?":<>|*':
            fixed = fixed.replace(char, "")

        if not fixed:
            return "note"

        fixed = fixed.replace('\\', '/')
        while '//' in fixed:
            fixed = fixed.replace('//', '/')
        if os.sep != '/':
            fixed = fixed.replace('/', os.sep)

        parts = fixed.split(os.sep)
        for i, part in enumerate(parts):
            parts[i] = part.strip()
        fixed = os.sep.join(parts)

        return fixed

    def make_file(self, name, copy_content=False):
        """Create a new file, using a variation of `name` as the filename.

        If copy_content=False, an empty file is created. If copy_content=True,
        then the contents of the file with the seed_name as its filename are
        copied into the new file.
        """
        
        name = self.correct_name(name)
        name = self.make_filename(name)
        path = self._settings.note_name_to_path(name)
        
        if os.path.isfile(path):
            raise FileExistsError("A file already has that name.")
        elif os.path.isdir(path):
            raise FileExistsError("A directory already has that name.")

        if copy_content:
            old_path = self._settings.note_name_to_path(seed_name)
            shutil.copyfile(old_path, path)
            self._log.record_change("CLONE", path, old_path)
        else:
            f = open(path, mode='w', encoding='utf-8')
            f.close()
            self._log.record_change("CREATE", path)

        self._change_name_list(name, "")
        return name
    
    def _save_to_path(self, path, text):
        os.makedirs(os.path.dirname(path), exist_ok = True)
        with open(path, mode='w', encoding='utf-8') as f:
            f.write(text)
    
    def delete_text(self, orig_name):
        orig_path = self._settings.note_name_to_path(orig_name)
        self._log.record_change("DELETE", orig_path)
        try:
            os.remove(orig_path)
        except FileNotFoundError:
            pass
        self._remove_empty_dirs(orig_path)
        self._change_name_list("", orig_name)


    def save_text(self, name, text, orig_name=""):
        """Save text to the given name or a new name, depending on arguments.

        If name is given and orig_name is not, SAVE the text, overwriting
        the file with that name.

        If orig_name is given and name is not, assume the user passed a blank
        path for the note, and save the text to a new name based on the
        orig_name.

        If both name and orig_name are given, RENAME the file, i.e.,
        save the text as name, and delete the file with the orig_name.
        If the new name is already taken, then the text is saved to the
        original name, and a FileExistsError is thrown.

        Note also that the requested name may be altered, e.g., if it ends
        with spaces or contains characters bad for filenames (such as colons
        or double quotes or question marks). This function returns the name
        used to save the file.
        """

        if name == orig_name:
            orig_name = ""
        
        ok_name = self.correct_name(name)
        if not name:
            ok_name = self.make_filename(ok_name)
        ok_path = self._settings.note_name_to_path(ok_name)
        orig_path = self._settings.note_name_to_path(orig_name)

        if ok_path:
            if orig_path:
                self._log.record_change("RENAME", ok_path, orig_path)
                if os.path.exists(ok_path):
                    if orig_path == ok_path:
                        self._overwrite(ok_name, ok_path, text)
                    else:
                        self._save_as(ok_name, ok_path, text)
                else:
                    self._rename(ok_name, ok_path, orig_name, orig_path, text)
            else:
                self._overwrite(ok_name, ok_path, text)
        else:
            if orig_path:
                self._delete(orig_name, orig_path)
            else:
                # Oops--can't save anything without a name.
                raise FileNotFoundError("File's name cannot be blank.")

        return ok_name

    def _save_as(self, ok_name, ok_path, text):
        message = "This name is already taken: " + ok_path
        self._log.record_change("ERROR", message)
        ok_name = self.make_filename(ok_name)
        ok_path = self._settings.note_name_to_path(ok_name)
        self._overwrite(ok_name, ok_path, text)

    def _rename(self, ok_name, ok_path, orig_name, orig_path, text):
        """Rename the file (save it to a new file; delete the old file)."""

        self._save_to_path(ok_path, text)
        try:
            os.remove(orig_path)
        except FileNotFoundError:
            pass
        self._remove_empty_dirs(orig_path)
        self._change_name_list(ok_name, orig_name)

    def _overwrite(self, ok_name, ok_path, text):
        """Save the file, overwriting the original file."""

        self._log.record_change("SAVE", ok_path)
        self._save_to_path(ok_path, text)
        self._change_name_list(ok_name, "")

    def _delete(self, orig_name, orig_path):
        self._log.record_change("DELETE", orig_path)
        try:
            os.remove(orig_path)
        except FileNotFoundError:
            pass
        self._remove_empty_dirs(orig_path)
        self._change_name_list("", orig_name)

    def record_message(self, message):
        self._log.record_change("USER:", message)

    def _change_name_list(self, name_to_add, name_to_remove):
        change = False
        if not len(self._names):
            self.refresh_name_cache()
        
        if name_to_add:
            if name_to_add not in self._names:
                self._names.append(name_to_add)
                change = True
                
        if name_to_remove:
            if name_to_remove in self._names:
                self._names.remove(name_to_remove)
                change = True
                
        if change:
            self._names.sort()

    def _remove_empty_dirs(self, path):
        """Remove any empty directories along the path passed.

        Call this after renaming (moving) or deleting a file.
        """

        if os.path.isfile(path) or not os.path.exists(path):
            path = os.path.dirname(path)
        while path:
            try:
                os.rmdir(path)
            except OSError:
                return
            path = os.path.dirname(path)
    
    def _remove_subset_prefix(self, name):
        prefix = 's:'
        if name.startswith(prefix):
            name = name[len(prefix):]
        name = name.strip()
        return name
    
    def _add_subset_prefix(self, name):
        if name:
            return 's:' + name
        return ""
    
    def next_subset(self, name):
        name = self._remove_subset_prefix(name)
        name = self._finder.next_subset(name)
        return self._add_subset_prefix(name)
    
    def prev_subset(self, name):
        name = self._remove_subset_prefix(name)
        name = self._finder.prev_subset(name)
        return self._add_subset_prefix(name)
    
    def get_matches(self, term_string=""):
        if not len(self._names):
            self.refresh_name_cache()
        matches = self._finder.get_matches(self._names, term_string)
        return matches
        

if __name__ == "__main__":
    # run test suite
    settings = Settings()
    store = NoteStore(settings)
    # store.refresh_name_cache() # store should do this in __init__()

