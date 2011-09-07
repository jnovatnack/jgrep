import json
import os
from tempfile import TemporaryFile
from unittest import TestCase

from json_grep import JSONGrep

class TestJSONGrep(TestCase):
    """
    Tests for the JGrep class
    """
    def test_simple(self):
        """
        Ensures we can filter a simple dict
        """
        json_grep = JSONGrep(['user'])
        source = {'userID': 5, 'url' : 'http://www.google.com'}
        result = json_grep.jgrep(json.dumps(source))
        self.assertEquals(result, {'userID': 5}) 
        
    def test_file_jgrep(self):
        """
        Ensures we can jgrep a file
        """
        tmp_file = TemporaryFile('w+')
        tmp_file.write('%s\n' % json.dumps({'user' : 'john', 'ip' : '192.168.2.2', 'city' : 'philadelphia'}))
        tmp_file.write('%s\n' % json.dumps({'user' : 'jill', 'ip' : '10.0.0.1', 'city' : 'stockholm'}))
        tmp_file.seek(0)

        
        expected_output = [
            json.dumps({'user' : 'john', 'ip' : '192.168.2.2'}),
            json.dumps({'user' : 'jill', 'ip' : '10.0.0.1'})]

        json_grep = JSONGrep(['user', 'ip'])
        output = [line for line in json_grep.jgrep_file(tmp_file)]
        self.assertEquals(expected_output, output)
         
        
                
        
        
        



