# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from app import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(500))

    def __init__(self, user, email, password):
        self.user = user
        self.password = password
        self.email = email

    def __repr__(self):
        return str(self.id) + ' - ' + str(self.user)

    def save(self):
        # inject self into db session
        db.session.add(self)

        # commit change and save the object
        db.session.commit()

        return self


class OvenTemp(db.Model):
    __bind_key__ = 'rock_roll'
    __tablename__ = 'Oven_Temperature_PV'
    rowid = db.Column(db.Integer, primary_key=True)
    VAR_NAME = db.Column(db.String(64))
    TIME_STRING = db.Column(db.String(120))
    VAR_VALUE = db.Column(db.Float)
    VALIDITY = db.Column(db.Integer)
    TIME_MS = db.Column(db.Integer)

    def __init__(self, name, time, value, validity, time_mill):
        self.VAR_NAME = name
        self.TIME_STRING = time
        self.VAR_VALUE = value
        self.VALIDITY = validity
        self.TIME_MS = time_mill

    def __repr__(self):
        return str(self.rowid) + ' - ' + str(self.VAR_NAME) + ' - ' + str(self.TIME_STRING) + ' - ' + str(
            self.VAR_VALUE) + ' - ' + str(
            self.VALIDITY) + ' - ' + str(self.TIME_MS)

    def save(self):
        # inject self into db session
        db.session.add(self)

        # commit change and save the object
        db.session.commit()

        return self


class MouldTemp(db.Model):
    __bind_key__ = 'rock_roll'
    __tablename__ = 'Mould_Temperature_PV'
    rowid = db.Column(db.Integer, primary_key=True)
    VAR_NAME = db.Column(db.String(64))
    TIME_STRING = db.Column(db.String(120))
    VAR_VALUE = db.Column(db.Float)
    VALIDITY = db.Column(db.Integer)
    TIME_MS = db.Column(db.Integer)

    def __init__(self, name, time, value, validity, time_mill):
        self.VAR_NAME = name
        self.TIME_STRING = time
        self.VAR_VALUE = value
        self.VALIDITY = validity
        self.TIME_MS = time_mill

    def __repr__(self):
        return str(self.id) + ' - ' + str(self.name) + ' - ' + str(self.time) + ' - ' + str(self.value) + ' - ' + str(
            self.validity) + ' - ' + str(self.time_mill)

    def save(self):
        # inject self into db session
        db.session.add(self)

        # commit change and save the object
        db.session.commit()

        return self


class CoolingTemp(db.Model):
    __bind_key__ = 'rock_roll'
    __tablename__ = 'Cooling_Temperature_PV'
    rowid = db.Column(db.Integer, primary_key=True)
    VAR_NAME = db.Column(db.String(64))
    TIME_STRING = db.Column(db.String(120))
    VAR_VALUE = db.Column(db.Float)
    VALIDITY = db.Column(db.Integer)
    TIME_MS = db.Column(db.Integer)

    def __init__(self, name, time, value, validity, time_mill):
        self.VAR_NAME = name
        self.TIME_STRING = time
        self.VAR_VALUE = value
        self.VALIDITY = validity
        self.TIME_MS = time_mill

    def __repr__(self):
        return str(self.id) + ' - ' + str(self.name) + ' - ' + str(self.time) + ' - ' + str(self.value) + ' - ' + str(
            self.validity) + ' - ' + str(self.time_mill)

    def save(self):
        # inject self into db session
        db.session.add(self)

        # commit change and save the object
        db.session.commit()

        return self


class RockAngle(db.Model):
    __bind_key__ = 'rock_roll'
    __tablename__ = 'Rock_Angle_PV'
    rowid = db.Column(db.Integer, primary_key=True)
    VAR_NAME = db.Column(db.String(64))
    TIME_STRING = db.Column(db.String(120))
    VAR_VALUE = db.Column(db.Float)
    VALIDITY = db.Column(db.Integer)
    TIME_MS = db.Column(db.Integer)

    def __init__(self, name, time, value, validity, time_mill):
        self.VAR_NAME = name
        self.TIME_STRING = time
        self.VAR_VALUE = value
        self.VALIDITY = validity
        self.TIME_MS = time_mill

    def __repr__(self):
        return str(self.id) + ' - ' + str(self.name) + ' - ' + str(self.time) + ' - ' + str(self.value) + ' - ' + str(
            self.validity) + ' - ' + str(self.time_mill)

    def save(self):
        # inject self into db session
        db.session.add(self)

        # commit change and save the object
        db.session.commit()

        return self


