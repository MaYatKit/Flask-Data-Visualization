# -*- encoding: utf-8 -*-

import os

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    CSRF_ENABLED = True
    SECRET_KEY = "77tgFCdrEEdv77554##@3"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '../database.db')

    SQLALCHEMY_BINDS = {
        'rock_roll': 'sqlite:///' + os.path.join(os.path.dirname(__file__), '../rr_database.db'),
        'k-kord': 'sqlite:///' + os.path.join(os.path.dirname(__file__), '../k_kord_Database.db'),
        'reinhardt': 'sqlite:///' + os.path.join(os.path.dirname(__file__), '../rh_database.db'),
    }
