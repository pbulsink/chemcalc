#!/usr/bin/env python

import unittest
from chemcalc_utilities import *
from time import time

one_element = "C"
two_elements = "CH"
three_elements = "CHBr"
four_elements = "CH2Br"
five_elements = "CH3Br"
ten_elements = "(CH3Br)2"
twenty_elements = "C10H9Br"
fifty_elements = "C25H20Br5"
onehundred_elements = "C50H50"
onethousand_elements = "C500H500"
tenthousand_elements = "C5000H5000"
onehundredthousand_elements = "C50000H50000"
complex_element = "(C17H11O3N3ReCl)2"


def test(form):
    formula = parse(form).return_elements()
    start = time()
    results = isotope_distribute(formula)
    return time() - start


print test(one_element)
print test(two_elements)
print test(three_elements)
print test(four_elements)
print test(five_elements)
print test(ten_elements)
print test(twenty_elements)
print test(fifty_elements)
print test(complex_element)
