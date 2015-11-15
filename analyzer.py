# author : Lisa gray
# date : Nov 14th 2015
# grammar analyzer with TDD.

import unittest
import json
import sys


def main():
    analyzer = GrammarAnalyzer("grammar.json")
    analyzer.read_input()
    print(analyzer.analyze())


class GrammarAnalyzer:
    def __init__(self, grammar_file):
        self.input_buffer = []
        with open(grammar_file) as json_file:
            self.json = json.load(json_file)
        self.stack = [self.json["start"]]

    def read_input(self):
        self.input_buffer = raw_input("Enter String:")

    def analyze(self):
        # if stack or input_buffer is empty; then return accept or reject
        if self.stack == [] or self.input_buffer == "":
            return self.is_accepted()

        # pop off stack
        check = self.stack.pop()

        # if is_var, then peek() -> rule, push right hand side onto the stack. else reject
        if self.is_variable(check):
            self.push(self.derive(check, self.input_buffer[0]))
            return self.analyze()  # continue
        # elif is_term, then if peek() == match, remove from input_buffer else reject
        elif self.is_terminal(check):
            if check == self.input_buffer[0]:
                self.input_buffer = self.input_buffer[1:]  # 'pop' off input_buffer
                return self.analyze()  # continue
            else:
                return 'reject'
        else:
            return 'reject'

    # push rule onto the stack
    def push(self, rule):
        if rule is None:
            sys.exit('reject')
        else:
            # push rule to stack (needs to be reversely appended "aSb" -> ["b","S","a"])
            for i in rule[::-1]:
                self.stack.append(i)

    # derive the rule from variable found and peeked character
    def derive(self, variable, peek):
        for i in self.json["rules"]:  # check all rules
            if variable == i["var"] and (self.is_variable(i["derives"][0]) or i["derives"][0] == peek):  # if rule exists
                return i["derives"]  # return the rule

        return None  # otherwise, return None

    # is the character a variable?
    def is_variable(self, character):
        for i in self.json["rules"]:  # for all rules
            if character == i["var"]:  # if character matches a variable return true otherwise false
                return True
        return False

    # is the character a terminal?
    def is_terminal(self, character):
        if character in self.json["terminals"]:  # if variable is a terminal, then return true else return false
            return True
        return False

    # is in an accepted state?
    def is_accepted(self):
        # if stack and input buffer are empty, then return 'accept' else return 'reject'
        if self.stack == [] and self.input_buffer == '':
            return "accept"
        elif self.stack != [] and self.input_buffer == '':
            return "reject"
        elif self.stack == [] and self.input_buffer != '':
            return "reject"
        else:
            return "reject"


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
        self.assertEqual(self.analyzer.json["rules"][0], {'var': 'S', 'derives': "aSb"})

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
        self.assertEqual(self.analyzer.derive("S", "a"), "aSb")
        self.assertEqual(self.analyzer.derive("S", "#"), "#")
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
        self.analyzer.input_buffer = "#b"
        self.assertEqual("reject", self.analyzer.analyze())

    def test_analyze_reject3(self):
        self.analyzer.input_buffer = "aa#cb"
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

if __name__ == '__main__':
    main()
