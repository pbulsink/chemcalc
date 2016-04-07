#!/usr/bin/env python

import unittest
from chemcalc_utilities import is_floatable, make_secure_val, check_secure_val
from chemcalc_utilities import parse_formula, shorten_formula, sort_formula
from chemcalc_utilities import isotope_distribute, is_numeric
from parse import parse
from time import time


class TestUtilities(unittest.TestCase):

    def setUp(self):
        self.secure_string = make_secure_val('Hello')
        self.formula1 = parse_formula("C10H22")[0]
        self.formula2 = parse_formula("CH3CH2CH2CH2 CH2CH2CH2CH2CH2CH3")[0]
        self.formula3 = parse_formula("C10H22N2")[0]
        self.formula4 = parse_formula("O2C10H22N2S")[0]
        self.formula5 = parse_formula("C10H21Cl")[0]
        self.man_formula1 = [["C", 10], ["H", 22]]
        self.man_formula2 = [["C", 10], ["H", 22]]
        self.man_formula3 = [["C", 10], ["H", 22], ["N", 2]]
        self.man_formula4 = [["C", 10], ["H", 22], ["N", 2], ["S", 1], ["O", 2]]
        self.man_formula5 = [["C", 10], ["H", 21], ["Cl", 1]]

    def formula_processing_test(self, formula):
        formula = parse(formula).return_elements()
        start = time()
        _results = isotope_distribute(formula)
        return time() - start

    def test_is_floatable_ok(self):
        self.assertTrue(is_floatable(1.4))

    def test_is_floatable_no(self):
        self.assertFalse(is_floatable('no'))

    def test_secure_string_ok(self):
        self.assertEqual(check_secure_val(self.secure_string), 'Hello')

    def test_secure_string_no(self):
        mod_string = self.secure_string + '1'
        self.assertIsNone(check_secure_val(mod_string))

    def test_is_numeric_ok(self):
        self.assertTrue(is_numeric(1))
        self.assertTrue(is_numeric(1.5))

    def test_is_numeric_no(self):
        self.assertFalse(is_numeric('n'))

    def test_shorten_formula(self):
        self.assertEqual(shorten_formula(self.formula1), "C10H22")
        self.assertEqual(shorten_formula(self.formula2), "C10H22")
        self.assertEqual(shorten_formula(self.formula3), "C10H22N2")
        self.assertEqual(shorten_formula(self.formula4), "C10H22N2SO2")
        self.assertEqual(shorten_formula(self.formula5), "C10H21Cl")

    def test_sort_formula(self):
        self.assertEqual(sort_formula(self.formula1), self.man_formula1)
        self.assertEqual(sort_formula(self.formula2), self.man_formula2)
        self.assertEqual(sort_formula(self.formula3), self.man_formula3)
        self.assertEqual(sort_formula(self.formula4), self.man_formula4)
        self.assertEqual(sort_formula(self.formula5), self.man_formula5)

    def test_complex_formula(self):
        one_element = "C"
        two_elements = "CH"
        three_elements = "CHBr"
        four_elements = "CH2Br"
        five_elements = "CH3Br"
        ten_elements = "(CH3Br)2"
        twenty_elements = "C10H9Br"
        fifty_elements = "C25H20Br5"
        onehundred_elements = "C100H100"
        complex_element = "(C17H11O3N3ReCl)2"

        print(self.formula_processing_test(one_element))
        print(self.formula_processing_test(two_elements))
        print(self.formula_processing_test(three_elements))
        print(self.formula_processing_test(four_elements))
        print(self.formula_processing_test(five_elements))
        print(self.formula_processing_test(ten_elements))
        print(self.formula_processing_test(twenty_elements))
        print(self.formula_processing_test(fifty_elements))
        print(self.formula_processing_test(onehundred_elements))
        print(self.formula_processing_test(complex_element))


if __name__ == '__main__':
    unittest.main(verbosity=2)