class RollAngle(db.Model):
    __bind_key__ = 'rock_roll'
    __tablename__ = 'Roll_Angle_PV'
    rowid = db.Column(db.Integer, primary_key=True)
    VAR_NAME = db.Column(db.String(64))
    TIME_STRING = db.Column(db.String(120))
    VAR_VALUE = db.Column(db.Float)
    VALIDITY = db.Column(db.Integer)
    TIME_MS = db.Column(db.Integer)

    def __init__(self, name, time, value, validity, time_mill):
        self.VAR_NAME = name
        self.TIME_STRING = time
        self.VAR_VALUE = value
        self.VALIDITY = validity
        self.TIME_MS = time_mill

    def __repr__(self):
        return str(self.id) + ' - ' + str(self.name) + ' - ' + str(self.time) + ' - ' + str(self.value) + ' - ' + str(
            self.validity) + ' - ' + str(self.time_mill)

    def save(self):
        # inject self into db session
        db.session.add(self)

        # commit change and save the object
        db.session.commit()

        return self


class CoolRotationOn(db.Model):
    __bind_key__ = 'rock_roll'
    __tablename__ = 'ioCoolRotationOn'
    rowid = db.Column(db.Integer, primary_key=True)
    VAR_NAME = db.Column(db.String(64))
    TIME_STRING = db.Column(db.String(120))
    VAR_VALUE = db.Column(db.Float)
    VALIDITY = db.Column(db.Integer)
    TIME_MS = db.Column(db.Integer)

    def __init__(self, name, time, value, validity, time_mill):
        self.VAR_NAME = name
        self.TIME_STRING = time
        self.VAR_VALUE = value
        self.VALIDITY = validity
        self.TIME_MS = time_mill

    def __repr__(self):
        return str(self.id) + ' - ' + str(self.name) + ' - ' + str(self.time) + ' - ' + str(self.value) + ' - ' + str(
            self.validity) + ' - ' + str(self.time_mill)

    def save(self):
        # inject self into db session
        db.session.add(self)

        # commit change and save the object
        db.session.commit()

        return self


class CoolFanStart(db.Model):
    __bind_key__ = 'rock_roll'
    __tablename__ = 'io_CoolingFansStart'
    rowid = db.Column(db.Integer, primary_key=True)
    VAR_NAME = db.Column(db.String(64))
    TIME_STRING = db.Column(db.String(120))
    VAR_VALUE = db.Column(db.Float)
    VALIDITY = db.Column(db.Integer)
    TIME_MS = db.Column(db.Integer)

    def __init__(self, name, time, value, validity, time_mill):
        self.VAR_NAME = name
        self.TIME_STRING = time
        self.VAR_VALUE = value
        self.VALIDITY = validity
        self.TIME_MS = time_mill

    def __repr__(self):
        return str(self.id) + ' - ' + str(self.name) + ' - ' + str(self.time) + ' - ' + str(self.value) + ' - ' + str(
            self.validity) + ' - ' + str(self.time_mill)

    def save(self):
        # inject self into db session
        db.session.add(self)

        # commit change and save the object
        db.session.commit()

        return self


class OvenDoor(db.Model):
    __bind_key__ = 'rock_roll'
    __tablename__ = 'ioOvenDoorLs'
    rowid = db.Column(db.Integer, primary_key=True)
    VAR_NAME = db.Column(db.String(64))
    TIME_STRING = db.Column(db.String(120))
    VAR_VALUE = db.Column(db.Float)
    VALIDITY = db.Column(db.Integer)
    TIME_MS = db.Column(db.Integer)

    def __init__(self, name, time, value, validity, time_mill):
        self.VAR_NAME = name
        self.TIME_STRING = time
        self.VAR_VALUE = value
        self.VALIDITY = validity
        self.TIME_MS = time_mill

    def __repr__(self):
        return str(self.id) + ' - ' + str(self.name) + ' - ' + str(self.time) + ' - ' + str(self.value) + ' - ' + str(
            self.validity) + ' - ' + str(self.time_mill)

    def save(self):
        # inject self into db session
        db.session.add(self)

        # commit change and save the object
        db.session.commit()

        return self


class RecipeNumber(db.Model):
    __bind_key__ = 'rock_roll'
    __tablename__ = 'rcpRecipeNumber'
    rowid = db.Column(db.Integer, primary_key=True)
    VAR_NAME = db.Column(db.String(64))
    TIME_STRING = db.Column(db.String(120))
    VAR_VALUE = db.Column(db.Float)
    VALIDITY = db.Column(db.Integer)
    TIME_MS = db.Column(db.Integer)

    def __init__(self, name, time, value, validity, time_mill):
        self.VAR_NAME = name
        self.TIME_STRING = time
        self.VAR_VALUE = value
        self.VALIDITY = validity
        self.TIME_MS = time_mill

    def __repr__(self):
        return str(self.id) + ' - ' + str(self.name) + ' - ' + str(self.time) + ' - ' + str(self.value) + ' - ' + str(
            self.validity) + ' - ' + str(self.time_mill)

    def save(self):
        # inject self into db session
        db.session.add(self)

        # commit change and save the object
        db.session.commit()

        return self