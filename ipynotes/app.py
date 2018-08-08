#!/usr/bin/env python3

import tkinter as tk
import tkinter.ttk as ttk

from .app_window import AppWindow
from .editor import Editor
from .filter_entry import FilterEntry
from .listbox import Listbox, NO_ITEM
from .path_entry import PathEntry
from .settings import Settings
from .status_bar import StatusBar
from .note_store import NoteStore
from .time_me import time_me


class App(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.settings = Settings()
        self.note_store = NoteStore(self.settings)

        self.master.title(self.settings.app_name())
        self.master.protocol("WM_DELETE_WINDOW", self.close)
        
        self.note_name = ""
        self.save_interval = 30000

        self.build_gui()
        self.refresh_list()
        self.poll_unsaved()
        self.focus = None

    def debug(self, text):
        self.window.status_bar.set_message(text)

    @time_me("STARTUP: Building main window:")
    def build_gui(self):
        self.window = AppWindow(self.master, orient = tk.HORIZONTAL)
        self._bind_events()
    
    def _bind_events(self):
        events = {
            '<FocusOut>':              self.focus_lost,
            '<FocusIn>':               self.focus_gained,

            '<<ItemSelected>>':        self.note_selected,
            '<<NewNameAccepted>>':     self.note_name_accepted,
            '<<RedoFailed>>':          self.redo_failed,
            '<<UndoFailed>>':          self.undo_failed,
            '<<PollFilter>>':          self.poll_filter,
            '<<CreateNote>>':          self.create_note,
            '<<NextNote>>':            self.next_note,
            '<<PreviousNote>>':        self.prev_note,
            '<<DeleteNote>>':          self.delete_note,
            '<<RefreshList>>':         self.refresh_list,
            '<<Saved>>':               self.show_saved,
            '<<Unsaved>>':             self.show_unsaved,
            '<<SaveNow>>':             self.save_if_needed,
            '<<CloseApplication>>':    self.close,
            }
        for trigger in events:
            self.master.bind(trigger, events[trigger])

    #### Event handlers ########################################################

    def focus_lost(self, event):
        pass

    def focus_gained(self, event):
        widget = None
        try:
            widget = event.widget
        except (tk.TclError, KeyError):
            pass
        self.focus = widget

    def note_selected(self, event):
        """When a note is selected: save the current note; load the new one."""

        note_name = self.window.listbox.text_selected()
        self.save_if_renamed(True)
        self.save_if_changed()

        self.window.path_entry.set_text(note_name, mark_unchanged=True)
        self.debug("App.note_selected(): Note name set as: ["
                   + note_name + "]")
        text = self.note_store.load_text(note_name)
        self.window.editor.set_text(text, mark_unchanged=True)
        self.note_name = note_name
        self.window.status_bar.clear_message()

    def note_name_accepted(self, event):
        """User pressed Enter while path entry had focus."""

        self.save_if_renamed(force=True)
        self.window.editor.focus_set()

    def redo_failed(self, event):
        self.window.status_bar.set_message("Nothing to redo.")

    def undo_failed(self, event):
        self.window.status_bar.set_message("Nothing to undo.")

    def show_saved(self, event):
        self.window.status_bar.show_saved()

    def show_unsaved(self, event):
        self.window.status_bar.show_unsaved()
        self.after(self.save_interval, self.save_if_changed)

    #### Commands available to the user ########################################

    def create_note(self, event=None):
        self.save_if_needed()
        
        old_name = self.note_name
        new_name = self.note_store.make_file(old_name)
        self.window.status_bar.set_message("New note: " + new_name)

        listbox = self.window.listbox
        index = listbox.find_item(old_name) + 1
        listbox.sort(new_name)
        #listbox.insert(index, new_name)
        #listbox.select_index(index)
        #listbox.stripe_all()
        self.window.path_entry.focus_set()
        self.show_note_count()

    def reselect_note(self):
        """If the list box lost the selection, reselect the current note."""
        
        if self.window.listbox.index_selected() == NO_ITEM:
            self.window.listbox.select_text(self.note_name)

    def next_note(self, event=None):
        self.save_if_needed()
        self.reselect_note()
        self.window.listbox.select_next()

    def prev_note(self, event=None):
        self.save_if_needed()
        self.reselect_note()
        self.window.listbox.select_prev()

    def delete_note(self, event=None):
        # Save changes anyway, just so the otherwise unsaved changes will be
        # written to the change log.
        self.save_if_needed()

        self.note_store.delete_text(self.note_name)
        
        listbox = self.window.listbox
        index = listbox.find_item(self.note_name)
        listbox.delete_index(index)
        listbox.select_index(index)
        listbox.stripe_all()
        self.show_note_count()

    def close(self, event=None):
        self.save_if_needed()
        if self.settings.modified():
            self.settings.save()

        # TODO: If options require it, ask user to give permission first.
        self.master.destroy()

    #### Updating the status bar ###############################################

    def show_note_count(self):
        """Update the "X of Y notes" panel in the status bar."""
        
        count = self.window.listbox.size()
        total = self.note_store.total_files()
        self.window.status_bar.set_note_count(count, total)

    #### Filling and refilling the note list ###################################

    def refresh_list(self, event=None):
        """Fill the note listbox for the first time."""

        self.window.status_bar.set_note_count_refreshing()
        self.note_store.refresh_name_cache()
        terms = self.window.filter_entry.get()
        names = self.note_store.get_matches(terms)
        self.window.listbox.refresh(names)
        self.show_note_count()
        self.after(500, self.poll_filter)

    def poll_filter(self, event=None):
        """If filter text has changed, clear out and refill the note list."""

        if self.window.filter_entry.changed():
            terms = self.window.filter_entry.get()
            names = self.note_store.get_matches(terms)
            self.window.listbox.refresh(names)
            self.window.filter_entry.mark_unchanged()
            self.show_note_count()

        # Keep the number reasonably large, so the user can type in two or
        # three letters before the listbox is cleared and refilled.
        self.after(1000, self.poll_filter)

    #### Checking for and saving changes #######################################

    def poll_unsaved(self, event=None):
        if (self.window.path_entry.changed()
            or self.window.editor.edit_modified()):
            self.event_generate("<<Unsaved>>")
        else:
            self.event_generate("<<Saved>>")
        self.after(250, self.poll_unsaved)

    def save_changes(self):
        """Save (and possibly rename) the current note; mark it as unchanged."""
        
        text = self.window.editor.get_text()
        req_name = self.window.path_entry.get()
        old_name = self.note_name
        if not req_name:
            req_name = old_name
        new_name = self.note_store.save_text(req_name, text, old_name)
        
        # If old_name == "", new_name should be added to list!

        self.window.path_entry.set_text(new_name, mark_unchanged=True)
        self.debug("App.save_changes(): Note name set as: ["
                   + new_name + "]")
        self.window.editor.edit_modified(False)
        self.note_name = new_name

        if req_name != new_name:
            message = "Note name changed to: " + new_name
            self.window.status_bar.set_message(message)
        
        if not old_name:
            self.window.listbox.insert(0, "_")
            self.window.listbox.rename_item(0, new_name)
            self.window.listbox.select_text(new_name)
            
        elif old_name != new_name:
            index = self.window.listbox.find_item(old_name)
            if index != NO_ITEM:
                self.window.listbox.rename_item(index, new_name)
                #self.window.listbox.select_index(index, quiet=True)
        self.show_note_count()

    def save_if_renamed(self, force=False):
        """If the path entry doesn't have focus, see if its text has changed.

        Usually this will abort if the path entry has focus, because the user
        might be in the middle of entering a new path. If a new note has been
        selected, or the window is being closed, pass force=True to run this
        function even if the path entry has focus."""

        if force or self.focus is not self.window.path_entry:
            req_name = self.window.path_entry.get()
            if req_name != self.note_name:
                self.save_changes()
                
        self.after(500, self.save_if_renamed)

    def save_if_changed(self):
        """Save the current note whenever it is found to have been changed."""

        if self.window.editor.edit_modified():
            self.save_changes()

        self.after(self.save_interval, self.save_if_changed)
        
    def save_if_needed(self, event=None):
        self.save_if_renamed(True)
        self.save_if_changed()

