# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

# Python modules
import os
import operator
import time
import datetime

# Flask modules
from flask import render_template, request, url_for, redirect, send_from_directory
from flask_login import login_user, logout_user, current_user

# App modules
from app import app, lm, db
from app.forms import LoginForm, RegisterForm
from app.models import User, OvenTemp, MouldTemp, CoolingTemp, RockAngle, RollAngle, RecipeNumber, OvenDoor

from sqlalchemy import Column, String, Integer, text
import json

CoolingTempMax = 200
CoolingTempMin = 0
MouldTempMax = 200
MouldTempMin = 20
OvenTempMax = 400
OvenTempMin = 0


# provide login manager with load_user callback
@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Logout user
@app.route('/logout.html')
def logout():
    logout_user()
    return redirect(url_for('login'))


# Register a new user
@app.route('/register.html', methods=['GET', 'POST'])
def register():
    # declare the Registration Form
    form = RegisterForm(request.form)

    msg = None

    if request.method == 'GET':
        return render_template('pages/register.html', form=form, msg=msg)

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str)
        email = request.form.get('email', '', type=str)

        # filter User out of database through username
        user = User.query.filter_by(user=username).first()

        # filter User out of database through username
        user_by_email = User.query.filter_by(email=email).first()

        if user or user_by_email:
            msg = 'Error: User exists!'

        else:

            pw_hash = password  # bc.generate_password_hash(password)

            user = User(username, email, pw_hash)

            user.save()

            msg = 'User created, please <a href="' + url_for('login') + '">login</a>'

    else:
        msg = 'Input error'

    return render_template('pages/register.html', form=form, msg=msg)


# Authenticate user
@app.route('/login.html', methods=['GET', 'POST'])
def login():
    # Declare the login form
    form = LoginForm(request.form)

    # Flask message injected into the page, in case of any errors
    msg = None

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str)

        # filter User out of database through username
        user = User.query.filter_by(user=username).first()

        if user:

            # if bc.check_password_hash(user.password, password):
            if user.password == password:
                login_user(user)
                return redirect(url_for('rock_roll_page'))
            else:
                msg = "Wrong password. Please try again."
        else:
            msg = "Unknown user"

    return render_template('pages/login.html', form=form, msg=msg)


# App main route + generic routing
# @app.route('/', defaults={'path': 'index.html'})
# @app.route('/<path>')
def index(path):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    content = None

    try:

        # try to match the pages defined in -> pages/<input file>
        return render_template('pages/' + path)

    except:
        return render_template('pages/error-404.html')


# Return sitemap
@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'sitemap.xml')


