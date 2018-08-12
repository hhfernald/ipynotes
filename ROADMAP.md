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

- Have the filter bar change color when changing the name of an existing note, as opposed to a note you just created.

#### Shell-like autosuggestions

- While entering a path, the filter bar should get a list of a folder's siblings and suggest the closest match, as a good shell should. If the "notes" folder has a subfolder "tasks", which has subfolders "hearth", "home", and "hotel", then if you enter "t", the entry should suggest "tasks" (by inserting "asks" after the cursor and selecting it). If you hit `<Tab>`, the entry would contain "tasks/" and would select the first subfolder "hearth". If you type an "h", "earth" is still selected. If you then type an "o", you'd get the first subfolder that begins with "ho", so "me" would be selected. If you typed a "t", "el" would be selected instead. And so on.

- In addition, you could hit the `<Up>` or `<Down>` keys to cycle among the current set of subfolders. If you'd already entered "tasks/", "hearth" would be suggested, but hitting `<Down>` once would suggest "home"; hitting it again changes the suggestion to "hotel".

- You should also hit a key to bring up a panel that lets you find a path with a given string in it; pick one from the list to copy it into the filter bar.

#### Automatic management of numbers in note names

- Where the sequence of notes in a folder is important, IPyNotes should be able to add a numeric prefix to each note in the folder. When you want to move a note up or down within a folder, IPyNotes should alter the numeric prefixes in the note names automatically. The prefix format would probably be a letter or underscore followed by one or more digits, e.g., `novel/p1/c01/s01/_01 Hero realizes he's seeing the monster`.



### Side panels

Tkinter's dialog boxes don't quite work in the way you expect dialog boxes to. I'm considering having side panels instead:

- Find
- Find and Replace
- Note properties (size, date, word count, etc.)
- Image display
- Scratchpad file editor
- Subset definition file editor



### Back-end enhancements

I'll be looking for ways to speed up the refilling of the note-name cache --- maybe with a coroutine or thread that scans the subfolders of the "notes" folder for changes, so the NoteStore object knows which subfolders to re-read and which to skip.



### Plugins

#### "Notemakers"

Each "notemaker" plugin script returns the name of a new note and some text to include in the new note. An example would be a `journal_entry` script to produce a note name like `journal/2018/08/08 Wednesday`.

Ctrl-M will invoke a dialog box, asking you what kind of note you want to create (i.e., which "notemaker" to run).


#### Filter plugins

A filter plugin would get a list of paths to note files, and a string of arguments, and the plugin would return a list of paths to the notes that meet the criteria set in the arguments. You'd be able to "call" a filter plugin from the filter bar, probably with text like `plugin:size(>4KB)`.


#### Tools

A tool plugin would get a list of note paths and would do some miscellaneous work, such as export the notes to a Markdown or EPUB file (e.g., through [pandoc], if it's installed), or back the notes up to a folder or a server, or count the number of words and sentences in the notes. A tool could return a message, which IPyNotes would then display to the user in a dialog box.


#### Sidebars

If I implement sidebars, it makes sense to allow for plugins to add new sidebars to the sidebar pane. This would create a new class, inherited from tk.Frame, where you could place widgets to your heart's content. I haven't worked out the mechanism by which the sidebar could ask the app for information to work on (e.g., the current line in the current note text; the current note name or path; the current filter string; the current note list; etc.).



### Note History

Currently, whenever you make a change to a note, IPyNotes saves the old version of the note to a change log. IPyNotes should have a feature to let you see past versions of the current note, at the very least.



[pandoc]: http://pandoc.org/
