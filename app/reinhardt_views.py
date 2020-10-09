# Python modules
import os
import operator
import time
from datetime import datetime, timezone

# Flask modules
from flask import render_template, request, url_for, redirect, send_from_directory
from flask_login import login_user, logout_user, current_user

# App modules
from app import app, lm, db
from app.forms import LoginForm, RegisterForm
from app.models import RH_OvenTemperature, RH_ARM1_PRODUCTION, RH_ARM2_PRODUCTION, RH_ARM3_PRODUCTION, \
    RH_ARM4_PRODUCTION, RH_Common_Recipe, RH_OvenDelay, ARM_One, ARM_Two, ARM_Three, ARM_Four

from sqlalchemy import Column, String, Integer, text
import json
import pytz
from datetime import timedelta


def convertTimeZoneIndiaToNZ(india_time):
    india_time = india_time.replace(tzinfo=pytz.timezone('Asia/Calcutta'))
    localFormat = "%Y-%m-%d %H:%M:%S"
    localDatetime = india_time.astimezone(pytz.timezone("Pacific/Auckland"))
    return localDatetime.strftime(localFormat)


def convertDateToStr(time):
    localFormat = "%Y-%m-%d %H:%M:%S"
    return time.strftime(localFormat)


def getArmRecipeData():
    recipe_setting_list = []  # sort from arm1 to arm4

    latest_arm1_production = RH_ARM1_PRODUCTION.query.order_by(
        RH_ARM1_PRODUCTION.time.desc()).all()  # Read the latest line in the table

    for each in latest_arm1_production:
        if each.receipe_no is not None:
            recipe_setting_list.append(each.receipe_no)
            break

    latest_arm2_production = RH_ARM2_PRODUCTION.query.order_by(
        RH_ARM2_PRODUCTION.time.desc()).all()  # Read the latest line in the table

    for each in latest_arm2_production:
        if each.receipe_no is not None:
            recipe_setting_list.append(each.receipe_no)
            break

    latest_arm3_production = RH_ARM3_PRODUCTION.query.order_by(
        RH_ARM3_PRODUCTION.time.desc()).all()  # Read the latest line in the table

    for each in latest_arm3_production:
        if each.receipe_no is not None:
            recipe_setting_list.append(each.receipe_no)
            break

    latest_arm4_production = RH_ARM4_PRODUCTION.query.order_by(
        RH_ARM4_PRODUCTION.time.desc()).all()  # Read the latest line in the table

    for each in latest_arm4_production:
        if each.receipe_no is not None:
            recipe_setting_list.append(each.receipe_no)
            break

    return recipe_setting_list


def getCommonRecipeData():
    recipe_settings = []  # sort from arm1 to arm4

    rh_common_recipe = RH_Common_Recipe.query.all()  # Read the latest line in the table

    for each in rh_common_recipe:
        recipe_setting = []  # include RECEIPE_NO (This spelling wrong name is named by an India guy from reinhardt machine...), SET_TEMP_1, MOULD_SPEED, HEAT1
        recipe_setting.append(each.receipe_no)
        recipe_setting.append(each.set_temp_1)
        recipe_setting.append(each.mould_speed)
        recipe_setting.append(each.heat1)
        recipe_settings.append(recipe_setting)

    return recipe_settings


# Rock & Roll page
@app.route('/reinhardt_charts.html', methods=['GET', 'POST'], defaults={'path': 'reinhardt_charts.html'})
def reinhardt_page(path):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    if path != 'reinhardt_charts.html' and path != '':
        try:
            # try to match the pages defined in -> pages/<input file>
            return render_template('pages/' + path)
        except:
            return render_template('pages/error-404.html')

    # column names
    ot_times = []
    ot_temperatures = []

    latest = RH_OvenTemperature.query.order_by(
        RH_OvenTemperature.Time.desc()).first()  # Read the latest line in the table
    latest_time = latest.Time
    latest_day = str(latest_time).split(" ")[0]  # Get the latest day
    search = "%{}%".format(latest_day)

    ot_temperatures_latest_day = RH_OvenTemperature.query.filter(RH_OvenTemperature.Time.like(search)).all()

    # Decide whether need to convert time zone
    need_convert_time_zone = False
    for each in ot_temperatures_latest_day:
        if each.Time.hour <= 5:
            need_convert_time_zone = True
            break

    # read all temperatures on the latest day
    for each in ot_temperatures_latest_day:
        # print(ot_each)
        time = convertTimeZone(need_convert_time_zone, each.Time)
        # time = convertTimeZoneIndiaToNZ(each.Time)
        ot_times.append(time)
        ot_temperatures.append(str(each.TEMP))

    ot_times_str = '_'.join(ot_times)
    ot_temperatures_str = '_'.join(ot_temperatures)
    print("latest_time = " + str(latest_time))

    arm_recipe_data = getArmRecipeData()
    recipe_settings = getCommonRecipeData()

    return render_template('pages/reinhardt_charts.html', ot_times=ot_times_str, ot_temperatures=ot_temperatures_str,
                           arm_recipe_data=arm_recipe_data, recipe_settings=recipe_settings)