# Rock & Roll page
@app.route('/', defaults={'path': 'rock_roll_charts.html'})
@app.route('/<path>')
@app.route('/rock_roll_charts.html', methods=['GET', 'POST'], defaults={'path': 'rock_roll_charts.html'})
def rock_roll_page(path):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    if path != 'rock_roll_charts.html' and path != '':
        try:
            # try to match the pages defined in -> pages/<input file>
            return render_template('pages/' + path)
        except:
            return render_template('pages/error-404.html')

    # column names
    names = []
    dates = []
    values = []
    validities = []
    mills = []

    # -------Oven_Temperature_PV--------
    latest = OvenTemp.query.order_by(OvenTemp.rowid.desc()).first()  # Read the latest line in the table
    latest_time = latest.TIME_STRING
    latest_day = latest_time.split(" ")[0]  # Get the latest day
    search = "%{}%".format(latest_day)
    ot_all = OvenTemp.query.filter(OvenTemp.TIME_STRING.like(search)).all()

    # read all data on the latest day
    for each in ot_all:
        # print(ot_each)
        names.append(each.VAR_NAME)
        dates.append(each.TIME_STRING)
        values.append(each.VAR_VALUE)
        validities.append(each.VALIDITY)
        mills.append(each.TIME_MS)

    ot_names_str = '_'.join(names)
    ot_dates_str = '_'.join(dates)
    ot_values_str = '_'.join(str(e) for e in values)  # Convert float to str
    ot_validities_str = '_'.join(str(e) for e in validities)  # Convert float to str
    ot_mills_str = '_'.join(str(e) for e in mills)  # Convert float to str

    # --------Mould_Temperature_PV-------
    latest = MouldTemp.query.order_by(MouldTemp.rowid.desc()).first()  # Read the latest line in the table
    latest_time = latest.TIME_STRING
    latest_day = latest_time.split(" ")[0]  # Get the latest day
    search = "%{}%".format(latest_day)
    mt_all = MouldTemp.query.filter(MouldTemp.TIME_STRING.like(search)).all()

    # column names
    names.clear()
    mt_dates = []
    mt_values = []
    validities.clear()
    mills.clear()

    # read all data on the latest day
    for each in mt_all:
        # print(mt_each)
        names.append(each.VAR_NAME)
        mt_dates.append(each.TIME_STRING)
        mt_values.append(each.VAR_VALUE)
        validities.append(each.VALIDITY)
        mills.append(each.TIME_MS)

    mt_names_str = '_'.join(names)
    mt_dates_str = '_'.join(mt_dates)
    mt_values_str = '_'.join(str(e) for e in mt_values)  # Convert float to str
    mt_validities_str = '_'.join(str(e) for e in validities)  # Convert float to str
    mt_mills_str = '_'.join(str(e) for e in mills)  # Convert float to str

    # -------Cooling_Temperature_PV--------
    latest = CoolingTemp.query.order_by(CoolingTemp.rowid.desc()).first()  # Read the latest line in the table
    latest_time = latest.TIME_STRING
    latest_day = latest_time.split(" ")[0]  # Get the latest day
    search = "%{}%".format(latest_day)
    ct_all = CoolingTemp.query.filter(CoolingTemp.TIME_STRING.like(search)).all()

    # column names
    names.clear()
    dates.clear()
    values = []
    validities = []
    mills = []

    # read all data on the latest day
    for each in ct_all:
        # print(mt_each)
        names.append(each.VAR_NAME)
        dates.append(each.TIME_STRING)
        values.append(each.VAR_VALUE)
        validities.append(each.VALIDITY)
        mills.append(each.TIME_MS)

    ct_names_str = '_'.join(names)
    ct_dates_str = '_'.join(dates)
    ct_values_str = '_'.join(str(e) for e in values)  # Convert float to str
    ct_validities_str = '_'.join(str(e) for e in validities)  # Convert float to str
    ct_mills_str = '_'.join(str(e) for e in mills)  # Convert float to str

    # ----------------Rock_Angle_PV------------------
    latest = RockAngle.query.order_by(RockAngle.rowid.desc()).first()  # Read the latest line in the table
    latest_time = latest.TIME_STRING
    latest_day = latest_time.split(" ")[0]  # Get the latest day
    search = "%{}%".format(latest_day)
    rock_a_all = RockAngle.query.filter(RockAngle.TIME_STRING.like(search)).all()

    # column names
    names.clear()
    dates.clear()
    values.clear()
    validities.clear()
    mills.clear()

    # read all data on the latest day
    for each in rock_a_all:
        # print(mt_each)
        names.append(each.VAR_NAME)
        dates.append(each.TIME_STRING)
        values.append(each.VAR_VALUE)
        validities.append(each.VALIDITY)
        mills.append(each.TIME_MS)

    rock_a_names_str = '_'.join(names)
    rock_a_dates_str = '_'.join(dates)
    rock_a_values_str = '_'.join(str(e) for e in values)  # Convert float to str
    rock_a_validities_str = '_'.join(str(e) for e in validities)  # Convert float to str
    rock_a_mills_str = '_'.join(str(e) for e in mills)  # Convert float to str

    # ----------------Roll_Angle_PV-----------------
    latest = RollAngle.query.order_by(RollAngle.rowid.desc()).first()  # Read the latest line in the table
    latest_time = latest.TIME_STRING
    latest_day = latest_time.split(" ")[0]  # Get the latest day
    search = "%{}%".format(latest_day)
    roll_a_all = RollAngle.query.filter(RollAngle.TIME_STRING.like(search)).all()

    # column names
    names.clear()
    dates.clear()
    values.clear()
    validities.clear()
    mills.clear()

    # read all data on the latest day
    for each in roll_a_all:
        # print(mt_each)
        names.append(each.VAR_NAME)
        dates.append(each.TIME_STRING)
        values.append(each.VAR_VALUE)
        validities.append(each.VALIDITY)
        mills.append(each.TIME_MS)

    roll_a_names_str = '_'.join(names)
    roll_a_dates_str = '_'.join(dates)
    roll_a_values_str = '_'.join(str(e) for e in values)  # Convert float to str
    roll_a_validities_str = '_'.join(str(e) for e in validities)  # Convert float to str
    roll_a_mills_str = '_'.join(str(e) for e in mills)  # Convert float to str

    recipes = RecipeNumber.query.filter(RecipeNumber.TIME_STRING.like(search)).all()
    # Save time intervals between target recipe and next recipe
    recipe_map_map = {}

    # recipe numbers ----> recipe intervals ----> start time and end time
    for i in range(len(recipes)):
        if recipes[i].VAR_VALUE not in recipe_map_map:
            recipe_map = {}
            start_time = recipes[i].TIME_STRING.split(" ")[1]
            time_stamp = transform_date_timestamp(start_time)
            if i == len(recipes) - 1:
                recipe_map[time_stamp] = 1000000000000
            else:
                start_time2 = recipes[i + 1].TIME_STRING.split(" ")[1]
                time_stamp2 = transform_date_timestamp(start_time2)
                recipe_map[time_stamp] = time_stamp2
            recipe_map_map[recipes[i].VAR_VALUE] = recipe_map
        else:
            recipe_map = recipe_map_map[recipes[i].VAR_VALUE]
            start_time = recipes[i].TIME_STRING.split(" ")[1]
            time_stamp = transform_date_timestamp(start_time)
            if i == len(recipes) - 1:
                recipe_map[time_stamp] = 1000000000000
            else:
                start_time2 = recipes[i + 1].TIME_STRING.split(" ")[1]
                time_stamp2 = transform_date_timestamp(start_time2)
                recipe_map[time_stamp] = time_stamp2

    # Count recipes which is set in last day
    lastday_recipes = RecipeNumber.query.filter(RecipeNumber.rowid.like(recipes[0].rowid - 1)).all()
    if len(lastday_recipes) != 0:
        if lastday_recipes[0].VAR_VALUE not in recipe_map_map:
            recipe_map = {}
            start_time = recipes[0].TIME_STRING.split(" ")[1]
            time_stamp = transform_date_timestamp(start_time)
            recipe_map[0] = time_stamp
            recipe_map_map[lastday_recipes[0].VAR_VALUE] = recipe_map
        else:
            recipe_map = recipe_map_map[lastday_recipes[0].VAR_VALUE]
            start_time = recipes[0].TIME_STRING.split(" ")[1]
            time_stamp = transform_date_timestamp(start_time)
            recipe_map[0] = time_stamp

    # Save all door operations on that day
    # door_opens = OvenDoor.query.filter(OvenDoor.TIME_STRING.like(search)).all()

    label_points = []
    labels = []
    for label in recipe_map_map:
        for start_time in recipe_map_map[label]:
            # Count how many door operations in the recipe operation intervals
            # should_has = 0
            # for each in door_opens:
            #     if each.VAR_VALUE == 1.0:
            #         time_stamp = transform_date_timestamp(each.TIME_STRING.split(" ")[1])
            #         if start_time < time_stamp < recipe_map_map[label][start_time]:
            #             should_has = should_has + 1
            # count = 0
            for i in range(1, len(mt_values)):  # from 1 instead of 0
                if mt_values[i - 1] < 20 and mt_values[i] > 20:  # 20 is the least value to plot
                    if start_time < transform_date_timestamp(mt_dates[i].split(" ")[1]) < recipe_map_map[label][
                        start_time]:
                        label_points.append(str(i))
                        labels.append(str(label))
                        # count = count + 1
                        # break

    label_points_str = "_".join(label_points)
    labels_str = "_".join(labels)

    return render_template('pages/rock_roll_charts.html', ot_names=ot_names_str
                           , ot_dates=ot_dates_str, ot_values=ot_values_str,
                           ot_validities=ot_validities_str, ot_mills=ot_mills_str,
                           mt_names=mt_names_str, mt_dates=mt_dates_str,
                           mt_values=mt_values_str, mt_validities=mt_validities_str,
                           mt_mills=mt_mills_str, ct_names=ct_names_str,
                           ct_dates=ct_dates_str, ct_values=ct_values_str,
                           ct_validities=ct_validities_str, ct_mills=ct_mills_str,
                           rock_a_names=rock_a_names_str, rock_a_dates=rock_a_dates_str,
                           rock_a_values=rock_a_values_str, rock_a_validities=rock_a_validities_str,
                           rock_a_mills=rock_a_mills_str, roll_a_names=roll_a_names_str,
                           roll_a_dates=roll_a_dates_str,
                           roll_a_values=roll_a_values_str, roll_a_validities=roll_a_validities_str,
                           roll_a_mills=roll_a_mills_str, label_points_str=label_points_str, labels_str=labels_str)


