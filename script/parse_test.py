#!/usr/bin/env python
"""Testing Suite"""

import unittest
from parse import *

class TestParser(unittest.TestCase):
    """Test the parsing for elements, etc"""
    def setUp(self):
        """Initialize the testing info"""
        self.goodSimple = "C2H4SO3"
        self.goodElement = "As"
        self.goodSingleBracketed = "CH2(NO2)4Cl"
        self.goodRepeated = "CH3CH2CH2CH3"
        self.goodDoubleBracketed = "CH2(N(OH)2)2Cl"
        self.goodSingleDot = "CH3CH2CH2CH3*2H2O"
        self.goodDoubleDot = "CH3CH2CH2CH3*H2O*CH3OH"
        self.goodSpaces = " CH3CH2 CH2  C(NO)2 H  "
        self.goodSingleThree = "Uuo"
        self.goodMultiThree = "C3UutH5"
        self.badOpenBracket = "CH2((NO2)2"
        self.badCloseBracket = "CH2)Cl2"
        self.badSingleElement = "Pj"
        self.badStringElement = "CH3NaPjDy"
        self.badLowers = "ch3cl2"
        self.badSymbols = "C3H8&!"
        self.badNumbers = "12C2H6"
        self.badFloatDot = "CH3CH2CH3*1.4H2O"
        self.badTrailingDot = "CH3CH2CH3*"

    def test_good_simple(self):
        """Test a simple formula"""
        self.assertEqual(parse(self.goodSimple).return_elements(),
                         [('C', 2), ('H', 4), ('O', 3), ('S', 1)])

    def test_good_element(self):
        """Test a simple element"""
        self.assertEqual(parse(self.goodElement).return_elements(),
                         [('As', 1)])

    def test_good_single_bracketed(self):
        """Test a good single bracketed"""
        self.assertEqual(parse(self.goodSingleBracketed).return_elements(),
                         [('C', 1), ('Cl', 1), ('H', 2), ('N', 4), ('O', 8)])

    def test_good_repeated(self):
        """Test repeated elements"""
        self.assertEqual(parse(self.goodRepeated).return_elements(),
                         [('C', 4), ('H', 10)])

    def test_good_double_bracketed(self):
        """Test a doubly bracketed string"""
        self.assertEqual(parse(self.goodDoubleBracketed).return_elements(),
                         [('C', 1), ('Cl', 1), ('H', 6), ('N', 2), ('O', 4)])

    def test_good_single_dot(self):
        """Test repeated elements"""
        self.assertEqual(parse(self.goodSingleDot).return_elements(),
                         [('C', 4), ('H', 14), ('O', 2)])

    def test_good_double_dot(self):
        """Test repeated elements"""
        self.assertEqual(parse(self.goodDoubleDot).return_elements(),
                         [('C', 5), ('H', 16), ('O', 2)])

    def test_good_spaces(self):
        """Test repeated elements"""
        self.assertEqual(parse(self.goodSpaces).return_elements(),
                         [('C', 4), ('H', 8), ('N', 2), ('O', 2)])

    def test_bad_open(self):
        """Test a not closed bracket"""
        self.assertRaises(ValueError, parse, self.badOpenBracket)

    def test_bad_close(self):
        """Test a bad closing bracket(not needed)"""
        self.assertRaises(ValueError, parse, self.badCloseBracket)

    def test_bad_single_element(self):
        """Test a non-existant element"""
        self.assertRaises(ValueError, parse, self.badSingleElement)

    def test_bad_string_element(self):
        """Test an non-existant element in a string"""
        self.assertRaises(ValueError, parse, self.badStringElement)

    def test_bad_lowercase(self):
        """Test a bad lowercase only string"""
        self.assertRaises(ValueError, parse, self.badLowers)

    def test_bad_symbols(self):
        """Test a string with invalid symbols"""
        self.assertRaises(ValueError, parse, self.badSymbols)

    def test_bad_leading_numbers(self):
        """Test for leading numbers"""
        self.assertRaises(ValueError, parse, self.badNumbers)

    def test_bad_float_dot(self):
        """Test for leading numbers"""
        self.assertRaises(ValueError, parse, self.badFloatDot)

    def test_bad_trailing_dot(self):
        """Test for leading numbers"""
        self.assertRaises(ValueError, parse, self.badTrailingDot)

    def test_empty_string(self):
        """Test for an empty string"""
        self.assertRaises(ValueError, parse, "")

    def test_good_single_three(self):
        """Test for three letter element"""
        self.assertEqual(parse(self.goodSingleThree).return_elements(),
                         [('Uuo', 1)])

    def test_good_multi_three(self):
        """Test for three letter element in formula"""
        self.assertEqual(parse(self.goodMultiThree).return_elements(),
                         [('C', 3), ('H', 5), ('Uut', 1)])

if __name__ == '__main__':
    unittest.main(verbosity=2)
