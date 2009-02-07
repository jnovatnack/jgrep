#!/usr/bin/env python
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
    def __init__(self, keys):
        """
        :Parameters:
            keys : list(str)
                A list of regular expressions
        """
        self.key_regex = [re.compile('%s\w*\s' % key) for key in keys]

    def jgrep_file(self, filename):
        """
        Greps the JSON dictionaries on each line of a file

        :Parameters: 
            filename : str
        :rtype: list(str)
        :returns: A list of encoded and filtered JSON objects 
        """
        filtered_lines = []
        with open(filename) as f:
            for line in f:
                try:
                    line_dec = decode(line)
                    fline = self.jgrep(line_dec)
                    if fline:
                        filtered_lines.append(encode(fline))
                except:
                    pass
                
        return filtered_lines
    
    def jgrep(self, source):
        """
        Filters the keys of a source dictionary by the set of regexes
        
        :Parameters:
            source : dict
                The source dictionary
        :rtype: dict
        :returns: A dictonary of filtered keys
        """
        key_str = ' '.join(['%s ' % k for k in source.keys()])
        fline = {}
        for regex in self.key_regex:
            match = regex.search(key_str)
            if match is not None:
                key = match.group().strip()
                fline[key] = source[key]
        return fline

# -----------------------------------
# Main
# -----------------------------------
def parse_args():
   parser = OptionParser()
   parser.add_option('-k', '--key' , dest='keys', action='append',
                     help='List of JSON keys to output, arg for each key')

   options, args = parser.parse_args()
   if len(args) != 1:
       parser.error('Must specify a file.')
       sys.exit()

   if not options.keys:
       parser.error('Must specify at least one key regex')
       sys.exit()

   return options, args

if __name__ == '__main__':
   options, args = parse_args()
   json_grep = JSONGrep(options.keys)
   lines = json_grep.jgrep_file(args[0])
   print '\n'.join(lines)