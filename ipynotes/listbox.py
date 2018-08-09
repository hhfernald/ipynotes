#!/usr/bin/env python3

import tkinter as tk
import tkinter.ttk as ttk

from .time_me import time_me

NO_ITEM = -1


class Listbox(tk.Listbox):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.config(activestyle = tk.NONE)
        self.colors = ['#f0f0ff', 'white']
        self._bind_events()
        self._selected = None
        self._poll()

    #### Events ################################################################

    def _bind_events(self):
        events = {
            '<Home>':     self.select_first,
            '<End>':      self.select_last,
            }
        for trigger in events:
            self.master.bind(trigger, events[trigger])

    #### Configuration #########################################################

    def width(self, new_width = 0):
        if new_width:
            self.config(width = new_width)
        return int(self.cget("width"))

    #### Watching for selection of an item #####################################

    def _poll(self):
        """Calls self.on_select() if the listbox selection changes."""

        selected = self.index_selected()
        if self._selected != selected:
            self._selected = selected
            self.on_select()
        self.after(200, self._poll)

    def on_select(self):
        i = self.index_selected()
        if i != NO_ITEM:
            text = self.get(i)
            self.see(i)
            self.event_generate("<<ItemSelected>>")

    #### Finding or selecting an item ##########################################

    def select_text(self, item_text, quiet=False):
        index = self.find_item(item_text)
        if index != NO_ITEM:
            self.select_index(index, quiet)

    def find_item(self, item_text):
        """Returns index of item_text in listbox if found, or -1 if not."""

        items = self.get(0, tk.END)
        for i, item in enumerate(items):
            if item_text == item:
                return i
        return NO_ITEM

    def select_first(self, event=None):
        if self.size():
            self.select_index(0)

    def select_last(self, event=None):
        size = self.size()
        if size:
            self.select_index(size - 1)

    def select_index(self, index=0, quiet=False):
        """Selects the item at the given index within the listbox.

        After the item is selected, the listbox is scrolled to make the item
        visible, and the item's text is passed to the main window.

        Pass quiet=False if you don't want the "<<ItemSelected>>" event to be
        generated.
        """
        self.select_clear(0, tk.END)
        
        count = self.size()
        if index >= count:
            index = count - 1
        if index < 0:
            index = 0
        
        self.selection_set(index)
        self.update_idletasks()

        if not quiet:
            self.on_select()

    def select_next(self):
        """Moves selection down to the next item, if a next item exists."""
        
        count = self.size()
        if not count:
            return

        i = self.index_selected()
        if i == NO_ITEM:
            self.select_index(0)
        elif i + 1 < count:
            self.select_index(i + 1)

    def select_prev(self):
        """Moves selection up to the previous item, if a previous item exists."""

        count = self.size()
        if not count:
            return

        i = self.index_selected()
        if i == NO_ITEM:
            self.select_index(count - 1)
        elif i > 0:
            self.select_index(i - 1)

    #### Getting information about the selected item ###########################

    def index_selected(self):
        curselection = self.curselection()
        if curselection:
            return curselection[0]
        return NO_ITEM

    def text_selected(self):
        index = self.index_selected()
        if index == NO_ITEM:
            return ""
        else:
            text = self.get(index)
            return text

    #### Altering the selected item ############################################
    
    def rename_item(self, index, new_item):
        self.delete(index)
        self.sort(new_item)

    def sort(self, item_to_add=""):
        """Insert new item; sort items in listbox; select new item."""
        
        # Grab and sort all items.
        items = []
        if item_to_add:
            items = [item_to_add]
        for i in range(self.size()):
            items.append(self.get(i))
        items.sort()

        # Clear the listbox and put all the items back in.
        self.refill(items)

        # Reselect the item with its new name.
        if item_to_add:
            for i, item in enumerate(items):
                if item == item_to_add:
                    # (Don't generate the "<<ItemSelected>>" event.)
                    self.select_index(i, quiet=True)

    def rename_selected(self, new_text):
        index = self.index_selected()
        if index == NO_ITEM:
            return

        self.rename_item(index, new_text)

    def color_item(self, item, color):
        # Set both "foreground" (or "fg") and "selectforeground" to the same
        # color, so that the item does not lose its color when selected.
        self.itemconfig(item, {'fg': color, 'selectforeground': color})

    #### Adding and removing items in the listbox ##############################

    def _position_to_index(self, position):
        i = 0
        last = self.size() - 1
        if position == tk.END:
            i = last
        elif isinstance(position, int):
            i = int(position)
        if isinstance(position, str):
            position = position.lower()
            if position == 'end':
                i = last
        return i

    def insert(self, position, text):
        super().insert(position, text)
        index = self._position_to_index(position)
        self.stripe_index(index)

    def delete_index(self, index):
        self.delete(index)

    def stripe_index(self, index):
        color = self.colors[index % 2]
        self.itemconfigure(index, background = color)

    #@time_me("Listbox.restripe():")
    def stripe_all(self):
        for i in range(self.size()):
            self.stripe_index(i)

    def clear(self):
        self.delete(0, "end")

    #@time_me("Listbox: Clearing and re-adding items:")
    def refill(self, items):
        self.clear()
        for i, item in enumerate(items):
            self.insert(tk.END, item)
        self.stripe_all()

    def refresh(self, items):
        """Clear the listbox; add the passed items to the listbox."""

        selection = self.text_selected()
        self.refill(items)
        index = self.find_item(selection)
        if index == NO_ITEM:
            index = 0 # Always have an item selected.
        self.select_index(index)

