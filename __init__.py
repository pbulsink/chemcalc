#!/usr/bin/env python

from flask import Flask
#from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
#app.config.from_object('config')
#db = SQLAlchemy(app)

from chemcalculator_app import views #, models

if __name__ == '__main__':
    app.run()
