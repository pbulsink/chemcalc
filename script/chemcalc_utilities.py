#!/usr/bin/env python
import hmac
import string
from matplotlib import pyplot as plt
from parse import parse  # Import the parser
from elements_list import ELEMENTS

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
    Return true/false if string is float number
    """
    try:
        float(s)
        return True
    except ValueError:
        return False


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
        error = error + "Not a valid Formula"
    except:
        error = error + "Unknown Error. "
    return valid_formula, error


def shorten_formula(formula):
    """
    Take a 'parsed formula' style formula and return a compact elemental
    formula. IE CH3CH2CH2CH3 --> [["C":4],["H":10]] --> C4H10
    """
    fdict = dict((x[0], x[1]) for x in formula)
    short_formula = ""
    if "C" in fdict:
        short_formula = short_formula + "C"
        if fdict["C"] > 1:
            short_formula = short_formula + str(fdict["C"])
        del fdict["C"]
    if "H" in fdict:
        short_formula = short_formula + "H"
        if fdict["H"] > 1:
            short_formula = short_formula + str(fdict["H"])
        del fdict["H"]
    if fdict:
        flist = list()
        for key in fdict:
            flist.append([key, fdict[key]])
        flist.sort()
        for e in flist:
            short_formula = short_formula + e[0]
            if e[1] > 1:
                short_formula = short_formula + str(e[1])
    return short_formula


def isotope_distribute(formula):
    e_formula = list()
    precision = 0.000001
    for e in formula:
        for f in range(0, e[1]):
            e_formula.append(e[0])
    molecule = list()
    molecule.append([0,1.0])
    for a in e_formula:
        next_mol = list()
        for m in molecule:
            for i in ELEMENTS[a].isotopes:
                next_mol.append([i[1]+m[0], (i[2]/100)*m[1]])
        mol = dict()
        for n in next_mol:
            if n[0] not in mol:
                mol[n[0]]=n[1]
            else:
                mol[n[0]]=mol[n[0]]+n[1]

        molecule = list()
        for key, value in mol.iteritems():
            molecule.append([key, value])

        molecule.sort()
        maximum = 0.0
        for m in molecule:
            m = list(m)
            if m[1]>maximum:
                maximum = m[1]
        for m in molecule:
            m[1]=m[1]/maximum
        molecule = [mol for mol in molecule if mol[1] > precision]
    return molecule


def listofzero(y):
    return [0]*len(y)


def plot_isotopes(isotopes):
    x = list()
    y = list()
    for i in isotopes:
        x.append(i[0])
        y.append(i[1])
    
    xmin = x[0] - x[0] * 0.005
    xmax = x[-1] + x[-1] * 0.005
    
    plt.figure()
    plt.vlines(x, [0], y)
    plt.title('Isotopes: {}'.format(shorten_formula(formula)))
    plt.ylim(0, 1.1)
    plt.xlim(xmin, xmax)

    xmin2, xmax2 = plt.xlim()
    return plt
    
