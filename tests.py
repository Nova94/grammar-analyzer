#!/user/bin/env python3
"""
 unit tests for GrammarAnalyzer
"""
__author__ = "Lisa Gray"
__date__ = "Nov 14th 2015"
__version__ = 1.0
__license__ = "MIT"

import unittest
from analyzer import GrammarAnalyzer


# unit tests
class GrammarTestCase(unittest.TestCase):
    def setUp(self):
        self.analyzer = GrammarAnalyzer("grammar.json")

    # kind of a stupid test but meh.
    def test_should_be_instantiated(self):
        self.assertIsInstance(self.analyzer, GrammarAnalyzer)
        self.assertEqual(self.analyzer.stack, [self.analyzer.json["start"]])
        self.assertEqual(self.analyzer.input_buffer, [])
        self.assertIsNotNone(self.analyzer.json)

    def test_should_load_first_grammar_fields(self):
        self.assertEqual(self.analyzer.json["terminals"], ["a", "b", "#"])
        self.assertEqual(self.analyzer.json["start"], "S")
        self.assertEqual(self.analyzer.json["rules"][0], {'var': 'S', 'derives': "aTb"})

    def test_is_variable(self):
        self.analyzer.stack.append("S")
        self.assertTrue(self.analyzer.is_variable(self.analyzer.stack.pop()))
        self.analyzer.stack.append("X")
        self.assertFalse(self.analyzer.is_variable(self.analyzer.stack.pop()))

    def test_is_terminal(self):
        self.analyzer.stack.append("a")
        self.analyzer.stack.append("S")
        self.assertFalse(self.analyzer.is_terminal(self.analyzer.stack.pop()))
        self.assertTrue(self.analyzer.is_terminal(self.analyzer.stack.pop()))

    def test_is_accepted(self):
        self.analyzer.input_buffer = 'a'
        self.assertEqual('reject', self.analyzer.is_accepted())
        self.analyzer.input_buffer = ''
        self.analyzer.stack.pop()
        self.assertEqual('accept', self.analyzer.is_accepted())

    def test_should_derive_correct_rule(self):
        self.assertEqual(self.analyzer.derive("S", "a"), "aTb")
        self.assertEqual(self.analyzer.derive("T", "#"), "#")

    def test_should_derive_None(self):
        self.assertEqual(self.analyzer.derive("Y", "x"), None)
        self.assertEqual(self.analyzer.derive("S", "x"), None)

    def test_should_accept_grammar1(self):
        self.analyzer.input_buffer = "aa#bb"
        self.assertEqual("accept", self.analyzer.analyze())

    def test_should_accept_grammar1_long(self):
        self.analyzer.input_buffer = "aaaaaa#bbbbbb"
        self.assertEqual("accept", self.analyzer.analyze())

    def test_should_reject_grammar1_input_buffer_empty(self):
        self.analyzer.input_buffer = "a#"
        self.assertEqual("reject", self.analyzer.analyze())

    def test_should_reject_grammar1_no_rule(self):
        self.analyzer.input_buffer = "#"
        self.assertEqual("reject", self.analyzer.analyze())

    def test_should_reject_grammar1_invalid_char(self):
        self.analyzer.input_buffer = "aa$bb"
        self.assertEqual("reject", self.analyzer.analyze())

    def test_should_reject_grammar1_no_match_on_terminal(self):
        self.analyzer.input_buffer = "aa#cb"
        self.assertEqual("reject", self.analyzer.analyze())

    def test_should_reject_grammar1_no_match_on_terminal2(self):
        self.analyzer.input_buffer = "aa#bc"
        self.assertEqual("reject", self.analyzer.analyze())

    def test_should_accept_grammar2(self):
        self.analyzer = GrammarAnalyzer("grammar2.json")
        self.analyzer.input_buffer = "0101101010#0101011010"
        self.assertEqual("accept", self.analyzer.analyze())

    def test_should_reject_grammar2_does_not_match_terminal(self):
        self.analyzer = GrammarAnalyzer("grammar2.json")
        self.analyzer.input_buffer = "0101101010#0101101010"
        self.assertEqual("reject", self.analyzer.analyze())

    def test_should_accept_grammar3_short(self):
        self.analyzer = GrammarAnalyzer("grammar3.json")
        self.analyzer.input_buffer = "aa#bb#c#"
        self.assertEqual("accept", self.analyzer.analyze())

    def test_should_accept_grammar3_more_c(self):
        self.analyzer = GrammarAnalyzer("grammar3.json")
        self.analyzer.input_buffer = "aaaaa#bbbbb#ccccccccccccccc#"
        self.assertEqual("accept", self.analyzer.analyze())

    def test_should_accept_grammar3_more_a_b(self):
        self.analyzer = GrammarAnalyzer("grammar3.json")
        self.analyzer.input_buffer = "aaaaaaaaaaaaaa#bbbbbbbbbbbbbb#c#"
        self.assertEqual("accept", self.analyzer.analyze())

    def test_should_reject_grammar3_incorrect_rule(self):
        self.analyzer = GrammarAnalyzer("grammar3.json")
        self.analyzer.input_buffer = "##c#"
        self.assertEqual("reject", self.analyzer.analyze())
