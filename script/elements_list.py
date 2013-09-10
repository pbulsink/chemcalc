#!/usr/bin/env python
import string
from table_of_exact_masses import TABLE_OF_MASS

_data = r"""'Ac', 'Actinium', 89, 227.03
'Ag', 'Silver', 47, 107.868
'Al', 'Aluminum', 13, 26.98154
'Am', 'Americium', 95, 243.06
'Ar', 'Argon', 18, 39.948
'As', 'Arsenic', 33, 74.9216
'At', 'Astatine', 85, 210
'Au', 'Gold', 79, 196.9665
'B', 'Boron', 5, 10.81
'Ba', 'Barium', 56, 137.33
'Be', 'Beryllium', 4, 9.01218
'Bh', 'Bohrium', 107, 270
'Bi', 'Bismuth', 83, 208.9804
'Bk', 'Berkelium', 97, 247.07
'Br', 'Bromine', 35, 79.904
'C', 'Carbon', 6, 12.011
'Ca', 'Calcium', 20, 40.08
'Cd', 'Cadmium', 48, 112.41
'Ce', 'Cerium', 58, 140.12
'Cf', 'Californium', 98, 251.08
'Cl', 'Chlorine', 17, 35.453
'Cm', 'Curium', 96, 247.07
'Cn', 'Copernicium', 112, 285.17
'Co', 'Cobalt', 27, 58.9332
'Cr', 'Chromium', 24, 51.996
'Cs', 'Cesium', 55, 132.9054
'Cu', 'Copper', 29, 63.546
'Db', 'Dubnium', 105, 268.13
'Ds', 'Darmstadtium', 110, 281.16
'Dy', 'Dysprosium', 66, 162.50
'Er', 'Erbium', 68, 167.26
'Es', 'Einsteinium', 99, 252.08
'Eu', 'Europium', 63, 151.96
'F', 'Fluorine', 9, 18.998403
'Fe', 'Iron', 26, 55.847
'Fl', 'Flerovium', 114, 289.19
'Fm', 'Fermium', 100, 257.10
'Fr', 'Francium', 87, 223.02
'Ga', 'Gallium', 31, 69.735
'Gd', 'Gadolinium', 64, 157.25
'Ge', 'Germanium', 32, 72.59
'H', 'Hydrogen', 1, 1.0079
'He', 'Helium', 2, 4.0026
'Hf', 'Hafnium', 72, 178.49
'Hg', 'Mercury', 80, 200.59
'Ho', 'Holmium', 67, 164.9304
'Hs', 'Hassium', 108, 277.15
'I', 'Iodine', 53, 126.9045
'In', 'Indium', 49, 114.82
'Ir', 'Iridium', 77, 192.22
'K', 'Potassium', 19, 39.0983
'Kr', 'Krypton', 36, 83.80
'La', 'Lanthanum', 57, 138.9055
'Li', 'Lithium', 3, 6.94
'Lr', 'Lawrencium', 103, 260
'Lu', 'Lutetium', 71, 174.96
'Lv', 'Livermorium', 116, 293
'Md', 'Mendelevium', 101, 258.10
'Mg', 'Magnesium', 12, 24.305
'Mn', 'Manganese', 25, 54.9380
'Mo', 'Molybdenum', 42, 95.94
'Mt', 'Meitnerium', 109, 276.15
'N', 'Nitrogen', 7, 14.0067
'Na', 'Sodium', 11, 22.98977
'Nb', 'Niobium', 41, 92.9064
'Nd', 'Neodymium', 60, 144.24
'Ne', 'Neon', 10, 20.17
'Ni', 'Nickel', 28, 58.71
'No', 'Nobelium', 102, 259.10
'Np', 'Neptunium', 93, 237.0482
'O', 'Oxygen', 8, 15.9994
'Os', 'Osmium', 76, 190.2
'P', 'Phosphorous', 15, 30.97376
'Pa', 'Proactinium', 91, 231.0359
'Pb', 'Lead', 82, 207.2
'Pd', 'Palladium', 46, 106.4
'Pm', 'Promethium', 61, 144.91
'Po', 'Polonium', 84, 209
'Pr', 'Praseodymium', 59, 140.9077
'Pt', 'Platinum', 78, 195.09
'Pu', 'Plutonium', 94, 244.06
'Ra', 'Radium', 88, 226.0254
'Rb', 'Rubidium', 37, 85.467
'Re', 'Rhenium', 75, 186.207
'Rf', 'Rutherfordium', 104, 265.12
'Rg', 'Roentgenium', 111, 280.16
'Rh', 'Rhodium', 45, 102.9055
'Rn', 'Radon', 86, 222
'Ru', 'Ruthenium', 44, 101.07
'S', 'Sulfur', 16, 32.06
'Sb', 'Antimony', 51, 121.75
'Sc', 'Scandium', 21, 44.9559
'Se', 'Selenium', 34, 78.96
'Sg', 'Seaborgium', 106, 271.13
'Si', 'Silicon', 14, 28.0855
'Sm', 'Samarium', 62, 150.4
'Sn', 'Tin', 50, 118.69
'Sr', 'Strontium', 38, 87.62
'Ta', 'Tantalum', 73, 180.947
'Tb', 'Terbium', 65, 158.9254
'Tc', 'Technetium', 43, 98.9062
'Te', 'Tellurium', 52, 127.60
'Th', 'Thorium', 90, 232.0381
'Ti', 'Titanium', 22, 47.90
'Tl', 'Thallium', 81, 204.37
'Tm', 'Thulium', 69, 168.9342
'U', 'Uranium', 92, 238.029
'Uuo', 'Ununoctium', 118, 294
'Uup', 'Ununpentium', 115, 288.19
'Uus', 'Ununseptium', 117, 294
'Uut', 'Ununtrium', 113, 284.18
'V', 'Vanadium', 23, 50.9415
'W', 'Tungsten', 74, 183.85
'Xe', 'Xenon', 54, 131.30
'Y', 'Yttrium', 39, 88.9059
'Yb', 'Ytterbium', 70, 173.04
'Zn', 'Zinc', 30, 65.38
'Zr', 'Zirconium', 40, 91.22"""


class Element:
    """Each element is an object"""
    def __init__(self, symbol, name, atomicnumber, molweight):
        self.sym = symbol
        self.name = name
        self.ano = atomicnumber
        self.mw = molweight
        self.has_isotopes = False
        self.isotopes = list()

    def addsyms(self, weight, result):
        result[self.sym] = result.get(self.sym, 0) + weight

    def add_isotopes(self, isotope):
        self.has_isotopes = True
        self.isotopes = isotope

    def get_isotopes(self):
        return self.isotopes

def build_dict(s):
    """Make the element list into a dictionary"""
    answer = {}
    for line in string.split(s, "\n"):
        symbol, name, num, weight = eval(line)
        answer[symbol] = Element(symbol, name, num, weight)
    for key in answer:
        if key in TABLE_OF_MASS:
            answer[key].add_isotopes(TABLE_OF_MASS[key].isotopes)
    return answer


ELEMENTS = build_dict(_data)

for key in ELEMENTS:
    print ELEMENTS[key].sym
    print ELEMENTS[key].isotopes