# get recipe and number by date.
@app.route('/api/get_recipe', methods=['POST'], strict_slashes=False)
def get_recipe():
    json_text = request.get_json(force=True)
    # print(json_text)
    date = json_text['new_result']['date']

    dates = date.split('-')
    day = dates[0]
    month = dates[1]
    year = dates[2]

    # column names
    recipe_values = []

    search_date = day + '.' + month + '.' + year
    search = "%{}%".format(search_date)
    recipes = RecipeNumber.query.filter(RecipeNumber.TIME_STRING.like(search)).all()

    for each in recipes:
        if each.VAR_VALUE == 1.0:
            recipe_values.append('Recipe 1')
        elif each.VAR_VALUE == 2.0:
            recipe_values.append('Recipe 2')
        elif each.VAR_VALUE == 3.0:
            recipe_values.append('Recipe 3')
        elif each.VAR_VALUE == 4.0:
            recipe_values.append('Recipe 4')

    recipe_values = list(dict.fromkeys(recipe_values))

    return '_'.join(recipe_values)


# get a certain recipe and its number by date.
@app.route('/api/get_recipe_number', methods=['POST'], strict_slashes=False)
def get_recipe_number():
    json_text = request.get_json(force=True)
    # print(json_text)
    date = json_text['new_result']['date']
    recipe = json_text['new_result']['recipe']

    recipe_number = 0
    if recipe == 'Recipe 1':
        recipe_number = 1.0
    elif recipe == 'Recipe 2':
        recipe_number = 2.0
    elif recipe == 'Recipe 3':
        recipe_number = 3.0
    elif recipe == 'Recipe 4':
        recipe_number = 4.0

    search_date = date.replace("-", ".")

    search = "%{}%".format(search_date)
    # Save all recipe operations on that day
    recipes = RecipeNumber.query.filter(RecipeNumber.TIME_STRING.like(search)).all()
    # Save all door operations on that day
    door_opens = OvenDoor.query.filter(OvenDoor.TIME_STRING.like(search)).all()

    # Save time intervals between target recipe and next recipe
    recipe_map = {}
    for i in range(len(recipes)):
        if recipes[i].VAR_VALUE == recipe_number:
            start_time = recipes[i].TIME_STRING.split(" ")[1]
            hour = start_time.split(":")[0]
            min = start_time.split(":")[1]
            sec = start_time.split(":")[2]
            time_stamp = int(hour) * 60 * 60 + int(min) * 60 + int(sec)
            if i == len(recipes) - 1:
                recipe_map[time_stamp] = 1000000000000
            else:
                start_time2 = recipes[i + 1].TIME_STRING.split(" ")[1]
                hour2 = start_time2.split(":")[0]
                min2 = start_time2.split(":")[1]
                sec2 = start_time2.split(":")[2]
                time_stamp2 = int(hour2) * 60 * 60 + int(min2) * 60 + int(sec2)
                recipe_map[time_stamp] = time_stamp2

    # Count recipes which is set in last day
    lastday_recipes = RecipeNumber.query.filter(RecipeNumber.rowid.like(recipes[0].rowid - 1)).all()
    if len(lastday_recipes):
        if lastday_recipes[0].VAR_VALUE == recipe_number:
            start_time = recipes[0].TIME_STRING.split(" ")[1]
            hour = start_time.split(":")[0]
            min = start_time.split(":")[1]
            sec = start_time.split(":")[2]
            time_stamp = int(hour) * 60 * 60 + int(min) * 60 + int(sec)
            recipe_map[0] = time_stamp

    # Count how many door operations in the recipe operation intervals
    count = 0
    for each in door_opens:
        if each.VAR_VALUE == 1.0:
            time_stamp = transform_date_timestamp(each.TIME_STRING.split(" ")[1])
            for recipe in recipe_map:
                if recipe < time_stamp < recipe_map[recipe]:
                    count = count + 1
                    break

    return str(count)


def sortByTime(all): # Sort data by TIME_MS field
    for each in all:
        each.TIME_MS = int(str(each.TIME_MS).ljust(15, '0'))  # Append zeros to make up to 15 bit for TIME_MS field
    all.sort(key=operator.attrgetter('TIME_MS'))
    return all


