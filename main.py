# author : Lisa gray
# date : Nov 14th 2015
# grammar analyzer with TDD.

#stack and input buffer

# {
#    "terminals": ["a", "b"]
#    "start":"S"
#    "rules": [
#     {
#        "var": "S"
#        "deriv":["aSb", "#"]
#     },
#    ]
# }

#  a#b

# 1. [S], [a,#,b]
# 2. [a,S,b],[a,#,b]
# 3. [S, b], [#,b]
# 4. [#, b], [#,b]
# 5. [b], [b]
# 6. [], []

import unittest
import json
import sys



class GrammarAnalyzer:

    def __init__(self):
        self.stack = []
        self.input_buffer = []
        with open("grammar.json") as json_file:
            self.json = json.load(json_file)


class GrammarTestCase(unittest.TestCase):
    def setUp(self):
        self.analyzer = GrammarAnalyzer()

    def test_should_be_instantiated(self):
        self.assertIsInstance(self.analyzer, GrammarAnalyzer)
        self.assertEqual(self.analyzer.stack, [])
        self.assertEqual(self.analyzer.input_buffer, [])
        self.assertIsNotNone(self.analyzer.json)


















