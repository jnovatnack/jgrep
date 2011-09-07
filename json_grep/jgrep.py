import json
import logging
import re
import sys

from optparse import OptionParser

log = logging.getLogger('jgrep')

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

    def jgrep_file(self, fd):
        """
        Greps the JSON dictionaries on each line of a file

        :Parameters: 
            fd : File 
        :rtype: list(str)
        :returns: A list of encoded and filtered JSON objects 
        """
        for line in fd:
            try:
                line = line.strip()
                fline = self.jgrep(line)
                if fline:
                    yield json.dumps(fline)
            except:
                log.exception('Exception reading line %s' % line)
                raise
    
    def jgrep(self, source_str):
        """
        Filters the keys of a source dictionary by the set of regexes
        
        :Parameters:
            source_str : src
                The json string
        :rtype: dict
        :returns: A dictonary of filtered keys
        """
        source = json.loads(source_str)

        keys = source.keys()
        fline = {}
        for regex in self.key_regex:
            for key in keys:
                match = regex.search(key)
                if match is not None:
                    fline[key] = source[key]
        return fline
