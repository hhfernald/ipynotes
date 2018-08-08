import os
import re

from .utils import get_file_text


class NoteFinder():
    """A search engine for notes."""
    
    def __init__(self, settings):
        self._settings = settings
        self._note_path = settings.note_path()
        self._set_path = os.path.join(settings.file_path(), "sets.ini")
        self._plugin_path = settings.filter_plugin_path()
        
    def split_terms(self, term_string):
        """Splits the text into a list of terms and returns the list.

        Each group of words inside double quotes is a single term.
        Each word outside double quotes is a single term.
        A colon always terminates a term, so "a:b" is two terms.
        """
        
        terms = []
        parts = term_string.split('"')
        
        for i, part in enumerate(parts):
            phrase = bool(i % 2)
            if phrase:
                terms.append(part)
            else:
                part = part.replace(":", ": ")
                words = part.split()
                for word in words:
                    if word:
                        terms.append(word)
        return terms

    def refresh_sets(self):
        """Read sets.ini file; keep "=" lines; ignore other lines."""
        
        self._sets = {}
        try:
            with open(self._set_path, encoding = 'utf-8') as f:
                for line in f:
                    line = re.sub(r'\s+', ' ', line.strip())
                    name, value = line.split("=", 1)
                    name = name.strip()
                    value = value.strip()
                    if name and value:
                        if name not in self._sets:
                            self._sets[name] = []
                        terms = self.get_terms(value)
                        self._sets[name].extend(terms)
        except OSError:
            pass
        
    def parse_terms(self, term_list):
        """Convert a list of terms into a dict of more precise options."""
        
        name_terms = []
        file_terms = []
        plugins = []
        bad_terms = []

        MAX_TERMS = 1000 # guard against list of terms growing too long
        
        search_file = False
        resolve_set = False
        run_plugin = False

        self.refresh_sets()
        
        for term in term_list:
            if term.endswith(':'):
                if term.lower() in ['set:', 's:']:
                    resolve_set = True
                elif term.lower() in ['text:', 't:']:
                    search_file = True
                elif term.lower() in ['plugin:', 'p:']:
                    run_plugin = True
                else:
                    bad_terms.append(term)
                continue
            
            item = {'text': '', 'case': False}
            if search_file:
                if term.islower():
                    item['text'] = term.lower()
                else:
                    item['case'] = True
                    item['text'] = term
                file_terms.append(item)
                search_file = False
    	        
            elif resolve_set:
                if term in self._sets:
                    if len(terms) < MAX_TERMS:
                        term_list.extend(self._sets[term])
                else:
                    bad_terms.append("set: " + term)
                resolve_set = False

            elif run_plugin:
                plugins.append(item)
                run_plugin = False

            else:
                if term.islower():
                    item['text'] = term.lower()
                else:
                    item['case'] = True
                    item['text'] = term
                name_terms.append(item)
    	    
        return {'name_terms': name_terms, 
                'file_terms': file_terms,
                'plugins':    plugins,
                'bad_terms':  bad_terms}

    #### Searching files #######################################################

    def _text_matches(self, name, term_dict):
        match = True
        file_text = ""
        
        path = self._settings.note_name_to_path(name)
        try:
            file_text = get_file_text(path)
        except (OSError, IOError):
            pass
        
        for term in term_dict['file_terms']:
            if term['case']:
                match = bool(term['text'] in file_text)
            else:
                match = bool(term['text'] in file_text.lower())
            if not match:
                return False
        
        # If no file terms, let the name go.
        return True

    def _name_matches(self, name, term_dict):
        match = True
        
        for term in term_dict['name_terms']:
            if term['case']:
                match = bool(term['text'] in name)
            else:
                match = bool(term['text'] in name.lower())
            if not match:
                return False
        
        # If no name terms, let the name go.
        return True

    def get_matches(self, names, term_string=""):
        """Take a filter-bar term string; return a list of matching notes."""
    
        if term_string:
            matches = []
            term_dict = self.parse_terms(self.split_terms(term_string))

            # Narrow the list down quickly by matching terms in note names
            # before searching the content of any note.

            for name in names:
                if self._name_matches(name, term_dict):
                    matches.append(name)

            # To try to keep memory consumption down with initially huge
            # lists, remove items from the new list rather than construct
            # yet another list.

            i = 0
            while i < len(matches):
                if self._text_matches(matches[i], term_dict):
                    i += 1
                else:
                    matches.pop(i)
            
            # for plugin in term_dict['plugins']:
            # import plugin; if no errors:
            # instantiate plugin, pass list, get back filtered list

        else:
            matches = names
        
        max_ = self._settings.max_list_size()
        if len(matches) > max_:
            matches = matches[:max_]
        return matches
        
