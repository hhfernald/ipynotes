Planned for IPyNotes
====================

Features
--------

### Proper settings

The Settings class does not yet use configparser to load and save settings in a file; it currently just returns hard-coded values.



### Editor enhancements

- If you hit Ctrl-Enter within the editor, this should split the current note. Text before the insertion point (or before the selected text) would remain in the current note; the rest of the text would go into a new note (and the path bar would have the focus, so you can edit the name of the new note).

- Syntax highlighting for Markdown.

- Search and replace (for text in the current note, and optionally for text in other notes).

- Search and replace (for note names).

- Zoom. Ctrl-Plus should make the text in the main window larger; Ctrl-Minus should make it smaller.



### Filter bar enhancements

- The vertical bar character ("|") should be an "OR" operator, which would let you show more notes at a time --- notes that match the filter on the left side OR the right side of the bar. So `cats | dogs` would match notes that contained "cats", notes that contained "dogs", and notes that contained both words.



### Plugins

#### "Notemakers"

Each "notemaker" plugin script returns the name of a new note and some text to include in the new note. An example would be a `journal_entry` script to produce a note name like `journal/2018/08/08 Wednesday`.

Ctrl-M will invoke a dialog box, asking you what kind of note you want to create (i.e., which "notemaker" to run).


#### Filter plugins

A filter plugin would get a list of paths to note files, and a string of arguments, and the plugin would return a list of paths to the notes that meet the criteria set in the arguments. You'd be able to "call" a filter plugin from the filter bar, probably with text like `plugin:size(>4KB)`.


#### Tools

A tool plugin would get a list of note paths and would do some miscellaneous work, such as export the notes to a Markdown or EPUB file (e.g., through [pandoc], if it's installed), or back the notes up to a folder or a server, or count the number of words and sentences in the notes. A tool could return a message, which IPyNotes would then display to the user in a dialog box.



### Note History

Currently, whenever you make a change to a note, IPyNotes saves the old version of the note to a change log. IPyNotes should have a feature to let you see past versions of the current note, at the very least.



[pandoc]: http://pandoc.org/