# search all circles by date
@app.route('/api/search_by_date', methods=['POST'], strict_slashes=False)
def search_by_date():
    json_text = request.get_json(force=True)
    # print(json_text)
    date = json_text['new_result']['date']

    date = date.replace('-', '.')

    # column names
    names = []
    dates = []
    values = []
    validities = []
    mills = []

    # -------Oven_Temperature_PV--------
    search = "%{}%".format(date)
    ot_all = OvenTemp.query.filter(OvenTemp.TIME_STRING.like(search)).all()

    ot_all = sortByTime(ot_all)
    # read all data on the latest day
    for each in ot_all:
        # print(ot_each)
        names.append(each.VAR_NAME)
        dates.append(each.TIME_STRING)
        values.append(each.VAR_VALUE)
        validities.append(each.VALIDITY)
        mills.append(each.TIME_MS)
    ot_names_str = '_'.join(names)
    ot_dates_str = '_'.join(dates)
    ot_values_str = '_'.join(str(e) for e in values)  # Convert float to str
    ot_validities_str = '_'.join(str(e) for e in validities)  # Convert float to str
    ot_mills_str = '_'.join(str(e) for e in mills)  # Convert float to str

    result = ot_names_str + ',' + ot_dates_str + ',' + ot_values_str + ',' + ot_validities_str + ',' + ot_mills_str

    # --------Mould_Temperature_PV-------
    mt_all = MouldTemp.query.filter(MouldTemp.TIME_STRING.like(search)).all()
    mt_all = sortByTime(mt_all)

    # column names
    names.clear()
    mt_dates = []
    mt_values = []
    validities.clear()
    mills.clear()

    for each in mt_all:
        # print(mt_each)
        names.append(each.VAR_NAME)
        mt_dates.append(each.TIME_STRING)
        mt_values.append(each.VAR_VALUE)
        validities.append(each.VALIDITY)
        mills.append(each.TIME_MS)

    mt_names_str = '_'.join(names)
    mt_dates_str = '_'.join(mt_dates)
    mt_values_str = '_'.join(str(e) for e in mt_values)  # Convert float to str
    mt_validities_str = '_'.join(str(e) for e in validities)  # Convert float to str
    mt_mills_str = '_'.join(str(e) for e in mills)  # Convert float to str

    result = result + ";" + mt_names_str + ',' + mt_dates_str + ',' + mt_values_str + ',' + mt_validities_str + ',' + mt_mills_str

    # -------Cooling_Temperature_PV--------
    ct_all = CoolingTemp.query.filter(CoolingTemp.TIME_STRING.like(search)).all()

    ct_all = sortByTime(ct_all)
    # column names
    names.clear()
    dates.clear()
    values = []
    validities = []
    mills = []

    # read all data on the latest day
    for each in ct_all:
        # print(mt_each)
        names.append(each.VAR_NAME)
        dates.append(each.TIME_STRING)
        values.append(each.VAR_VALUE)
        validities.append(each.VALIDITY)
        mills.append(each.TIME_MS)

    ct_names_str = '_'.join(names)
    ct_dates_str = '_'.join(dates)
    ct_values_str = '_'.join(str(e) for e in values)  # Convert float to str
    ct_validities_str = '_'.join(str(e) for e in validities)  # Convert float to str
    ct_mills_str = '_'.join(str(e) for e in mills)  # Convert float to str

    result = result + ";" + ct_names_str + ',' + ct_dates_str + ',' + ct_values_str + ',' + ct_validities_str + ',' + ct_mills_str

    # ----------------Rock_Angle_PV------------------
    rock_a_all = RockAngle.query.filter(RockAngle.TIME_STRING.like(search)).all()
    rock_a_all = sortByTime(rock_a_all)


    # column names
    names.clear()
    dates.clear()
    values.clear()
    validities.clear()
    mills.clear()

    # read all data on the latest day
    for each in rock_a_all:
        # print(mt_each)
        names.append(each.VAR_NAME)
        dates.append(each.TIME_STRING)
        values.append(each.VAR_VALUE)
        validities.append(each.VALIDITY)
        mills.append(each.TIME_MS)

    rock_a_names_str = '_'.join(names)
    rock_a_dates_str = '_'.join(dates)
    rock_a_values_str = '_'.join(str(e) for e in values)  # Convert float to str
    rock_a_validities_str = '_'.join(str(e) for e in validities)  # Convert float to str
    rock_a_mills_str = '_'.join(str(e) for e in mills)  # Convert float to str

    result = result + ";" + rock_a_names_str + ',' + rock_a_dates_str + ',' + rock_a_values_str + ',' + rock_a_validities_str + ',' + rock_a_mills_str

    # ----------------Roll_Angle_PV-----------------
    roll_a_all = RollAngle.query.filter(RollAngle.TIME_STRING.like(search)).all()
    roll_a_all = sortByTime(roll_a_all)

    # column names
    names.clear()
    dates.clear()
    values.clear()
    validities.clear()
    mills.clear()

    # read all data on the latest day
    for each in roll_a_all:
        # print(mt_each)
        names.append(each.VAR_NAME)
        dates.append(each.TIME_STRING)
        values.append(each.VAR_VALUE)
        validities.append(each.VALIDITY)
        mills.append(each.TIME_MS)

    roll_a_names_str = '_'.join(names)
    roll_a_dates_str = '_'.join(dates)
    roll_a_values_str = '_'.join(str(e) for e in values)  # Convert float to str
    roll_a_validities_str = '_'.join(str(e) for e in validities)  # Convert float to str
    roll_a_mills_str = '_'.join(str(e) for e in mills)  # Convert float to str

    recipes = RecipeNumber.query.filter(RecipeNumber.TIME_STRING.like(search)).all()
    # Save time intervals between target recipe and next recipe
    recipe_map_map = {}

    # recipe numbers ----> recipe intervals ----> start time and end time
    for i in range(len(recipes)):
        if recipes[i].VAR_VALUE not in recipe_map_map:
            recipe_map = {}
            start_time = recipes[i].TIME_STRING.split(" ")[1]
            time_stamp = transform_date_timestamp(start_time)
            if i == len(recipes) - 1:
                recipe_map[time_stamp] = 1000000000000
            else:
                start_time2 = recipes[i + 1].TIME_STRING.split(" ")[1]
                time_stamp2 = transform_date_timestamp(start_time2)
                recipe_map[time_stamp] = time_stamp2
            recipe_map_map[recipes[i].VAR_VALUE] = recipe_map
        else:
            recipe_map = recipe_map_map[recipes[i].VAR_VALUE]
            start_time = recipes[i].TIME_STRING.split(" ")[1]
            time_stamp = transform_date_timestamp(start_time)
            if i == len(recipes) - 1:
                recipe_map[time_stamp] = 1000000000000
            else:
                start_time2 = recipes[i + 1].TIME_STRING.split(" ")[1]
                time_stamp2 = transform_date_timestamp(start_time2)
                recipe_map[time_stamp] = time_stamp2

    # Count recipes which is set in last day
    lastday_recipes = RecipeNumber.query.filter(RecipeNumber.rowid.like(recipes[0].rowid - 1)).all()
    if len(lastday_recipes) != 0:
        if lastday_recipes[0].VAR_VALUE not in recipe_map_map:
            recipe_map = {}
            start_time = recipes[0].TIME_STRING.split(" ")[1]
            time_stamp = transform_date_timestamp(start_time)
            recipe_map[0] = time_stamp
            recipe_map_map[lastday_recipes[0].VAR_VALUE] = recipe_map
        else:
            recipe_map = recipe_map_map[lastday_recipes[0].VAR_VALUE]
            start_time = recipes[0].TIME_STRING.split(" ")[1]
            time_stamp = transform_date_timestamp(start_time)
            recipe_map[0] = time_stamp

    label_points = []
    labels = []
    for label in recipe_map_map:
        for start_time in recipe_map_map[label]:
            for i in range(1, len(mt_values)):
                if mt_values[i - 1] < 20 and mt_values[i] > 20:  # 20 is the least value to plot
                    if start_time < transform_date_timestamp(mt_dates[i].split(" ")[1]) < recipe_map_map[label][
                        start_time]:
                        label_points.append(str(i))
                        labels.append(str(label))
                        break

    label_points_str = "_".join(label_points)
    labels_str = "_".join(labels)

    result = result + ";" + roll_a_names_str + ',' + roll_a_dates_str + ',' + roll_a_values_str + ',' + roll_a_validities_str + ',' + roll_a_mills_str
    result = result + ';' + label_points_str + ';' + labels_str  # Add label point

    return result


