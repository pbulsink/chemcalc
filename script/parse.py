#!/usr/bin/env python
# symbol, name, atomic number, molecular weight
import re
import string
from elements_list import ELEMENTS

sym2elt = ELEMENTS

class ElementSequence:
    def __init__(self, *seq):
        self.seq = list(seq)
        self.count = 1
        self.items = ""

    def append(self, thing):
        self.seq.append(thing)

    def set_count(self, n):
        self.count = n

    def __len__(self):
        return len(self.seq)

    def addsyms(self, weight, result):
        totalweight = weight * self.count
        for thing in self.seq:
            thing.addsyms(totalweight, result)

    def return_elements(self):
        result = {}
        self.addsyms(1, result)
        self.items = result.items()
        self.items.sort()
        return self.items

NAME, NUM, LPAREN, RPAREN, EOS = range(5)
IS_EL_RE = re.compile(r"[A-Z][a-z]*|\d+|[()]|\*|<EOS>").match

class Tokenizer:
    def __init__(self, input):
        self.input = input + "<EOS>"
        self.i = 0

    def gettoken(self):
        global ttype, tvalue
        self.lasti = self.i
        m = IS_EL_RE(self.input, self.i)
        if m is None:
            raise self.error("unexpected character")
        self.i = m.end()
        tvalue = m.group()
        if tvalue == "(":
            ttype = LPAREN
        elif tvalue == ")":
            ttype = RPAREN
        elif tvalue == "<EOS>":
            ttype = EOS
        elif "0" <= tvalue[0] <= "9":
            ttype = NUM
            tvalue = int(tvalue)
        else:
            ttype = NAME

    def error(self, msg):
        return ValueError(msg)



def parse(s):
    global t, ttype, tvalue
    #trim all spaces
    s = s.replace(" ","")
    #split at any * and attach at the end as brackets(). Only ints allowed
    ssplit = s.split('*')
    for i in range(1, len(ssplit)): #Avoid the first (molecule) item
        if ssplit[i] == "":
            raise ValueError
        char=0
        prefix = ""
        while ssplit[i][char:char+1].isdigit():
            prefix = prefix + ssplit[i][char:char+1]
            char = char + 1
        ssplit[i] = "({0}){1}".format(ssplit[i][char:], prefix)
    s = ''.join(ssplit)
    
    t = Tokenizer(s)
    t.gettoken()
    seq = parse_sequence()
    if ttype != EOS:
        error = t.error("expected end of input")
        raise error
    return seq

def parse_sequence():
    global t, ttype, tvalue
    seq = ElementSequence()
    error = ""
    while ttype in (LPAREN, NAME):
        # parenthesized expression or straight name
        if ttype == LPAREN:
            t.gettoken()
            thisguy = parse_sequence()
            if ttype != RPAREN:
                error = t.error("expected right paren")
                raise error
            t.gettoken()
        else:
            assert ttype == NAME
            if sym2elt.has_key(tvalue):
                thisguy = ElementSequence(sym2elt[tvalue])
            else:
                error = t.error("'" + tvalue + "' is not an element symbol")
                raise error
            t.gettoken()
        # followed by optional count
        if ttype == NUM:
            thisguy.set_count(tvalue)
            t.gettoken()
        seq.append(thisguy)
    if len(seq) == 0:
        error = t.error("empty sequence")
        raise error
    return seq
