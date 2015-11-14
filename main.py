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

#TODO: Read grammar from file
#TODO: Read in String from user
#TODO: Push start variable onto stack
#TODO: If var, then peek() -> rule, push right hand side onto the stack. else reject
#TODO: if term, then peek() && match, remove both else reject
#TODO: if stack empty && input buffer empty, then accept else reject

import unittest, json


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


















