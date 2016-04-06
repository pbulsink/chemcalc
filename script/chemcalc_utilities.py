#!/usr/bin/env python
import hmac
import string
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from parse import parse  # Import the parser
from secret import secret
from elements_list import ELEMENTS
from os import path, makedirs
from hashlib import md5


def check_secure_val(secure_val):
    """Verify value is unmodified, and return it"""
    if secure_val == "":
        return ""
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val
    else:
        return None


def is_floatable(s):
    """
    Return true/false if string s is float number
    """
    try:
        float(s)
    except ValueError:
        return False
    return True


def make_secure_val(val):
    """Write string with value, hash, for cookies security checking"""
    return '%s|%s' % (str(val), hmac.new(secret, str(val)).hexdigest())


def parse_formula(formula, error):
    """
    Parse formula to list of elements and number of appearances. Catch bad
    formulas and return error.
    """
    valid_formula = ""
    try:
        valid_formula = parse(formula).return_elements()
    except ValueError:
        valid_formula = None
        error += " Not a valid Formula."
    except:
        error += " Unknown Error."
    return valid_formula, error


def shorten_formula(formula):
    """
    Take a 'parsed formula' style formula and return a compact elemental
    formula. IE CH3CH2CH2CH3 --> [["C":4],["H":10]] --> C4H10
    """
    fdict = dict((x[0], x[1]) for x in formula)
    short_formula = ""
    if "C" in fdict:
        short_formula += "C"
        if fdict["C"] > 1:
            short_formula += str(fdict["C"])
        del fdict["C"]
    if "H" in fdict:
        short_formula += "H"
        if fdict["H"] > 1:
            short_formula += str(fdict["H"])
        del fdict["H"]
    if fdict:
        flist = list()
        for key in fdict:
            flist.append([key, fdict[key]])
        flist.sort()
        for e in flist:
            short_formula = short_formula + e[0]
            if e[1] > 1:
                short_formula += str(e[1])
    return short_formula


def sort_formula(formula):
    """
    Take a 'parsed formula' style formula and return a compact elemental
    formula. IE CH3CH2CH2CH3 --> [["C":4],["H":10]] not H then C
    """
    fdict = dict((x[0], x[1]) for x in formula)
    sorted_formula = list()
    if "C" in fdict:
        sorted_formula.append(["C", fdict["C"]])
        del fdict["C"]
    if "H" in fdict:
        sorted_formula.append(["H", fdict["H"]])
        del fdict["H"]
    if fdict:
        flist = list()
        for key in fdict:
            flist.append([key, fdict[key]])
        flist.sort()
        for e in flist:
            sorted_formula.append([e[0], e[1]])
    return sorted_formula


def isotope_distribute(formula):
    """calculate isotopic distribution of the provided formula"""
    e_formula = list()
    precision = 0.000001
    for e in formula:
        for f in range(0, e[1]):
            e_formula.append(e[0])
    molecule = list()
    molecule.append([0, 1.0])
    for a in e_formula:
        next_mol = list()
        for m in molecule:
            for i in ELEMENTS[a].isotopes:
                next_mol.append([i[1] + m[0], (i[2] / 100) * m[1]])
        mol = dict()
        for n in next_mol:
            if n[0] not in mol:
                mol[n[0]] = n[1]
            else:
                mol[n[0]] = mol[n[0]] + n[1]

        molecule = list()
        for key, value in mol.iteritems():
            molecule.append([key, value])

        molecule.sort()
        maximum = 0.0
        for m in molecule:
            m = list(m)
            if m[1] > maximum:
                maximum = m[1]
        for m in molecule:
            m[1] = m[1] / maximum
        molecule = [mol for mol in molecule if mol[1] > precision]
    for m in molecule:
        m[1] *= 100.00
    return molecule


def listofzero(y):
    """Return a list of zeros of length y"""
    return [0] * len(y)


def plot_isotopes(isotopes, sformula):
    """Plot the isotopes as given to file"""
    x = list()
    y = list()
    for i in isotopes:
        x.append(i[0])
        y.append(i[1])

    if x[0] < 200:
        xmin = x[0] - x[0] * 0.005
        xmax = x[-1] + x[-1] * 0.005
    elif x[0] < 1000:
        xmin = x[0] - 1
        xmax = x[-1] + 1
    else:
        xmin = x[0] - 2
        xmax = x[-1] + 2

    plt.figure()
    plt.vlines(x, [0], y, colors='b')
    plt.title('Isotopes: {}'.format(sformula))
    plt.xlabel('Mass (amu)')
    plt.ylabel('Intensity (a.u.)')
    plt.ylim(0, 110)
    plt.xlim(xmin, xmax)

    return plt


def is_numeric(num):
    """Checks if the value is an integer"""
    try:
        int(num)
    except ValueError or TypeError:
        return False
    return True