# get recipe and number by date.
@app.route('/api/reinhardt/get_ot_by_date', methods=['POST'], strict_slashes=False)
def get_ot_by_date():
    json_text = request.get_json(force=True)
    # print(json_text)
    date = json_text['parameter']['date']

    dates = date.split('-')
    day = dates[0]
    month = dates[1]
    year = dates[2]

    # column names
    ot_times = []
    ot_temperatures = []

    search_date = year + '_' + month + '_' + day
    search = "%{}%".format(search_date)
    ot_temperatures_by_day = RH_OvenTemperature.query.filter(RH_OvenTemperature.Time.like(search)).all()

    # read all temperatures on the latest day
    if len(ot_temperatures_by_day) == 0:
        return '0'

    # Decide whether need to convert time zone
    need_convert_time_zone = False
    for each in ot_temperatures_by_day:
        if each.Time.hour <= 5:
            need_convert_time_zone = True
            break

    for each in ot_temperatures_by_day:
        # print(ot_each)
        time = convertTimeZone(need_convert_time_zone, each.Time)
        ot_times.append(time)
        ot_temperatures.append(str(each.TEMP))

    ot_times_str = '_'.join(ot_times)
    ot_temperatures_str = '_'.join(ot_temperatures)

    result = ot_times_str + ";" + ot_temperatures_str

    return result


def convertTimeZone(needConvertTimeZone, time):
    if needConvertTimeZone:
        result = convertTimeZoneIndiaToNZ(time)
    else:
        result = convertDateToStr(time)
    return result


# get recipe and number by date.
@app.route('/api/reinhardt/get_recipe', methods=['POST'], strict_slashes=False)
def rh_get_recipe():
    json_text = request.get_json(force=True)
    date = json_text['parameter']['date']

    dates = date.split('-')
    day = dates[0]
    month = dates[1]
    year = dates[2]

    # column names
    recipe_values = []

    search_date = year + '_' + month + '_' + day
    search = "%{}%".format(search_date)
    recipes = RH_OvenDelay.query.filter(RH_OvenDelay.Time.like(search)).all()

    for each in recipes:
        if (not recipe_values.__contains__(str(each.Receipe_no))) and str(each.Receipe_no) != "None":
            recipe_values.append(str(each.Receipe_no))

    return '_'.join(recipe_values)


# get recipe and number by date.
@app.route('/api/reinhardt/get_recipe_number', methods=['POST'], strict_slashes=False)
def rh_get_recipe_number():
    json_text = request.get_json(force=True)
    date = json_text['parameter']['date']
    recipe = json_text['parameter']['recipe']

    dates = date.split('-')
    day = dates[0]
    month = dates[1]
    year = dates[2]

    # Recipe count in the date
    count = 0

    search_date = year + '_' + month + '_' + day
    search = "%{}%".format(search_date)
    recipes = RH_OvenDelay.query.filter(RH_OvenDelay.Time.like(search)).all()

    for each in recipes:
        if each.Receipe_no == int(recipe):
            count = count + 1

    return str(count)


