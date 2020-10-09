# -*- encoding: utf-8 -*-
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


class RH_OvenTemperature(db.Model):
    __bind_key__ = 'reinhardt'
    __tablename__ = 'TEMPERATURE'
    rowid = db.Column(db.Integer, primary_key=True)
    Id = db.Column(db.INTEGER)
    Time = db.Column(db.DateTime)
    TEMP = db.Column(db.SMALLINT)

    def __init__(self, Id, Time, TEMP):
        self.Id = Id
        self.Time = Time
        self.TEMP = TEMP

    def __repr__(self):
        return str(self.Id) + ' - ' + str(self.Time) + ' - ' + str(self.TEMP)

    def save(self):
        # inject self into db session
        db.session.add(self)

        # commit change and save the object
        db.session.commit()

        return self


class RH_Common_Recipe(db.Model):
    __bind_key__ = 'reinhardt'
    __tablename__ = 'COMMAN_RECEIPE'
    rowid = db.Column(db.Integer, primary_key=True)
    # field_name = db.Column(db.String(64))
    # arm_speed = db.Column(db.SMALLINT)
    # clock_rotation = db.Column(db.SMALLINT)
    heat1 = db.Column(db.SMALLINT)
    # heat2 = db.Column(db.SMALLINT)
    # heat3 = db.Column(db.SMALLINT)
    # heat4 = db.Column(db.SMALLINT)
    # heat5 = db.Column(db.SMALLINT)
    mould_speed = db.Column(db.SMALLINT)
    receipe_no = db.Column(db.SMALLINT)
    set_temp_1 = db.Column(db.SMALLINT)

    # set_temp_2 = db.Column(db.SMALLINT)
    # set_temp_3 = db.Column(db.SMALLINT)
    # set_temp_4 = db.Column(db.SMALLINT)
    # set_temp_5 = db.Column(db.SMALLINT)
    # anti_clok_rotation = db.Column(db.SMALLINT)
    # delay_arm_rotation = db.Column(db.SMALLINT)
    # delay_internal_air_heating_time = db.Column(db.SMALLINT)
    # internal_air_air_heating_time = db.Column(db.SMALLINT)
    # stop_after_1 = db.Column(db.SMALLINT)
    # stop_after_2 = db.Column(db.SMALLINT)
    # stop_after_3 = db.Column(db.SMALLINT)
    # stop_for_1 = db.Column(db.SMALLINT)
    # stop_for_2 = db.Column(db.SMALLINT)
    # stop_for_3 = db.Column(db.SMALLINT)
    # delay_starting_bower = db.Column(db.SMALLINT)
    # blower_time_cool = db.Column(db.SMALLINT)
    # delay_time_cool = db.Column(db.SMALLINT)
    # mist_on = db.Column(db.SMALLINT)
    # mist_off = db.Column(db.SMALLINT)
    # initial_temperature = db.Column(db.SMALLINT)
    # factor = db.Column(db.SMALLINT)
    # alarm_for_removing_insert = db.Column(db.SMALLINT)
    # delay_internal_air_cool = db.Column(db.SMALLINT)
    # internal_air_cool = db.Column(db.SMALLINT)
    # delay_internal_air_gas_cool = db.Column(db.SMALLINT)
    # internal_air_gas_cool = db.Column(db.SMALLINT)
    # mould_temp_set_point = db.Column(db.SMALLINT)
    # temperature_to_start_internal_air_heating = db.Column(db.SMALLINT)
    # temperature_to_stop_internal_air_heating = db.Column(db.SMALLINT)
    # temperature_to_start_internal_gas_heating = db.Column(db.SMALLINT)
    # temperature_to_stop_internal_gas_heating = db.Column(db.SMALLINT)
    # sandwitch_temperature_set_point = db.Column(db.SMALLINT)
    # temperature_to_start_blower = db.Column(db.SMALLINT)
    # temperature_to_stop_blower = db.Column(db.SMALLINT)
    # temperature_to_start_mist = db.Column(db.SMALLINT)
    # temperature_to_stop_mist = db.Column(db.SMALLINT)
    # temperature_to_start_internal_air_cooling = db.Column(db.SMALLINT)
    # temperature_to_stop_internal_air_cooling = db.Column(db.SMALLINT)
    # temperature_to_start_internal_gas_cooling = db.Column(db.SMALLINT)
    # temperature_to_stop_internal_gas_cooling1 = db.Column(db.SMALLINT)
    # time_temp = db.Column(db.SMALLINT)
    # delay_internal_gas_heating_time = db.Column(db.SMALLINT)
    # internal_gas_heating_time = db.Column(db.SMALLINT)

    def __init__(self, RECEIPE_NO, SET_TEMP_1, MOULD_SPEED, HEAT1):
        self.receipe_no = RECEIPE_NO
        self.set_temp_1 = SET_TEMP_1
        self.mould_speed = MOULD_SPEED
        self.heat1 = HEAT1

    def __repr__(self):
        return str(self.receipe_no) + ' - ' + str(self.set_temp_1) + ' - ' + str(self.mould_speed) + ' - ' + str(
            self.heat1)

    def save(self):
        # inject self into db session
        db.session.add(self)

        # commit change and save the object
        db.session.commit()

        return self


