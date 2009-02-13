from __future__ import with_statement
import sys
import re
from optparse import OptionParser
from cjson import decode, encode

# ---------------------------------------
# JSONGrep implementation
# ---------------------------------------
class JSONGrep(object):
    """
    A class for filtering JSON keys by a number of regexes
    """
    def __init__(self, keys, tab_delimited=False):
        """
        :Parameters:
            keys : list(str)
                A list of regular expressions
        """
        self.key_regex = [re.compile('%s' % key) for key in keys]

    def jgrep_file(self, filename):
        """
        Greps the JSON dictionaries on each line of a file

        :Parameters: 
            filename : str
        :rtype: list(str)
        :returns: A list of encoded and filtered JSON objects 
        """
        with open(filename) as f:
            for line in f:
                try:
                    line = line.strip()
                    fline = self.jgrep(line)
                    if fline:
                        yield fline
                except:
                    pass
    
    def jgrep(self, source_str):
        """
        Filters the keys of a source dictionary by the set of regexes
        
        :Parameters:
            source_str : src
                The json string
        :rtype: dict
        :returns: A dictonary of filtered keys
        """
        source = decode(source_str)

        keys = source.keys()
        fline = {}
        for regex in self.key_regex:
            for key in keys:
                match = regex.search(key)
                if match is not None:
                    fline[key] = source[key]

        return fline