# search all circles by date and recipe
@app.route('/api/search_by_date_recipe', methods=['POST'], strict_slashes=False)
def search_by_date_recipe():
    json_text = request.get_json(force=True)
    # print(json_text)
    date = json_text['new_result']['date']
    recipe = json_text['new_result']['recipe']

    recipe_number = 0
    if recipe == 'Recipe 1':
        recipe_number = 1.0
    elif recipe == 'Recipe 2':
        recipe_number = 2.0
    elif recipe == 'Recipe 3':
        recipe_number = 3.0
    elif recipe == 'Recipe 4':
        recipe_number = 4.0

    search_date = date.replace("-", ".")

    search = "%{}%".format(search_date)
    # Save all recipe operations on that day
    recipes = RecipeNumber.query.filter(RecipeNumber.TIME_STRING.like(search)).all()

    # Save all door operations on that day
    door_opens = OvenDoor.query.filter(OvenDoor.TIME_STRING.like(search)).all()

    # Save time intervals between target recipe and next recipe
    recipe_map = {}
    for i in range(len(recipes)):
        if recipes[i].VAR_VALUE == recipe_number:
            start_time = recipes[i].TIME_STRING.split(" ")[1]
            time_stamp = transform_date_timestamp(start_time)
            if i == len(recipes) - 1:
                recipe_map[time_stamp] = 1000000000000
            else:
                start_time2 = recipes[i + 1].TIME_STRING.split(" ")[1]
                time_stamp2 = transform_date_timestamp(start_time2)
                recipe_map[time_stamp] = time_stamp2

    # Count recipes which is set in last day
    lastday_recipes = RecipeNumber.query.filter(RecipeNumber.rowid.like(recipes[0].rowid - 1)).all()
    if len(lastday_recipes) != 0:
        if lastday_recipes[0].VAR_VALUE == recipe_number:
            start_time = recipes[0].TIME_STRING.split(" ")[1]
            time_stamp = transform_date_timestamp(start_time)
            recipe_map[0] = time_stamp

    # Record all recipes index which match the parameter
    recipe_index = []
    for i in range(len(recipes)):
        if recipes[i].VAR_VALUE == recipe_number:
            recipe_index.append(i)

    # Count recipes which is set in last day
    lastday_recipes = RecipeNumber.query.filter(RecipeNumber.rowid.like(recipes[0].rowid - 1)).all()
    if len(lastday_recipes) != 0:
        if lastday_recipes[0].VAR_VALUE == recipe_number:
            recipe_index.append(-1)

    time_maps = {}
    if len(recipes) == 1:
        time_maps[0] = 10000000000
    else:
        for each in recipe_index:
            if each == -1:
                recipe_time = 0  # If last recipe in previous day is a target recipe
            else:
                recipe_time = transform_date_timestamp(recipes[each].TIME_STRING.split(" ")[1])
            for i in range(len(door_opens)):
                time = door_opens[i].TIME_STRING.split(" ")[1]
                time_stamp = transform_date_timestamp(time)
                # find the first door open marker which bigger than the recipe timestamp
                if door_opens[i].VAR_VALUE == 0 and time_stamp > recipe_time:
                    if i == len(door_opens) - 1 or i == len(door_opens) - 2:
                        # If this open is the last or last -1, mean the recipe won't change
                        time_maps[time_stamp] = 10000000000
                        break
                    if each == (len(recipes) - 1):
                        # If this recipe marker is the last marker of one day
                        time_maps[time_stamp] = 10000000000
                        break
                    for j in range(i + 1, len(door_opens)):
                        # If the door marker's value is open
                        if door_opens[j].VAR_VALUE == 0:
                            time = door_opens[j].TIME_STRING.split(" ")[1]
                            time_stamp2 = transform_date_timestamp(time)
                            # If next recipe marker is between the first open door mark and the second open door mark,
                            # and the next recipe marker is not the same as the selected recipe, then the range is valid
                            # for plotting the cooling temperature
                            for re in range(each + 1, len(recipes)):
                                temp_time = transform_date_timestamp(
                                    recipes[re].TIME_STRING.split(" ")[1])
                                if time_stamp < temp_time < time_stamp2 and recipes[
                                    re].VAR_VALUE != recipe_number:
                                    time_maps[time_stamp] = time_stamp2
                                    break
                                if temp_time > time_stamp2:
                                    # This recipe setting time is after the second open door time,
                                    # so no need to continue
                                    break
                            if time_stamp in time_maps and time_maps[time_stamp] == time_stamp2:
                                break
                    if time_maps.get(time_stamp) == None:
                        # Mean no more recipe changes any more
                        time_maps[time_stamp] = 10000000000
                        break
                    break

    # column names
    names = []
    dates = []
    values = []
    validities = []
    mills = []

    # --------Mould_Temperature_PV-------
    mt_all = MouldTemp.query.filter(MouldTemp.TIME_STRING.like(search)).all()
    mt_all = sortByTime(mt_all)


    # column names
    names.clear()
    mt_dates = []
    mt_values = []
    validities.clear()
    mills.clear()

    for each in mt_all:
        time_stamp = transform_date_timestamp(each.TIME_STRING.split(" ")[1])
        exist = 0
        for internal in recipe_map:
            if internal < time_stamp < recipe_map[internal]:
                names.append(each.VAR_NAME)
                mt_dates.append(each.TIME_STRING)
                mt_values.append(each.VAR_VALUE)
                validities.append(each.VALIDITY)
                mills.append(each.TIME_MS)
                exist = 1
                break
        if exist == 0:
            names.append(each.VAR_NAME)
            mt_dates.append(each.TIME_STRING)
            mt_values.append(0)
            validities.append(each.VALIDITY)
            mills.append(each.TIME_MS)

    mt_names_str = '_'.join(names)
    mt_dates_str = '_'.join(mt_dates)
    mt_values_str = '_'.join(str(e) for e in mt_values)  # Convert float to str
    mt_validities_str = '_'.join(str(e) for e in validities)  # Convert float to str
    mt_mills_str = '_'.join(str(e) for e in mills)  # Convert float to str

    # -------Cooling_Temperature_PV--------
    ct_all = CoolingTemp.query.filter(CoolingTemp.TIME_STRING.like(search)).all()
    ct_all = sortByTime(ct_all)

    # column names
    names.clear()
    ct_dates = []
    ct_values = []
    validities = []
    mills = []
    # read all data on the latest day
    for each in ct_all:
        exist = 0
        time_stamp = transform_date_timestamp(each.TIME_STRING.split(" ")[1])
        for start in time_maps:
            if start < time_stamp < time_maps[start]:
                names.append(each.VAR_NAME)
                ct_dates.append(each.TIME_STRING)
                ct_values.append(each.VAR_VALUE)
                validities.append(each.VALIDITY)
                mills.append(each.TIME_MS)
                exist = 1
                break
        if exist == 0:
            names.append(each.VAR_NAME)
            ct_dates.append(each.TIME_STRING)
            ct_values.append(0)
            validities.append(each.VALIDITY)
            mills.append(each.TIME_MS)

    ct_names_str = '_'.join(names)
    ct_dates_str = '_'.join(ct_dates)
    ct_values_str = '_'.join(str(e) for e in ct_values)  # Convert float to str
    ct_validities_str = '_'.join(str(e) for e in validities)  # Convert float to str
    ct_mills_str = '_'.join(str(e) for e in mills)  # Convert float to str

    # Find time ranges between mould temperature circle and cooling circle
    oven_time_map = {}
    ct_index = 0
    for i in range(len(mt_values)):
        if i != len(mt_values) - 1 and mt_values[i] <= 10 and mt_values[i + 1] > 10:
            oven_time_start = mt_dates[i + 1]  # start point of a mould temperature circle
            for y in range(ct_index, len(ct_values)):
                # whether find the end point of a cooling circle
                if y == len(ct_values) - 1 or (ct_values[y] != 0 and ct_values[y + 1] == 0):
                    oven_time_map[oven_time_start] = ct_dates[y]
                    ct_index = y + 1
                    break

    # -------Oven_Temperature_PV--------
    ot_all = OvenTemp.query.filter(OvenTemp.TIME_STRING.like(search)).all()
    ot_all = sortByTime(ot_all)


    # read all data on the latest day
    for each in ot_all:
        # print(ot_each)
        exist = 0
        for start in oven_time_map:
            if transform_date_timestamp(start.split(" ")[1]) <= transform_date_timestamp(
                    each.TIME_STRING.split(" ")[1]) <= transform_date_timestamp(oven_time_map[start].split(" ")[1]):
                names.append(each.VAR_NAME)
                dates.append(each.TIME_STRING)
                values.append(each.VAR_VALUE)
                validities.append(each.VALIDITY)
                mills.append(each.TIME_MS)
                exist = 1
                break
        if exist == 0:
            names.append(each.VAR_NAME)
            dates.append(each.TIME_STRING)
            values.append(0)
            validities.append(each.VALIDITY)
            mills.append(each.TIME_MS)

    ot_names_str = '_'.join(names)
    ot_dates_str = '_'.join(dates)
    ot_values_str = '_'.join(str(e) for e in values)  # Convert float to str
    ot_validities_str = '_'.join(str(e) for e in validities)  # Convert float to str
    ot_mills_str = '_'.join(str(e) for e in mills)  # Convert float to str

    # ----------------Rock_Angle_PV------------------
    rock_a_all = RockAngle.query.filter(RockAngle.TIME_STRING.like(search)).all()
    rock_a_all = sortByTime(rock_a_all)
    # column names
    names.clear()
    dates.clear()
    values.clear()
    validities.clear()
    mills.clear()

    # read all data on the latest day
    for each in rock_a_all:
        # exist = 0
        for start in oven_time_map:
            if transform_date_timestamp(start.split(" ")[1]) <= transform_date_timestamp(
                    each.TIME_STRING.split(" ")[1]) <= transform_date_timestamp(oven_time_map[start].split(" ")[1]):
                names.append(each.VAR_NAME)
                dates.append(each.TIME_STRING)
                values.append(each.VAR_VALUE)
                validities.append(each.VALIDITY)
                mills.append(each.TIME_MS)
                # exist = 1
                break
        # if exist == 0:
        #     names.append(each.VAR_NAME)
        #     dates.append(each.TIME_STRING)
        #     values.append(0)
        #     validities.append(each.VALIDITY)
        #     mills.append(each.TIME_MS)

    rock_a_names_str = '_'.join(names)
    rock_a_dates_str = '_'.join(dates)
    rock_a_values_str = '_'.join(str(e) for e in values)  # Convert float to str
    rock_a_validities_str = '_'.join(str(e) for e in validities)  # Convert float to str
    rock_a_mills_str = '_'.join(str(e) for e in mills)  # Convert float to str

    # ----------------Roll_Angle_PV-----------------
    roll_a_all = RollAngle.query.filter(RollAngle.TIME_STRING.like(search)).all()
    roll_a_all = sortByTime(roll_a_all)
    # column names
    names.clear()
    dates.clear()
    values.clear()
    validities.clear()
    mills.clear()

    # read all data on the latest day
    for each in roll_a_all:
        # print(mt_each)
        for start in oven_time_map:
            if transform_date_timestamp(start.split(" ")[1]) <= transform_date_timestamp(
                    each.TIME_STRING.split(" ")[1]) <= transform_date_timestamp(oven_time_map[start].split(" ")[1]):
                names.append(each.VAR_NAME)
                dates.append(each.TIME_STRING)
                values.append(each.VAR_VALUE)
                validities.append(each.VALIDITY)
                mills.append(each.TIME_MS)
                break

    roll_a_names_str = '_'.join(names)
    roll_a_dates_str = '_'.join(dates)
    roll_a_values_str = '_'.join(str(e) for e in values)  # Convert float to str
    roll_a_validities_str = '_'.join(str(e) for e in validities)  # Convert float to str
    roll_a_mills_str = '_'.join(str(e) for e in mills)  # Convert float to str

    result = ot_names_str + ',' + ot_dates_str + ',' + ot_values_str + ',' + ot_validities_str + ',' + ot_mills_str
    result = result + ";" + mt_names_str + ',' + mt_dates_str + ',' + mt_values_str + ',' + mt_validities_str + ',' + mt_mills_str
    result = result + ";" + ct_names_str + ',' + ct_dates_str + ',' + ct_values_str + ',' + ct_validities_str + ',' + ct_mills_str
    result = result + ";" + rock_a_names_str + ',' + rock_a_dates_str + ',' + rock_a_values_str + ',' + rock_a_validities_str + ',' + rock_a_mills_str
    result = result + ";" + roll_a_names_str + ',' + roll_a_dates_str + ',' + roll_a_values_str + ',' + roll_a_validities_str + ',' + roll_a_mills_str

    return result


