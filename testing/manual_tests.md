Testing IPyNotes
================

## Testing with zero notes

IPyNotes must behave gracefully even if the `notes` folder is completely empty.

- **If the path bar is blank, but user enters text into the editor:**

  App must save text to a new file.

- **If user presses Ctrl-N when there is no current note:**

  The new note will have the default name ("note").

- **If user creates a new note, but clears out the path bar and enters text:**

  The app will submit the original name of the note as if the user had not erased the name.


