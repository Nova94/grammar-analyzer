#!/usr/bin/env python3
"""
A simple grammar analyzer - trying out test driven development

There are two main criteria the grammars need to have.

    1. All rules in the grammar must have a terminal as the first symbol on the right hand side of
the rule.

    2. No variable in the grammar can have two rules with the same terminal as the first symbol on
the right hand side.

"""
__author__ = "Lisa Gray"
__date__ = "Nov 14th 2015"
__version__ = 1.0
__license__ = "MIT"

import sys
import json
import getopt


def main(argv):
    input_file = ''
    try:
        opts, args = getopt.getopt(argv, 'f:', ['file='])
    except getopt.GetoptError:
        print 'analyzer.py -f <grammar_json>'
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-f', '--file'):
            input_file = arg

    analyzer = GrammarAnalyzer(input_file)
    analyzer.read_input()
    print(analyzer.analyze())


class NoRuleFound(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class GrammarAnalyzer:
    def __init__(self, grammar_file):
        self.input_buffer = []
        try:
            with open(grammar_file) as json_file:
                self.json = json.load(json_file)
        except IOError:
            print('File not found!')
            sys.exit(2)

        self.stack = [self.json["start"]]

    def read_input(self):
        self.input_buffer = raw_input("Enter String:")

    def analyze(self):
        # if stack or input_buffer is empty; then return accept or reject
        if self.stack == [] or self.input_buffer == "":
            return self.is_accepted()

        # pop off stack
        top = self.stack.pop()

        # if is_var, then peek() -> rule, push right hand side onto the stack. else reject
        if self.is_variable(top):
            try:
                self.push(self.derive(top, self.input_buffer[0]))
                return self.analyze()  # continue
            except NoRuleFound:
                return 'reject'
        # elif is_term, then if peek() == match, remove from input_buffer else reject
        elif self.is_terminal(top):
            if top == self.input_buffer[0]:
                self.input_buffer = self.input_buffer[1:]  # 'pop' off input_buffer
                return self.analyze()  # continue
            else:
                return 'reject'
        else:
            return 'reject'

    # push rule onto the stack
    def push(self, rule):
        if rule is None:
            raise NoRuleFound('reject: no rule found')
        else:
            # push rule to stack (needs to be reversely appended "aSb" -> ["b","S","a"])
            for i in rule[::-1]:
                self.stack.append(i)

    # derive the rule from variable found and peeked character
    def derive(self, variable, peek):
        for i in self.json["rules"]:  # check all rules
            # if rule exists
            if variable == i["var"] and (self.is_variable(i["derives"][0]) or i["derives"][0] == peek):
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
        else:
            return "reject"


if __name__ == '__main__':
    main(sys.argv[1:])
