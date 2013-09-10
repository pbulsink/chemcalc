#!/usr/bin/env python
import logging
import string
from parse import parse
from elements_list import ELEMENTS

TOP_BEST = {}
TOP_DIFF = 100
TOP_EA = {}
EXPERIMENTALS = {}


class Molecule:
    """
    This is a molecule class that takes in the formula, and will be able to
    return the mass, or the elemental analysis
    """
    def __init__(self, formula, molfrac=1, name=""):
        self.formula = formula
        self.mass = self._calc_mass()
        self.molfrac = molfrac
        self.name = name
        self._ea_val = []

    def _calc_mass(self):
        """Return the molar mass of the molecule to the self.mass"""
        mass = 0
        for e in self.formula:
            mass = mass + float(ELEMENTS[e[0]].mw) * float(e[1])
        return mass

    def ea(self):
        """Return the elemental analysis from the cache if it exists"""
        if self._ea_val:
            return self._ea_val
        else:
            calc_vals = dict()
            for e in self.formula:
                calc_vals[e[0]] = (ELEMENTS[e[0]].mw * e[1] / self.mass)*100
            self._ea_val = calc_vals
            return self._ea_val


def get_ea(formula):
    """
    External get elemental analysis.
    Returns 'ea', the elemental anaysis, and the mass
    """
    mol = Molecule(formula)
    return "ea", mol.ea(), mol.mass


def elemental_calculate(formula):
    """Internal elemental analysis. Only returns ea"""
    mol = Molecule(formula)
    return mol.ea()


def solvent_calculate(formula, sols, exp):
    """
    Main call for calculating solvent inclusion.
    Returns 'corr', the ea of the clean molecule, the molar mass,
    the solvent list with molar inclusion, the ea of the solvent inclusion, and
    the largest difference between new calculated ea and input experimental ea.
    """
    formula = Molecule(formula)
    clean_ea = formula.ea()
    clean_mm = formula.mass
    solvents = []
    for s in sols:
        parsed_sol = parse(s[1]).return_elements()
        solvents.append(Molecule(parsed_sol, 0, s[0]))
    global EXPERIMENTALS
    EXPERIMENTALS = dict(exp)
    start_time = time.time()
    looped = cycle_solvents(formula, solvents)
    logging.info("Calculation required %s loops" % looped)
    sol_results = []
    for s in TOP_BEST:
        sol_results.append([s, TOP_BEST[s]])
    return "corr", clean_ea, clean_mm, sol_results, TOP_EA, TOP_DIFF


def cycle_solvents(formula, solvents, num=0, looped=0):
    """
    Recursively loop through solvents. Returns only the number of loops done.
    Results are stored globally.
    """
    for i in range(0, 51):
        solvents[num].molfrac = float(i) / 100
        if num < len(solvents)-1:
            looped = cycle_solvents(formula, solvents, num+1, looped)

        looped = looped + 1
        dirty_formula = dict(formula.formula)
        for s in solvents:
            for e in s.formula:
                if e[0] in dirty_formula:
                    #make the dirty formula
                    dirty_formula[e[0]] = dirty_formula[e[0]] + e[1]*s.molfrac
                else:
                    dirty_formula[e[0]] = e[1]*s.molfrac
        ea_vals = Molecule(dirty_formula.items()).ea()
        biggestdiff = 0
        for key, value in ea_vals.iteritems():
            if key in EXPERIMENTALS and EXPERIMENTALS[key] > 0:
                thisdiff = abs((float(EXPERIMENTALS[key]) - value))
                if thisdiff > biggestdiff:
                    biggestdiff = thisdiff
        global TOP_DIFF
        if biggestdiff < TOP_DIFF:
            global TOP_BEST, TOP_EA
            TOP_DIFF = biggestdiff
            for s in solvents:
                TOP_BEST[s.name] = s.molfrac
            TOP_EA = ea_vals
    return looped
