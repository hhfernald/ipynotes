#!/usr/bin/env python3

import locale

def get_file_text(path):
    """Return contents of file at the given path."""
    
    #try:
        #with open(path, encoding='utf-8') as f:
            #text = f.read()
    #except UnicodeDecodeError:
        #with open(path, encoding='latin-1') as f:
            #text = f.read().decode('string_escape')
        #print("NOTICE: Had to use Latin-1 encoding to read file:")
        #print("---", path)
    with open(path, mode='rb') as f:
        b = f.read()
    try:
        text = b.decode('utf-8')
    except UnicodeDecodeError:
        text = b.decode(locale.getpreferredencoding())
    return text

