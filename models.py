#!/usr/bin/env python

from chemcalculator_app import db

class Plots(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    formula = db.Column(db.String(128), index = True)
    image = db.Column(db.String(16), unique = True)
    isotopes = db.Column(db.String(2048))
    precision = db.Column(db.Integer())


    def __repr__(self):
        return '<Plot %r>' % (self.formula)