# search all oven temperature by date and recipe
@app.route('/api/reinhardt/search_by_date_recipe', methods=['POST'], strict_slashes=False)
def rh_search_by_date_recipe():
    json_text = request.get_json(force=True)
    date = json_text['new_result']['date']
    recipe = json_text['new_result']['recipe']
    number = None
    if 'number' in json_text['new_result']:
        number = json_text['new_result']['number']

    dates = date.split('-')
    day = dates[0]
    month = dates[1]
    year = dates[2]

    # Recipe count in the date

    search_date = year + '_' + month + '_' + day
    search = "%{}%".format(search_date)
    recipes = RH_OvenDelay.query.filter(RH_OvenDelay.Time.like(search)).all()

    # Save time intervals between target recipe and next recipe
    ot_temperature_datas = []  # Oven temperature list for saving certain day and certain recipe
    for index in range(0, len(recipes)):
        if recipes[index].Receipe_no == int(recipe):  # Current start recipe is the target recipe
            if index != len(recipes) - 1:
                start = datetime.strptime(recipes[index].Time.split('.')[0], "%Y-%m-%d %H:%M:%S")
                end = datetime.strptime(recipes[index + 1].Time.split('.')[0], "%Y-%m-%d %H:%M:%S")
                ot_temperature_data = RH_OvenTemperature.query.filter(RH_OvenTemperature.Time >= start).filter(
                    RH_OvenTemperature.Time <= end).all()  # Get oven temperature between the time interval
                ot_temperature_datas.append(ot_temperature_data)
            else:
                start = datetime.strptime(recipes[index].Time.split('.')[0], "%Y-%m-%d %H:%M:%S")
                end = start.replace(hour=23, minute=59, second=59)
                ot_temperature_data = RH_OvenTemperature.query.filter(RH_OvenTemperature.Time >= start).filter(
                    RH_OvenTemperature.Time <= end).all()  # Get oven temperature between the time interval
                ot_temperature_datas.append(ot_temperature_data)

    current_number = 1
    times = []
    temperatures = []

    # Decide whether need to convert time zone
    need_convert_time_zone = False
    for ot_temperature_data in ot_temperature_datas:
        for each in ot_temperature_data:
            if each.Time.hour <= 5:
                need_convert_time_zone = True
                break

    for ot_temperature_data in ot_temperature_datas:
        if number is None:
            for i in range(0, len(ot_temperature_data)):
                times.append(convertTimeZone(need_convert_time_zone, ot_temperature_data[i].Time).split('.')[0])
                temperatures.append(str(ot_temperature_data[i].TEMP))
                if i == len(ot_temperature_data) - 1:
                    # generate a new time stamp for None to separate the graphs
                    second_none = ot_temperature_data[i].Time.second
                    minute_none = ot_temperature_data[i].Time.minute
                    if second_none == 59:
                        minute_none = minute_none + 1
                    else:
                        second_none = second_none + 1
                    times.append(convertTimeZone(need_convert_time_zone,
                                                 ot_temperature_data[i].Time.replace(
                                                     minute=minute_none, second=second_none)).split('.')[0])
                    temperatures.append("None")
        elif int(number) == current_number:
            for i in range(0, len(ot_temperature_data)):
                times.append(convertTimeZone(need_convert_time_zone, ot_temperature_data[i].Time).split('.')[0])
                temperatures.append(str(ot_temperature_data[i].TEMP))
            break
        current_number = current_number + 1

    time_string = "_".join(times)
    temperature_string = "_".join(temperatures)

    return time_string + "," + temperature_string


def convertTimetoTimestamp(time):
    return int(time.split(":")[0]) * 60 * 60 + int(time.split(":")[1]) * 60 + int(time.split(":")[2])


def sortFunc(item):
    time = item.time
    return int(time.split(":")[0]) * 60 * 60 + int(time.split(":")[1]) * 60 + int(time.split(":")[2])


def sortByTime(all):  # Sort data by TIME field
    # for each in all:
    all.sort(key=sortFunc)
    return all


# get recipe and number by date.
@app.route('/api/k-kord/get_arm_by_date', methods=['POST'], strict_slashes=False)
def get_arm_by_date():
    json_text = request.get_json(force=True)
    date = json_text['parameter']['date']
    arm = json_text['parameter']['arm']

    dates = date.split('-')
    day = str(int(dates[2]))  # drop the zero
    month = str(int(dates[1]))  # drop the zero
    year = dates[0]

    # column names
    arm_times = []
    arm_IATs = []
    arm_MWTs = []
    arm_AMBs = []

    search_date = day + '.' + month + '.' + year

    arm_data_by_day = None
    if arm == 1:
        arm_data_by_day = ARM_One.query.filter(ARM_One.date.contains(search_date)).all()
        arm_data_by_day.sort(key=sortFunc)
    elif arm == 2:
        arm_data_by_day = ARM_Two.query.filter(ARM_Two.date.contains(search_date)).all()
        arm_data_by_day.sort(key=sortFunc)
    elif arm == 3:
        arm_data_by_day = ARM_Three.query.filter(ARM_Three.date.contains(search_date)).all()
        arm_data_by_day.sort(key=sortFunc)
    elif arm == 4:
        arm_data_by_day = ARM_Four.query.filter(ARM_Four.date.contains(search_date)).all()
        arm_data_by_day.sort(key=sortFunc)

    # read all temperatures on the latest day
    if arm_data_by_day is None:
        return '0'

    # Decide whether need to convert time zone
    need_convert_time_zone = False
    for each in arm_data_by_day:
        if int(each.time.split(":")[0]) <= 5:
            need_convert_time_zone = True
            break

    for each in arm_data_by_day:
        time = convertTimeZone(need_convert_time_zone,
                               datetime(year=int(year), month=int(month), day=int(day),
                                        hour=int(each.time.split(":")[0]),
                                        minute=int(each.time.split(":")[1]), second=int(each.time.split(":")[2])))
        arm_times.append(time.split(" ")[1])
        arm_IATs.append(str(each.iat))
        arm_MWTs.append(str(each.mwt))
        arm_AMBs.append(str(each.amb))

    arm_times = '_'.join(arm_times)
    arm_IATs = '_'.join(arm_IATs)
    arm_MWTs = '_'.join(arm_MWTs)
    arm_AMBs = '_'.join(arm_AMBs)

    result = arm_times + ";" + arm_IATs + ";" + arm_MWTs + ";" + arm_AMBs

    return result


