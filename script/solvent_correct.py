#!/usr/bin/env python

import os
import logging
import string
import time
from parse import *
from elements_list import ELEMENTS

TOP_BEST = {}
TOP_DIFF = 100
TOP_EA = {}

class Molecule:
    def __init__(self, formula, molfrac=1, name=""):
        self.formula = formula
        self.mass = self.calc_mass()
        self.molfrac = molfrac
        self.name = name
        self.ea_val = []

    def calc_mass(self):
        mass = 0
        for e in self.formula:
            mass = mass + float(ALL_ELEMENTS[e[0]].mw) * float(e[1])
        return mass

    def ea(self):
        if self.ea_val:
            return self.ea_val
        else:
            calc_vals = dict()
            for e in self.formula:
                calc_vals[e[0]] = (ALL_ELEMENTS[e[0]].mw * e[1] / self.mass)*100
            self.ea_val=calc_vals
            return self.ea_val

ALL_ELEMENTS = dict(ELEMENTS)
EXPERIMENTALS = {}

def get_ea(formula):
    mol = Molecule(formula)
    return "ea", mol.ea(), mol.mass

def elemental_calculate(formula):
    calc_vals = {}
    mol = Molecule(formula)
    mass = mol.mass
    for e in formula:
        calc_vals[e[0]] = (ALL_ELEMENTS[e[0]].mw * e[1] / mass)*100
    return calc_vals

def solvent_calculate(formula, sols, exp):
    formula = Molecule(formula)
    clean_ea = formula.ea()
    clean_mm = formula.mass
    solvents = []
    for s in sols:
        parsed_sol = parse(s[1]).return_elements()
        solvents.append(Molecule(parsed_sol,0,s[0]))
    global EXPERIMENTALS
    EXPERIMENTALS = dict(exp)
    start_time = time.time()
    looped = cycle_solvents(formula, solvents)
    sol_results = []
    for s in TOP_BEST:
        sol_results.append([s, TOP_BEST[s]])
    return  "corr", clean_ea, clean_mm, sol_results, TOP_EA, TOP_DIFF

def cycle_solvents(formula, solvents, num=0, looped=0):
    for i in range(0,51):
        solvents[num].molfrac = float(i) / 100
        if num < len(solvents)-1:
            looped = cycle_solvents(formula, solvents, num+1, looped)
        
        looped = looped + 1
        dirty_formula = dict(formula.formula)
        for s in solvents:
            for e in s.formula:
                if dirty_formula.has_key(e[0]):
                    dirty_formula[e[0]] = dirty_formula[e[0]] + e[1]*s.molfrac #make the dirty formula
                else:
                    dirty_formula[e[0]] = e[1]*s.molfrac
        ea_vals = Molecule(dirty_formula.items()).ea()
        biggestdiff = 0
        for key, value in ea_vals.iteritems():
            if EXPERIMENTALS.has_key(key) and EXPERIMENTALS[key] > 0:
                thisdiff = abs((float(EXPERIMENTALS[key]) - value))
                if thisdiff > biggestdiff:
                    biggestdiff = thisdiff
        global TOP_DIFF
        if biggestdiff < TOP_DIFF:
            global TOP_BEST, TOP_EA
            TOP_DIFF = biggestdiff
            for s in solvents:
                TOP_BEST[s.name]=s.molfrac
            TOP_EA = ea_vals
    return looped
