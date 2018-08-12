### What guidelines did I follow in writing this?

I've been keeping notes on various things for a long time. I have literally thousands of notes for various projects, and organizing and keeping track of them all has often been a pain. Over the years, I've tried many different applications and schemes for storing, retrieving, and editing notes. I've even tried a few times to write my own application, only to find I wasn't happy with the result for one reason or another.

IPyNotes is my latest attempt.

Before I wrote the program, though, I sat down and listed the criteria that I wanted it to meet:


- **The app should work on more than one operating system.**
     IPyNotes is written in Python using Tkinter, which runs on Windows, Linux, and other operating systems.


- **The app should remain simple.**
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


