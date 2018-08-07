IPyNotes: Quick User's Manual
=============================



## Introduction


### What is IPyNotes?


### What guidelines did I follow in writing this?


- **The app should work on more than one operating system.**
     IPyNotes is written in Python using Tkinter, which runs on Windows, Linux, and other operating systems.


- **Keep the app simple.**
     Do not add features that aren't necessary. Stick with what the file system offers: directories and filenames.

     For example, IPyNotes does not create or maintain indexes for full-text searches of notes; it simply searches files directly. IPyNotes also does not offer tags *per se*; you put tags in notes' filenames.

     Another thing that IPyNotes doesn't do is save your notes onto the cloud somewhere. (This is in contrast to, say, SimpleNote, which requires you to have an account with the SimpleNote website so that the app can sync your notes across multiple devices.) One day I may write a plugin to perform a similar task via Dropbox, but for now, all your notes would be in your home folder.


- **Use plain text.**
     Plain-text files can be opened, read, edited, and saved on just about any operating system.

     IPyNotes could have stored notes into a database, such as SQLite --- but then you'd need IPyNotes (or a SQLite file browser) to see your notes again.


- **Keep each note is in its own file.**
     If you have 10,000 notes, you have 10,000 text files. If each note is on average 1KB in size and you were to keep all notes in a single file, you'd have a 10MB text file --- which is large enough that some text editors, even today, suffer performance lags when you try to load and edit such a file.

  The advantages of the one-note-per-file model are:

  - *Loading and saving files is simple.*
     If a note is changed, then only that single note needs to be saved. If the note were part of a larger text file, then every note in the file would need to be rewritten to disk.

     Saving notes to a database would solve that problem, but of course you'd lose the advantage of plain text files.

  - *Each note automatically has its own ID and modification date.*
     The relative path of the note is sufficient to find and load the note.

  - *Small files occupy little memory.*
     The application can load just the note being viewed or worked on, and all of the memory that is not being used to hold thousands of lines from a large text file can be used instead to keep a cache of the relative paths of all of the notes in your collection.

  The drawbacks are:

  - *Small files waste some disk space.* If file systems allocate four-kilobyte blocks of disk space, and you save a one-kilobyte file, that file makes three kilobytes of space unavailable to other files. On the other hand, disk space these days is plentiful and cheap; a four-terabyte external drive can be had for a hundred bucks.

  - *File searches are slower.* It takes longer to search a thousand small files than to search a single huge file with the same content. As stated above, IPyNotes does not use full-text indexes to speed up file searches, but a couple of factors mitigate the speed issue:

     The filter bar by default searches only note paths --- which are cached in memory.

     If you specify a search of the contents of notes (by adding `t:` before a term), the search is limited to the files that match the other terms in the filter bar. If the filter bar contains `dogs t:petting cats`, then IPyNotes will produce a subset of notes whose paths contain both the word "dogs" and the word "cats" and will search the contents of only those notes for the word "petting".

     Even if you want to search *all* notes for a given phrase, the amount of time spent searching may not bother you. I did an informal test on my slightly underpowered $200 laptop (an HP Stream 11-r010nr from 2015, with a 1.60GHz Intel Celeron and 32GB of eMMC storage). Searching 20,000 small files took less than 2.5 seconds, while searching 100,000 took about 20 seconds. I currently have around 15,000 notes and doubt I will ever end up with 100,000. I imagine that most people will also not have huge numbers of notes.


- **Filenames are metadata.**
     You should always feel free to change a note's filename as need arises. IPyNotes searches note filenames by default, so add or remove keywords in note names as you see fit.


- **Use a listbox, not a treeview.**
     I've discovered that I don't like using treeviews very much. I really don't like having to click one triangle after another to see things. I wanted all my notes on one level --- in a listbox. Notes could still go into hierarchies and categories, but each note's entry would be a relative path to the note.


- **Filter the listbox in place.**
     Put the filter bar on the main window; don't make the user invoke a dialog box to see a list of search results.


- **Note order and categories are still important.**
     Notes are presented in sorted order. You can add arbitrary numbers to filenames to enforce a certain order among notes.

     Notes go into folders when their relative paths contain the path separator (either '/' or '\', on Linux or Windows). Moving a note to a different folder is as easy as renaming it.


- **Autosave is important.**
     If you're browsing among hundreds of notes, it can be easy to forget to save changes to the current note before navigating to the next note. So IPyNotes saves changes automatically. On the other hand, Ctrl-S still forces a save, because old habits die hard.


- **Make it easy to do everything with the keyboard.**
     I wanted to be able to change the list filter, go to the next or previous note in the list, edit the note's path, and switch back to the text editor without having to reach for the mouse.

     I reserved certain keyboard shortcuts --- `Ctrl` plus the four home-row keys under the right hand, `j k l ;` --- for navigating among notes and among subsets of notes.


- **The app is not for all things.**
     IPyNotes is for taking and organizing notes, and finding which notes have similar topics or similar content. It expects every note to be a Markdown file, with a `.md` extension, and it is built to let you rename notes at will --- so it isn't designed to organize source-code files in a project, for instance (since interpreters and compilers tend not to respond well when a file's name is changed arbitrarily).



### Why did I write this, really?

What I wanted was a tool that would help me to organize my many notes into a series of novels.

The thing about organizing scenes in a novel is that, while the novel may appear to be hierarchical --- a book is divided into chapters, which is divisible into scenes --- the reality is that narrative threads run through many of the scenes in a book.

Each section of a scene in a novel, each part that establishes only one or two pieces of information, each passage only a few paragraphs long, would become a note. The path of the note would include a summary of what happens or what is learned in the passage, and it would contain the names of characters or other things I'd need to track through the novel.



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


### Keyboard shortcuts

- Alt-1: Filter Bar
- Alt-2: Note List
- Alt-3: Path Bar
- Alt-4: Note Editor

In the editor:

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


