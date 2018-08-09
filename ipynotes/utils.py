#!/usr/bin/env python3

import locale

def get_file_text(path):
    """Return contents of file at the given path."""
    
    with open(path, mode='rb') as f:
        b = f.read()
    try:
        text = b.decode('utf-8')
    except UnicodeDecodeError:
        text = b.decode(locale.getpreferredencoding())
    return text

