from unittest import TestCase
from cjson import encode, decode
from jgrep import JSONGrep

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
        result = json_grep.jgrep(source)
        self.assertEquals(result, {'userID': 5}) 
        
        