# search all circles by date and recipe
@app.route('/api/search_by_date_recipe_number', methods=['POST'], strict_slashes=False)
def search_by_date_recipe_number():
    json_text = request.get_json(force=True)
    # print(json_text)
    date = json_text['new_result']['date']
    recipe = json_text['new_result']['recipe']
    number = json_text['new_result']['number']
    number = int(number)

    recipe_number = 0
    if recipe == 'Recipe 1':
        recipe_number = 1.0
    elif recipe == 'Recipe 2':
        recipe_number = 2.0
    elif recipe == 'Recipe 3':
        recipe_number = 3.0
    elif recipe == 'Recipe 4':
        recipe_number = 4.0

    search_date = date.replace("-", ".")

    search = "%{}%".format(search_date)
    # Save all recipe operations on that day
    recipes = RecipeNumber.query.filter(RecipeNumber.TIME_STRING.like(search)).all()

    # Save all door operations on that day
    door_opens = OvenDoor.query.filter(OvenDoor.TIME_STRING.like(search)).all()

    # Save time intervals between target recipe and next recipe
    recipe_map = {}
    for i in range(len(recipes)):
        if recipes[i].VAR_VALUE == recipe_number:
            start_time = recipes[i].TIME_STRING.split(" ")[1]
            time_stamp = transform_date_timestamp(start_time)
            if i == len(recipes) - 1:
                recipe_map[time_stamp] = 1000000000000
            else:
                start_time2 = recipes[i + 1].TIME_STRING.split(" ")[1]
                time_stamp2 = transform_date_timestamp(start_time2)
                recipe_map[time_stamp] = time_stamp2

    # Count recipes which is set in last day
    lastday_recipes = RecipeNumber.query.filter(RecipeNumber.rowid.like(recipes[0].rowid - 1)).all()
    if len(lastday_recipes) != 0:
        if lastday_recipes[0].VAR_VALUE == recipe_number:
            start_time = recipes[0].TIME_STRING.split(" ")[1]
            time_stamp = transform_date_timestamp(start_time)
            recipe_map[0] = time_stamp

    recipe_map = {k: v for k, v in sorted(recipe_map.items(), key=lambda item: item[1])}
    recipe_map_temp = {}

    # record an interval of a certain number of a script
    i = 0
    start = 0
    end = 0
    for each in recipe_map:
        success = 0
        start = each
        end = recipe_map[each]
        for d in range(len(door_opens)):
            current_door = door_opens[d]
            door_open_time = transform_date_timestamp(current_door.TIME_STRING.split(" ")[1])
            if current_door.VAR_VALUE == 0 and each < door_open_time < recipe_map[each]:
                i = i + 1
                if i == number:  # if it's the number which is search, make it be the end time and break
                    end = door_open_time
                    success = 1
                    break
                else:  # if it's not the number which is search, make it be the start time
                    start = door_open_time
            elif door_open_time > recipe_map[each]:
                break
        if success == 1:
            break

    recipe_map_temp[start] = end

    recipe_map = recipe_map_temp

    # Record all recipes index which match the parameter
    recipe_index = []
    for i in range(len(recipes)):
        if recipes[i].VAR_VALUE == recipe_number:
            recipe_index.append(i)

    # Count recipes which is set in last day
    lastday_recipes = RecipeNumber.query.filter(RecipeNumber.rowid.like(recipes[0].rowid - 1)).all()
    if len(lastday_recipes) != 0:
        if lastday_recipes[0].VAR_VALUE == recipe_number:
            recipe_index.append(-1)

    time_maps = {}
    if len(recipes) == 1:
        time_maps[0] = 10000000000
    else:
        for each in recipe_index:
            if each == -1:
                recipe_time = 0  # If last recipe in previous day is a target recipe
            else:
                recipe_time = transform_date_timestamp(recipes[each].TIME_STRING.split(" ")[1])
            for i in range(len(door_opens)):
                time = door_opens[i].TIME_STRING.split(" ")[1]
                door1_time_stamp = transform_date_timestamp(time)
                if each != len(recipes) - 1 and door1_time_stamp > transform_date_timestamp(
                        recipes[each + 1].TIME_STRING.split(" ")[1]):
                    # If next door open marker time is bigger than next recipe time, mean this recipe has no circle,
                    # then should be ignored.
                    break
                # find the first door open marker which bigger than the recipe timestamp
                if door_opens[i].VAR_VALUE == 0 and door1_time_stamp > recipe_time:
                    if i == len(door_opens) - 1 or i == len(door_opens) - 2:
                        # If this open is the last or last -1, mean the recipe won't change
                        time_maps[door1_time_stamp] = 10000000000
                        break
                    if each == (len(recipes) - 1):
                        # If this recipe marker is the last marker of one day
                        time_maps[door1_time_stamp] = 10000000000
                        break
                    for j in range(i + 1, len(door_opens)):
                        # If the door marker's value is open
                        if door_opens[j].VAR_VALUE == 0:
                            time = door_opens[j].TIME_STRING.split(" ")[1]
                            door2_time_stamp = transform_date_timestamp(time)
                            # If next recipe marker is between the first open door mark and the second open door mark,
                            # and the next recipe marker is not the same as the selected recipe, then the range is valid
                            # for plotting the cooling temperature
                            for re in range(each + 1, len(recipes)):
                                temp_time = transform_date_timestamp(
                                    recipes[re].TIME_STRING.split(" ")[1])
                                if door1_time_stamp < temp_time < door2_time_stamp and recipes[
                                    re].VAR_VALUE != recipe_number:
                                    time_maps[door1_time_stamp] = door2_time_stamp
                                    break
                                if temp_time > door2_time_stamp:
                                    # This recipe setting time is after the second open door time,
                                    # so no need to continue
                                    break
                            if door1_time_stamp in time_maps and time_maps[door1_time_stamp] == door2_time_stamp:
                                break
                    if time_maps.get(door1_time_stamp) == None:
                        # Mean no more recipe changes any more
                        time_maps[door1_time_stamp] = 10000000000
                        break
                    break

    time_maps_temp = {}
    for start in time_maps:
        if len(time_maps_temp.items()) == 0:
            time_maps_temp[start] = time_maps[start]
            continue
        include = 0
        for start2 in time_maps_temp:
            if start2 <= start and time_maps[start] <= time_maps_temp[start2]:
                include = 1
                break
            elif start2 <= start < time_maps_temp[start2] <= time_maps[start]:
                time_maps_temp[start2] = time_maps[start]
                include = 1
                break
            elif start <= start2 < time_maps[start] <= time_maps_temp[start2]:
                time_maps_temp[start] = time_maps_temp[start2]
                time_maps_temp.pop(start2)
                include = 1
                break
        if include == 0:
            time_maps_temp[start] = time_maps[start]

    time_maps_temp = {k: v for k, v in sorted(time_maps_temp.items(), key=lambda item: item[1])}
    # time_maps_temp = {}
    i = 0
    # record an interval of a certain number of a script
    start = 0
    end = 0
    for each in time_maps_temp:
        success = 0
        start = each
        end = time_maps_temp[each]
        for d in range(len(door_opens)):
            current_door = door_opens[d]
            door_open_time = transform_date_timestamp(current_door.TIME_STRING.split(" ")[1])
            if current_door.VAR_VALUE == 0 and each < door_open_time <= time_maps_temp[each]:
                i = i + 1
                if i == number:  # if it's the number which is search, make it be the end time and break
                    end = door_open_time
                    success = 1
                    break
                else:  # if it's not the number which is search, make it be the start time
                    start = door_open_time
            elif door_open_time > time_maps_temp[each]:
                break
        if success == 1:
            break

    time_maps_temp = {}
    time_maps_temp[start] = end
    time_maps = time_maps_temp

    # column names
    names = []
    dates = []
    values = []
    validities = []
    mills = []

    # --------Mould_Temperature_PV-------
    mt_all = MouldTemp.query.filter(MouldTemp.TIME_STRING.like(search)).all()
    mt_all = sortByTime(mt_all)

    # column names
    names.clear()
    mt_dates = []
    mt_values = []
    validities.clear()
    mills.clear()

    for each in mt_all:
        time_stamp = transform_date_timestamp(each.TIME_STRING.split(" ")[1])
        end = 0  # Record whether each has arrived the last recipe map
        for internal in recipe_map:
            if internal < time_stamp < recipe_map[internal]:
                if MouldTempMin < int(each.VAR_VALUE) < MouldTempMax:
                    names.append(each.VAR_NAME)
                    mt_dates.append(each.TIME_STRING)
                    mt_values.append(each.VAR_VALUE)
                    validities.append(each.VALIDITY)
                    mills.append(each.TIME_MS)
                    break
            elif time_stamp >= recipe_map[internal]:
                end = 1
                break
        if end == 1:
            break

        # if exist == 0:
        #     names.append(each.VAR_NAME)
        #     dates.append(each.TIME_STRING)
        #     values.append(0)
        #     validities.append(each.VALIDITY)
        #     mills.append(each.TIME_MS)

    mt_names_str = '_'.join(names)
    mt_dates_str = '_'.join(mt_dates)
    mt_values_str = '_'.join(str(e) for e in mt_values)  # Convert float to str
    mt_validities_str = '_'.join(str(e) for e in validities)  # Convert float to str
    mt_mills_str = '_'.join(str(e) for e in mills)  # Convert float to str

    # -------Cooling_Temperature_PV--------
    ct_all = CoolingTemp.query.filter(CoolingTemp.TIME_STRING.like(search)).all()
    ct_all = sortByTime(ct_all)

    # column names
    names.clear()
    ct_dates = []
    ct_values = []
    validities = []
    mills = []
    # read all data on the latest day
    for each in ct_all:
        time_stamp = transform_date_timestamp(each.TIME_STRING.split(" ")[1])
        end = 0  # Record whether each has arrived the last recipe map
        for start in time_maps:
            if start < time_stamp < time_maps[start]:
                # Filter out abnormal data
                if CoolingTempMin < int(each.VAR_VALUE) < CoolingTempMax:
                    names.append(each.VAR_NAME)
                    ct_dates.append(each.TIME_STRING)
                    ct_values.append(each.VAR_VALUE)
                    validities.append(each.VALIDITY)
                    mills.append(each.TIME_MS)
                    break
            elif time_stamp >= time_maps[start]:
                end = 1
                break
        if end == 1:  # Iterated cool data has beyond the last recipe interval
            break
        # if exist == 0:
        #     names.append(each.VAR_NAME)
        #     dates.append(each.TIME_STRING)
        #     values.append(0)
        #     validities.append(each.VALIDITY)
        #     mills.append(each.TIME_MS)

    ct_names_str = '_'.join(names)
    ct_dates_str = '_'.join(ct_dates)
    ct_values_str = '_'.join(str(e) for e in ct_values)  # Convert float to str
    ct_validities_str = '_'.join(str(e) for e in validities)  # Convert float to str
    ct_mills_str = '_'.join(str(e) for e in mills)  # Convert float to str

    # column names
    names.clear()
    ot_dates = []
    ot_values = []
    validities.clear()
    mills.clear()

    # -------Oven_Temperature_PV--------
    ot_all = OvenTemp.query.filter(OvenTemp.TIME_STRING.like(search)).all()
    ot_all = sortByTime(ot_all)

    # read all data on the latest day
    for each in ot_all:
        mt_start_time = transform_date_timestamp(mt_dates[0].split(" ")[1])
        ct_end_time = transform_date_timestamp(ct_dates[len(ct_dates) - 1].split(" ")[1])
        ot_time = transform_date_timestamp(each.TIME_STRING.split(" ")[1])
        if mt_start_time <= ot_time <= ct_end_time:
            names.append(each.VAR_NAME)
            ot_dates.append(each.TIME_STRING)
            ot_values.append(each.VAR_VALUE)
            validities.append(each.VALIDITY)
            mills.append(each.TIME_MS)
        elif ot_time > ct_end_time:
            break

    ot_names_str = '_'.join(names)
    ot_dates_str = '_'.join(ot_dates)
    ot_values_str = '_'.join(str(e) for e in ot_values)  # Convert float to str
    ot_validities_str = '_'.join(str(e) for e in validities)  # Convert float to str
    ot_mills_str = '_'.join(str(e) for e in mills)  # Convert float to str

    # ----------------Rock_Angle_PV------------------
    rock_a_all = RockAngle.query.filter(RockAngle.TIME_STRING.like(search)).all()
    rock_a_all = sortByTime(rock_a_all)

    # column names
    names.clear()
    dates.clear()
    values.clear()
    validities.clear()
    mills.clear()

    # read all data on the latest day
    for each in rock_a_all:
        # print(mt_each)
        mt_start_time = transform_date_timestamp(mt_dates[0].split(" ")[1])
        ct_end_time = transform_date_timestamp(ct_dates[len(ct_dates) - 1].split(" ")[1])
        rock_time = transform_date_timestamp(each.TIME_STRING.split(" ")[1])
        if mt_start_time <= rock_time <= ct_end_time:
            names.append(each.VAR_NAME)
            dates.append(each.TIME_STRING)
            values.append(each.VAR_VALUE)
            validities.append(each.VALIDITY)
            mills.append(each.TIME_MS)
        elif rock_time > ct_end_time:
            break

    rock_a_names_str = '_'.join(names)
    rock_a_dates_str = '_'.join(dates)
    rock_a_values_str = '_'.join(str(e) for e in values)  # Convert float to str
    rock_a_validities_str = '_'.join(str(e) for e in validities)  # Convert float to str
    rock_a_mills_str = '_'.join(str(e) for e in mills)  # Convert float to str

    # ----------------Roll_Angle_PV-----------------
    roll_a_all = RollAngle.query.filter(RollAngle.TIME_STRING.like(search)).all()
    roll_a_all = sortByTime(roll_a_all)

    # column names
    names.clear()
    dates.clear()
    values.clear()
    validities.clear()
    mills.clear()

    # read all data on the latest day
    for each in roll_a_all:
        mt_start_time = transform_date_timestamp(mt_dates[0].split(" ")[1])
        ct_end_time = transform_date_timestamp(ct_dates[len(ct_dates) - 1].split(" ")[1])
        roll_time = transform_date_timestamp(each.TIME_STRING.split(" ")[1])
        if mt_start_time <= roll_time <= ct_end_time:
            names.append(each.VAR_NAME)
            dates.append(each.TIME_STRING)
            values.append(each.VAR_VALUE)
            validities.append(each.VALIDITY)
            mills.append(each.TIME_MS)

    roll_a_names_str = '_'.join(names)
    roll_a_dates_str = '_'.join(dates)
    roll_a_values_str = '_'.join(str(e) for e in values)  # Convert float to str
    roll_a_validities_str = '_'.join(str(e) for e in validities)  # Convert float to str
    roll_a_mills_str = '_'.join(str(e) for e in mills)  # Convert float to str

    result = ot_names_str + ',' + ot_dates_str + ',' + ot_values_str + ',' + ot_validities_str + ',' + ot_mills_str
    result = result + ";" + mt_names_str + ',' + mt_dates_str + ',' + mt_values_str + ',' + mt_validities_str + ',' + mt_mills_str
    result = result + ";" + ct_names_str + ',' + ct_dates_str + ',' + ct_values_str + ',' + ct_validities_str + ',' + ct_mills_str
    result = result + ";" + rock_a_names_str + ',' + rock_a_dates_str + ',' + rock_a_values_str + ',' + rock_a_validities_str + ',' + rock_a_mills_str
    result = result + ";" + roll_a_names_str + ',' + roll_a_dates_str + ',' + roll_a_values_str + ',' + roll_a_validities_str + ',' + roll_a_mills_str

    return result


def transform_date_timestamp(time):
    hour = time.split(":")[0]
    min = time.split(":")[1]
    sec = time.split(":")[2]
    time_stamp = int(hour) * 60 * 60 + int(min) * 60 + int(sec)
    return time_stamp


def search_by_date_recipe_number():
    return 0
