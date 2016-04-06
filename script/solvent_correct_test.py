#!/usr/bin/env python

import unittest
from decimal import *
from solvent_correct import *
from parse import *


class TestElementalAnalysis(unittest.TestCase):
    """Test the elemental analysis calculator"""

    def setUp(self):
        """Initialize the testing info"""
        self.just_c = parse("C").return_elements()
        self.just_h = parse("H").return_elements()
        self.just_n = parse("N").return_elements()
        self.just_s = parse("S").return_elements()
        self.simple_ch = parse("CH").return_elements()
        self.complex_ch = parse(
            "CH3HCH2CH2CH(CH3)CH2C(CH3)2CH2CH3").return_elements()
        self.simple_all = parse("CHNS").return_elements()
        self.complex_all = parse("C10H24N2S2").return_elements()
        self.simple_other = parse("CSi").return_elements()
        self.complex_other = parse("C17H11O6N3ReSF3").return_elements()
        self.no_chns = parse("AgCl3").return_elements()

    def test_just_c(self):
        self.assertAlmostEqual(elemental_calculate(self.just_c),
                               {"C": 100.00, "H": 0.0, "N": 0.0, "S": 0.0})

    def test_just_h(self):
        self.assertAlmostEqual(elemental_calculate(self.just_h),
                               {"C": 0.0, "H": 100.00, "N": 0.0, "S": 0.0})

    def test_just_n(self):
        self.assertAlmostEqual(elemental_calculate(self.just_n),
                               {"C": 0.0, "H": 0.0, "N": 100.00, "S": 0.0})

    def test_just_s(self):
        self.assertAlmostEqual(elemental_calculate(self.just_s),
                               {"C": 0.0, "H": 0.0, "N": 0.0, "S": 100.00})

    def test_simple_ch(self):
        self.assertAlmostEqual(elemental_calculate(self.simple_ch),
                               {"C": 92.26, "H": 7.74, "N": 0.0, "S": 0.0})

    def test_complex_ch(self):
        self.assertAlmostEqual(elemental_calculate(self.complex_ch),
                               {"C": 83.98, "H": 16.02, "N": 0.0, "S": 0.0})

    def test_simple_all(self):
        self.assertAlmostEqual(elemental_calculate(self.simple_all),
                               {"C": 29.95, "H": 1.71, "N": 23.71, "S": 54.26})

    def test_complex_all(self):
        self.assertAlmostEqual(elemental_calculate(self.complex_all),
                               {"C": 50.8, "H": 10.23, "N": 11.85, "S": 27.12})

    def test_simple_other(self):
        self.assertAlmostEqual(elemental_calculate(self.simple_other),
                               {"C": 29.95, "H": 0, "N": 0, "S": 0})

    def test_complex_other(self):
        self.assertAlmostEqual(elemental_calculate(self.complex_other),
                               {"C": 83.98, "H": 16.02, "N": 0, "S": 0})

    def test_simple_none(self):
        self.assertAlmostEqual(elemental_calculate(self.no_chns),
                               {"C": 32.48, "H": 1.76, "N": 6.68, "S": 5.1})


if __name__ == '__main__':
    unittest.main(verbosity=2)