class RH_ARM1_PRODUCTION(db.Model):
    __bind_key__ = 'reinhardt'
    __tablename__ = 'ARM_1_PRODUCTION'
    rowid = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.SMALLINT)
    time = db.Column(db.String(120))
    receipe_no = db.Column(db.SMALLINT)
    sandwich_time = db.Column(db.SMALLINT)
    arm_num = db.Column(db.SMALLINT)

    def __init__(self, Id, Time, RECEIPE_NO, Sandwich_Time, Arm_num):
        self.id = Id
        self.time = Time
        self.receipe_no = RECEIPE_NO
        self.sandwich_time = Sandwich_Time
        self.arm_num = Arm_num

    def __repr__(self):
        return str(self.id) + ' - ' + str(self.time) + ' - ' + str(self.receipe_no) + ' - ' + str(
            self.sandwich_time) + ' - ' + str(self.arm_num)

    def save(self):
        # inject self into db session
        db.session.add(self)

        # commit change and save the object
        db.session.commit()

        return self


class RH_ARM2_PRODUCTION(db.Model):
    __bind_key__ = 'reinhardt'
    __tablename__ = 'ARM_2_PRODUCTION'
    rowid = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.SMALLINT)
    time = db.Column(db.String(120))
    receipe_no = db.Column(db.SMALLINT)
    sandwich_time = db.Column(db.SMALLINT)
    arm_num = db.Column(db.SMALLINT)

    def __init__(self, Id, Time, RECEIPE_NO, Sandwich_Time, Arm_num):
        self.id = Id
        self.time = Time
        self.receipe_no = RECEIPE_NO
        self.sandwich_time = Sandwich_Time
        self.arm_num = Arm_num

    def __repr__(self):
        return str(self.id) + ' - ' + str(self.time) + ' - ' + str(self.receipe_no) + ' - ' + str(
            self.sandwich_time) + ' - ' + str(self.arm_num)

    def save(self):
        # inject self into db session
        db.session.add(self)

        # commit change and save the object
        db.session.commit()

        return self


class RH_ARM3_PRODUCTION(db.Model):
    __bind_key__ = 'reinhardt'
    __tablename__ = 'ARM_3_PRODUCTION'
    rowid = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.SMALLINT)
    time = db.Column(db.String(120))
    receipe_no = db.Column(db.SMALLINT)
    sandwich_time = db.Column(db.SMALLINT)
    arm_num = db.Column(db.SMALLINT)

    def __init__(self, Id, Time, RECEIPE_NO, Sandwich_Time, Arm_num):
        self.id = Id
        self.time = Time
        self.receipe_no = RECEIPE_NO
        self.sandwich_time = Sandwich_Time
        self.arm_num = Arm_num

    def __repr__(self):
        return str(self.id) + ' - ' + str(self.time) + ' - ' + str(self.receipe_no) + ' - ' + str(
            self.sandwich_time) + ' - ' + str(self.arm_num)

    def save(self):
        # inject self into db session
        db.session.add(self)

        # commit change and save the object
        db.session.commit()

        return self


class RH_ARM4_PRODUCTION(db.Model):
    __bind_key__ = 'reinhardt'
    __tablename__ = 'ARM_4_PRODUCTION'
    rowid = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.SMALLINT)
    time = db.Column(db.String(120))
    receipe_no = db.Column(db.SMALLINT)
    sandwich_time = db.Column(db.SMALLINT)
    arm_num = db.Column(db.SMALLINT)

    def __init__(self, Id, Time, RECEIPE_NO, Sandwich_Time, Arm_num):
        self.id = Id
        self.time = Time
        self.receipe_no = RECEIPE_NO
        self.sandwich_time = Sandwich_Time
        self.arm_num = Arm_num

    def __repr__(self):
        return str(self.id) + ' - ' + str(self.time) + ' - ' + str(self.receipe_no) + ' - ' + str(
            self.sandwich_time) + ' - ' + str(self.arm_num)

    def save(self):
        # inject self into db session
        db.session.add(self)

        # commit change and save the object
        db.session.commit()

        return self