# get recipe and number by date.
@app.route('/api/k-kord/get_arm_by_date_intervals', methods=['POST'], strict_slashes=False)
def get_arm_by_date_intervals():
    json_text = request.get_json(force=True)
    date = json_text['parameter']['date']
    arm = json_text['parameter']['arm']
    intervals = json_text['parameter']['intervals']
    ot_data = json_text['parameter']['ot_data']

    timeStamps = []
    for interval in intervals.split("_"):
        timeStamps.append(interval.split(" ")[1])

    otData = []
    for data in ot_data.split("_"):
        otData.append(data)

    dates = date.split('-')
    day = str(int(dates[2]))  # drop the zero
    month = str(int(dates[1]))  # drop the zero
    year = dates[0]
    # column names
    arm_times = []
    arm_IATs = []
    arm_MWTs = []
    arm_AMBs = []

    search_date = day + '.' + month + '.' + year

    arm_data_by_day = None
    if arm == 1:
        arm_data_by_day = ARM_One.query.filter(ARM_One.date.contains(search_date)).all()
        arm_data_by_day.sort(key=sortFunc)
    elif arm == 2:
        arm_data_by_day = ARM_Two.query.filter(ARM_Two.date.contains(search_date)).all()
        arm_data_by_day.sort(key=sortFunc)
    elif arm == 3:
        arm_data_by_day = ARM_Three.query.filter(ARM_Three.date.contains(search_date)).all()
        arm_data_by_day.sort(key=sortFunc)
    elif arm == 4:
        arm_data_by_day = ARM_Four.query.filter(ARM_Four.date.contains(search_date)).all()
        arm_data_by_day.sort(key=sortFunc)

    # read all temperatures on the latest day
    if arm_data_by_day is None:
        return '0'

    intervals = {}
    interval_start = timeStamps[0]

    for index in range(0, len(timeStamps)):  # Record all intervals for display
        if otData[index] == 'None':
            intervals[interval_start] = timeStamps[index]
            if index != len(timeStamps) - 1:
                interval_start = timeStamps[index + 1]

    if len(intervals) == 0:
        intervals[interval_start] = timeStamps[len(timeStamps) - 1]

    # Decide whether need to convert time zone
    need_convert_time_zone = False
    for each in arm_data_by_day:
        if int(each.time.split(":")[0]) <= 5:
            need_convert_time_zone = True
            break

    interval_end = False  # mark this arm data is the last data of an interval.
    for each in arm_data_by_day:
        time = convertTimeZone(need_convert_time_zone,
                               datetime(year=int(year), month=int(month), day=int(day),
                                        hour=int(each.time.split(":")[0]),
                                        minute=int(each.time.split(":")[1]), second=int(each.time.split(":")[2])))

        exist_in_interval = False  # mark this arm data whether belongs to any time interval
        for start in intervals:
            if convertTimetoTimestamp(start) <= convertTimetoTimestamp(time.split(" ")[1]) < convertTimetoTimestamp(
                    intervals[start]):
                arm_times.append(time.split(" ")[1])
                arm_IATs.append(str(each.iat))
                arm_MWTs.append(str(each.mwt))
                arm_AMBs.append(str(each.amb))
                exist_in_interval = True
                interval_end = True

        if interval_end and not exist_in_interval:
            arm_times.append(time.split(" ")[1])
            arm_IATs.append('None')
            arm_MWTs.append('None')
            arm_AMBs.append('None')
            interval_end = False
            continue

    arm_times = '_'.join(arm_times)
    arm_IATs = '_'.join(arm_IATs)
    arm_MWTs = '_'.join(arm_MWTs)
    arm_AMBs = '_'.join(arm_AMBs)

    result = arm_times + ";" + arm_IATs + ";" + arm_MWTs + ";" + arm_AMBs

    return result
