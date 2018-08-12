IPyNotes: Quick User's Manual
=============================



## Introduction


### What is IPyNotes?



## Installing and running IPyNotes




## Running IPyNotes for the first time


### Directories created in your home folder



### Creating and entering your first note



### Using the path bar to rename the note

Before moving the focus out of the name bar, you can roll back your changes by hitting Escape. Hitting Enter, or moving the focus out of the name bar, causes the note to be renamed to whatever is in the name bar. (Hitting Enter also moves the focus to the editor so you can start typing or editing.)

(Slashes or backslashes produce folders)



### Creating a second note

When a note is selected and you press Ctrl-N again, the new note will have the same name as the current note, except that a number is appended to the name. The path bar will be in focus, so you can edit the name to what you want.



## Using IPyNotes to create and organize notes

### Using the filter bar to find notes

*Tip:* Text with capital letters matches case and thus exclude more notes; text with only lowercase letters ignores case differences.


### Named subsets

When you enter text into the filter bar, the notes listed in the listbox are a **subset** of all of your notes. You can enter the full text manually, or you can give the full text a short name and enter that instead. Once you have the name, you can enter `s:` followed by the name instead of the full filter text.

Currently, you have to open `subsets.ini` in the `$HOME/IPyNotes/files` directory and add a line to create a subset with a name. Each subset goes on its own line and has this format:

     name = text
     
The text can include anything you'd normally type in the filter bar. You can search note names for individual words or phrases; you can search note texts; you can even nest another subset:

     basic = project writing
     novel = s:basic "stitch in time"
     notes = s:novel t:Notes

In this example, `s:novel` would match any notes whose names contained the word "project", the word "writing", and the phrase "stitch in time" (all case-insensitive); `s:notes` would match any notes matching `s:novel` whose text also contained the word "Notes" (with a capital 'N').

     name = word "a phrase" t:"in files" s:another_name

#### Cycling among subsets

One nice feature of named subsets is that you don't even have to type in the subset name. You can cycle among the named subsets with the keyboard. Pressing Ctrl-L automatically populates the filter bar with the first subset name. If the filter bar already has one of the named subsets, Ctrl-L moves to the next. If you reach the last subset and press Ctrl-L again, the filter bar is cleared, and you're back to seeing all notes (or the maximum number of notes that IPyNotes will add to the listbox).

Ctrl-Semicolon works in the same way, but it cycles backward.



### Keyboard shortcuts

- Alt-1: Filter Bar
- Alt-2: Note List
- Alt-3: Path Bar
- Alt-4: Note Editor

In the note list:

- Ctrl-Home: Select first note
- Ctrl-End: Select last note
- PageUp: Scroll up a page without selecting a different note
- PageDown: Scroll down a page without selecting a different note

In the note editor:

- Ctrl-A: Select All  
  Selects all of the current note's text.
  
- Ctrl-C: Copy Text  
  Copies selected text to the clipboard.
   
- Ctrl-D: Delete Note  
  Deletes the current note.
  
- Ctrl-J: Next Note  
  Saves the current note and loads the next note in the list.
  
- Ctrl-K: Previous Note  
  Saves the current note and loads the previous note in the list.

- Ctrl-N: New Note  
  Creates a new note.

- Ctrl-S: Save Note  
  Saves the current note immediately.

- Ctrl-V: Paste Text  
  Pastes the text on the clipboard into the current note.

- Ctrl-W: Close Window  
  Closes the main window and quits the application.

- Ctrl-X: Cut Text  
  Cuts selected text to the clipboard.

- Ctrl-Y: Redo

- Ctrl-Z: Undo