class RH_OvenDelay(db.Model):
    __bind_key__ = 'reinhardt'
    __tablename__ = 'DELAY'
    rowid = db.Column(db.Integer, primary_key=True)
    Id = db.Column(db.INTEGER)
    Time = db.Column(db.String(120))
    Arm_no = db.Column(db.Integer)
    Delay_time = db.Column(db.Float)
    Receipe_no = db.Column(db.Integer)

    def __init__(self, Id, Time, Arm_no, Delay_time, Receipe_no):
        self.Id = Id
        self.Time = Time
        self.Arm_no = Arm_no
        self.Delay_time = Delay_time
        self.Receipe_no = Receipe_no

    def __repr__(self):
        return str(self.Id) + ' - ' + str(self.Time) + ' - ' + str(self.Arm_no) + ' - ' + str(
            self.Delay_time) + ' - ' + str(self.Receipe_no)

    def save(self):
        # inject self into db session
        db.session.add(self)

        # commit change and save the object
        db.session.commit()

        return self


class ARM_One(db.Model):
    __bind_key__ = 'k-kord'
    __tablename__ = 'arm1'
    rowid = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(64))
    date = db.Column(db.String(64))
    iat = db.Column(db.Integer)
    mwt = db.Column(db.Integer)
    amb = db.Column(db.Integer)

    def __init__(self, time, date, iat, mwt, amb):
        self.time = time
        self.date = date
        self.iat = iat
        self.mwt = mwt
        self.amb = amb

    def __repr__(self):
        return str(self.time) + ' - ' + str(self.date) + ' - ' + str(self.iat) + ' - ' + str(
            self.mwt) + ' - ' + str(self.amb)

    def save(self):
        # inject self into db session
        db.session.add(self)

        # commit change and save the object
        db.session.commit()

        return self


class ARM_Two(db.Model):
    __bind_key__ = 'k-kord'
    __tablename__ = 'arm2'
    rowid = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(64))
    date = db.Column(db.String(64))
    iat = db.Column(db.Integer)
    mwt = db.Column(db.Integer)
    amb = db.Column(db.Integer)

    def __init__(self, time, date, iat, mwt, amb):
        self.time = time
        self.date = date
        self.iat = iat
        self.mwt = mwt
        self.amb = amb

    def __repr__(self):
        return str(self.time) + ' - ' + str(self.date) + ' - ' + str(self.iat) + ' - ' + str(
            self.mwt) + ' - ' + str(self.amb)

    def save(self):
        # inject self into db session
        db.session.add(self)

        # commit change and save the object
        db.session.commit()

        return self


class ARM_Three(db.Model):
    __bind_key__ = 'k-kord'
    __tablename__ = 'arm3'
    rowid = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(64))
    date = db.Column(db.String(64))
    iat = db.Column(db.Integer)
    mwt = db.Column(db.Integer)
    amb = db.Column(db.Integer)

    def __init__(self, time, date, iat, mwt, amb):
        self.time = time
        self.date = date
        self.iat = iat
        self.mwt = mwt
        self.amb = amb

    def __repr__(self):
        return str(self.time) + ' - ' + str(self.date) + ' - ' + str(self.iat) + ' - ' + str(
            self.mwt) + ' - ' + str(self.amb)

    def save(self):
        # inject self into db session
        db.session.add(self)

        # commit change and save the object
        db.session.commit()

        return self


class ARM_Four(db.Model):
    __bind_key__ = 'k-kord'
    __tablename__ = 'arm4'
    rowid = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(64))
    date = db.Column(db.String(64))
    iat = db.Column(db.Integer)
    mwt = db.Column(db.Integer)
    amb = db.Column(db.Integer)

    def __init__(self, time, date, iat, mwt, amb):
        self.time = time
        self.date = date
        self.iat = iat
        self.mwt = mwt
        self.amb = amb

    def __repr__(self):
        return str(self.time) + ' - ' + str(self.date) + ' - ' + str(self.iat) + ' - ' + str(
            self.mwt) + ' - ' + str(self.amb)

    def save(self):
        # inject self into db session
        db.session.add(self)

        # commit change and save the object
        db.session.commit()

        return self


class Latest_Script_Parameter(db.Model):
    __bind_key__ = 'k-kord'
    __tablename__ = 'Latest_Script_Parameter'
    rowid = db.Column(db.Integer, primary_key=True)
    last_xls_arm1 = db.Column(db.Integer)
    last_xls_arm2 = db.Column(db.Integer)
    last_xls_arm3 = db.Column(db.Integer)
    last_xls_arm4 = db.Column(db.Integer)

    def __init__(self, last_xls_arm1, last_xls_arm2, last_xls_arm3, last_xls_arm4):
        self.last_xls_arm1 = last_xls_arm1
        self.last_xls_arm2 = last_xls_arm2
        self.last_xls_arm3 = last_xls_arm3
        self.last_xls_arm4 = last_xls_arm4

    def __repr__(self):
        return str(self.last_xls_arm1) + ' - ' + str(self.last_xls_arm2) + ' - ' + str(
            self.last_xls_arm3) + ' - ' + str(self.last_xls_arm4)

    def save(self):
        # inject self into db session
        db.session.add(self)

        # commit change and save the object
        db.session.commit()

        return self
