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
    def __init__(self, keys, filename):
        self.filename = filename
        self.key_regex = [re.compile('%s\w*\s' % key) for key in keys]
        self.a = [1,2,3]

    def jgrep(self):
        filtered_lines = []
        with open(self.filename) as f:
            for line in f:
                try:
                    line_dec = decode(line)
                    key_str = ' '.join(['%s ' % k for k in line_dec.keys()])
                    fline = {}
                    for regex in self.key_regex:
                        match = regex.search(key_str)
                        if match is not None:
                            key = match.group().strip()
                            fline[key] = line_dec[key]
                    
                    if fline:
                        filtered_lines.append(encode(fline))
                except:
                    pass
                
        return filtered_lines

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
   json_grep = JSONGrep(options.keys, args[0])
   lines = json_grep.jgrep()
   print '\n'.join(lines)