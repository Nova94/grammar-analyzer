#!/user/bin/env python3

import unittest
from analyzer import GrammarAnalyzer


# unit tests
class GrammarTestCase(unittest.TestCase):
    def setUp(self):
        self.analyzer = GrammarAnalyzer("grammar.json")

    def test_should_be_instantiated(self):
        self.assertIsInstance(self.analyzer, GrammarAnalyzer)
        self.assertEqual(self.analyzer.stack, [self.analyzer.json["start"]])
        self.assertEqual(self.analyzer.input_buffer, [])
        self.assertIsNotNone(self.analyzer.json)

    def test_first_grammar_fields(self):
        self.assertEqual(self.analyzer.json["terminals"], ["a", "b", "#"])
        self.assertEqual(self.analyzer.json["start"], "S")
        self.assertEqual(self.analyzer.json["rules"][0], {'var': 'S', 'derives': "aTb"})

    def test_isVariable(self):
        self.analyzer.stack.append("S")
        self.assertTrue(self.analyzer.is_variable(self.analyzer.stack.pop()))
        self.analyzer.stack.append("X")
        self.assertFalse(self.analyzer.is_variable(self.analyzer.stack.pop()))

    def test_isTerminal(self):
        self.analyzer.stack.append("a")
        self.analyzer.stack.append("S")
        self.assertFalse(self.analyzer.is_terminal(self.analyzer.stack.pop()))
        self.assertTrue(self.analyzer.is_terminal(self.analyzer.stack.pop()))

    def test_isAcceptedIfStackAndBufferAreEmpty(self):
        self.analyzer.input_buffer = 'a'
        self.assertEqual('reject', self.analyzer.is_accepted())
        self.analyzer.input_buffer = ''
        self.analyzer.stack.pop()
        self.assertEqual('accept', self.analyzer.is_accepted())

    def test_derive_rule(self):
        self.assertEqual(self.analyzer.derive("S", "a"), "aTb")
        self.assertEqual(self.analyzer.derive("T", "#"), "#")
        self.assertEqual(self.analyzer.derive("Y", "x"), None)

    def test_analyze_accept(self):
        self.analyzer.input_buffer = "aa#bb"
        self.assertEqual("accept", self.analyzer.analyze())

    def test_analyze_accept1(self):
        self.analyzer.input_buffer = "aaaaaa#bbbbbb"
        self.assertEqual("accept", self.analyzer.analyze())

    def test_analyze_reject(self):
        self.analyzer.input_buffer = "a#"
        self.assertEqual("reject", self.analyzer.analyze())

    def test_analyze_reject2(self):
        self.analyzer.input_buffer = "#"
        self.assertEqual("reject", self.analyzer.analyze())

    def test_analyze_reject3(self):
        self.analyzer.input_buffer = "aa#cb"
        self.assertEqual("reject", self.analyzer.analyze())

    def test_analyze_reject4(self):
        self.analyzer.input_buffer = "aa#cc"
        self.assertEqual("reject", self.analyzer.analyze())

    def test_analyze_grammar2_accept(self):
        self.analyzer = GrammarAnalyzer("grammar2.json")
        self.analyzer.input_buffer = "0101101010#0101011010"
        self.assertEqual("accept", self.analyzer.analyze())

    def test_analyze_grammar2_reject(self):
        self.analyzer = GrammarAnalyzer("grammar2.json")
        self.analyzer.input_buffer = "0101101010#0101101010"
        self.assertEqual("reject", self.analyzer.analyze())

    def test_analyze_grammar3_accept(self):
        self.analyzer = GrammarAnalyzer("grammar3.json")
        self.analyzer.input_buffer = "aa#bb#c#"
        self.assertEqual("accept", self.analyzer.analyze())

    def test_analyze_grammar3_accept2(self):
        self.analyzer = GrammarAnalyzer("grammar3.json")
        self.analyzer.input_buffer = "aaaaa#bbbbb#ccccccccccccccc#"
        self.assertEqual("accept", self.analyzer.analyze())

    def test_analyze_grammar3_accept3(self):
        self.analyzer = GrammarAnalyzer("grammar3.json")
        self.analyzer.input_buffer = "aaaaaaaaaaaaaa#bbbbbbbbbbbbbb#c#"
        self.assertEqual("accept", self.analyzer.analyze())

    def test_analyze_grammar3_reject(self):
        self.analyzer = GrammarAnalyzer("grammar3.json")
        self.analyzer.input_buffer = "a##c#"
        self.assertEqual("reject", self.analyzer.analyze())
