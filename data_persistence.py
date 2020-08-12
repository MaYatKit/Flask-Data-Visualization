import csv
import os.path
import re
import sqlite3
from sqlite3 import Error
import datetime
import time
import shutil
from os import listdir
import codecs
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

class Script:
    m_db_file_path = r"C:/Users/Owner/Desktop/rr_project/rr_database.db"
    m_csv_path = r"C:/rock_roll/csv_backup/"
    m_csv_copy_path = r"G:/Shared drives/Facilities & Equipment/Rotational Moulding Equipment/Database/csv_backup/"
    m_last_csv_time = 0  # the time in the last read csv
    m_latest_back_up_date = 0  # the latest back up date

    m_wait_time = 10 * 60  # script wait time (in second)
    m_sleep_time = 10  # script sleep time (in second)
    sleeper = time

    const_week_millsecond = 604800000

    # const_week_millsecond = 6

    def __init__(self):
        self.timeString = 0


def init_database():
    if os.path.isfile(Script.m_db_file_path):
        print("DB file already exist, ignore")
        # os.remove(Script.m_db_file_path)

    else:
        print("DB file not exist, init it")
        items = set()

        for file in listdir(Script.m_csv_path):
            if os.path.isfile(Script.m_csv_path + file) and r'HMI_Panel' in file:
                with open(Script.m_csv_path + file,
                          'rt', encoding='utf-8-sig') as cf:
                    data = csv.reader(cf)
                    next(data, None)
                    for row in data:
                        s = "".join(row)
                        item_list = s.split(";")
                        items.add(item_list[0])

        print(items)
        # print(int(round(time.time() * 1000)))
        conn = sqlite3.connect(
            Script.m_db_file_path)
        c = conn.cursor()
        # Start to create tables
        for item in items:
            item = re.sub('[^0-9a-zA-Z_]+', '_', item)
            # item = item.replace(".", "_")
            print("Create table " + item)
            c.execute(r"create table if not exists " + item
                      + "( VAR_NAME TEXT    NOT NULL,"
                      + " TIME_STRING TEXT    NOT NULL unique,"
                      + " VAR_VALUE REAL   NOT NULL,"
                      + " VALIDITY INTEGER    NOT NULL,"
                      + " TIME_MS INTEGER    NOT NULL"
                      + ");")
        c.execute(r"create table Latest_Script_Parameter"  # create a table to save the latest parameter for the script
                  + "( LAST_CSV_TIME TEXT "
                  + ");")
        c.execute(r"create table Back_Up_Date"  # create a table to save the back up day for the csv
                  + "( LAST_BACKUP_DAY TEXT "
                  + ");")
        conn.commit()
        c.close()
        conn.close()
        print("DB file init finish")
        # Script.m_last_read_time = 0
        # Script.m_latest_data_time = 0
        # Script.m_latest_date_time_ms = 0
        Script.m_latest_back_up_date = 0
        Script.m_last_csv_time = 0


def convert_date_to_UNIXTimeStamp(date):
    print("date = %s" % str(date))
    date = re.split(r'[.:\s]', date)
    dt = datetime.datetime(int(date[2]), int(date[1]), int(date[0]), int(date[3]), int(date[4]), int(date[5]))

    return time.mktime(dt.timetuple())


def convert_UNIXTimeStamp_to_date(time_stamp):
    from datetime import datetime
    ts = int(time_stamp)
    # if you encounter a "year is out of range" error the timestamp
    # may be in milliseconds, try `ts /= 1000` in that case
    return time.asctime(time.localtime(time_stamp))
    # return datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S %p')


def convert_date_to_UNIXTimeStamp(year, month, day, hour, minute, second):
    dt = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
    return time.mktime(dt.timetuple())


def insert_data_to_db():
    print("Inserting data to the database...")

    conn = None
    c = None

    # csv_mtime = int(os.path.getmtime(Script.m_csv_path))  # csv modify time
    # csv_ctime = int(os.path.getctime(Script.m_csv_path))  # csv create time

    new_csvs = []
    for file in listdir(Script.m_csv_path):
        if os.path.isfile(Script.m_csv_path + file) and r'HMI_Panel' in file:
            date = file.split("_")[2]
            time = file.split("_")[3]
            csv_create_time = convert_date_to_UNIXTimeStamp(date[0:4], date[4:6], date[6:], time[0:2], time[2:4],
                                                            time[4:])
            if csv_create_time > Script.m_last_csv_time:
                new_csvs.append(file)

    # if Script.m_last_read_time >= csv_mtime:
    #     print("Last read time is greater or equal to csv last modification time, skip")
    #     print("csv_mtime : %s" % csv_mtime)
    #     print("csv_ctime : %s" % csv_ctime)
    #     print("m_last_read_time : %s" % Script.m_last_read_time)
    #     print("m_latest_data_time : %s" % Script.m_latest_data_time)
    #     print("m_latest_data_time_ms : %s" % Script.m_latest_date_time_ms)
    #     return

    if len(new_csvs) <= 0:
        # because the latest csv is possible still not finish writing,
        # so we just take the latest-1 as the latest
        print("There is no newer csv file compared with last_csv, skip")
        print("The last csv date is %s" % convert_UNIXTimeStamp_to_date(Script.m_last_csv_time))
        return

    # Sort the list
    new_csvs.sort(
        key=lambda x: convert_date_to_UNIXTimeStamp(x.split("_")[2][0:4], x.split("_")[2][4:6], x.split("_")[2][6:],
                                                    x.split("_")[3][0:2], x.split("_")[3][2:4], x.split("_")[3][4:]),
        reverse=False)

    # new_csvs = new_csvs[:len(new_csvs) - 1]

    for csv_index in range(0, len(new_csvs)):
        try:
            with codecs.open(Script.m_csv_path + new_csvs[csv_index],
                             'rb', 'utf-8') as cf:
                cvs_data = csv.reader(cf)
                next(cvs_data, None)

                conn = sqlite3.connect(Script.m_db_file_path)
                # print("Succeed to connect the database: " + sqlite3.version)
                c = conn.cursor()

                try:
                    for row in cvs_data:
                        s = "".join(row)
                        item_list = s.split(";")
                        table = re.sub('[^0-9a-zA-Z_]+', '_', item_list[0])
                        if len(item_list) != 5:  # filter out some invalid row
                            continue
                        item_list[1] = item_list[1].strip('"')  # strip out " in the data string
                        item_list[2] = re.sub('[^-0-9a-zA-Z_]+', '', item_list[2])
                        item_list[3] = re.sub('[^-0-9a-zA-Z_]+', '', item_list[3])
                        item_list[4] = re.sub('[^0-9a-zA-Z_]+', '', item_list[4])

                        # Calibrate some decimal numbers
                        if item_list[0] == "Oven.Temperature.PV":  # Temperature is around 300.0 degree.
                            if len(row) == 3:
                                integer = ("".join(row[0])).split(";")[2]
                                decimal = ("".join(row[1])).split(";")[0]
                                item_list[2] = integer + '.' + decimal
                            else:
                                integer = ("".join(row[0])).split(";")[2]
                                decimal = '0'
                                item_list[2] = integer + '.' + decimal
                        elif item_list[0] == "Mould.Temperature.PV":  # Temperature is around 20.0~140.0 degree.
                            if item_list[2][0] == "-":
                                item_list[2] = item_list[2][0:2] + '.' + item_list[2][2:]
                            elif len(row) == 2 and ("".join(row[1])).split(";")[0] == '1':
                                item_list[2] = '0'
                            elif len(row) == 1:
                                item_list[2] = ("".join(row[0])).split(";")[2]
                            else:
                                integer = ("".join(row[0])).split(";")[2]
                                decimal = ("".join(row[1])).split(";")[0]
                                item_list[2] = integer + '.' + decimal

                        elif item_list[0] == "Cooling.Temperature.PV":  # Temperature is around 100.0~185.0 degree.
                            if item_list[2][0] == "-":
                                item_list[2] = '0'  # if cooling temperature is minus, then set it to zero
                            else:
                                item_list[2] = item_list[2][0:3] + '.' + item_list[2][3:]
                        elif item_list[0] == "Rock.Angle.PV" or item_list[0] == "Roll.Angle.PV":
                            None  # Rock angle is around -26.0~26.0 degree, roll angle is around -100.0~360.0 degree.
                        elif item_list[0] == "ioCoolRotationOn" or item_list[0] == "io_CoolingFansStart" or item_list[
                            0] == "ioOvenDoorLs":  # On or Off (1.0 or 0.0).
                            item_list[2] = re.sub('[^0-9a-zA-Z_]+', '', item_list[2])
                        elif len(item_list[2]) > 1 and item_list[2][0] == '0':
                            item_list[2] = item_list[2][0] + '.' + item_list[2][1:]

                        c.execute(r'create table if not exists ' + table + "( VAR_NAME TEXT   NOT NULL,"
                                  + " TIME_STRING TEXT    NOT NULL unique,"
                                  + " VAR_VALUE REAL   NOT NULL,"
                                  + " VALIDITY INTEGER    NOT NULL,"
                                  + " TIME_MS INTEGER    NOT NULL"
                                  + ");")

                        c.execute(r"insert or ignore into " + table
                                  + "(VAR_NAME,TIME_STRING,VAR_VALUE, VALIDITY, TIME_MS)"
                                  + " values('" + item_list[0] + "','" + item_list[1] + "'," + item_list[2] + ","
                                  + item_list[3] + "," + item_list[4] + ");")
                        print(
                            "Appended a row into %s: %s + %s + %s + %s + %s, current csv is %s" % (
                                table, item_list[0], item_list[1], item_list[2],
                                item_list[3], item_list[4], new_csvs[csv_index]))

                except csv.Error as e:
                    print(e)
                    print("Error happen!!!, current csv is: " + str(
                        Script.m_csv_path + new_csvs[csv_index]) + ", skip this csv.")
                    continue

                # print("Finish "+new_csvs[csv_index]+" ...")
                # Script.sleeper.sleep(Script.m_wait_time)
                # Save current CSV's date into database
                date = new_csvs[csv_index].split("_")[2]
                time = new_csvs[csv_index].split("_")[3]
                Script.m_last_csv_time = convert_date_to_UNIXTimeStamp(date[0:4], date[4:6], date[6:], time[0:2],
                                                                       time[2:4], time[4:])
                c.execute(
                    r"delete from Latest_Script_Parameter")  # clear the previous time parameter from the database
                c.execute(
                    r"insert into Latest_Script_Parameter "  # insert the current time parameter into the database
                    + "(LAST_CSV_TIME)"
                    + " values('" + str(Script.m_last_csv_time) + "');")
                # print("Writing all data finish-----")
                print("Save current CSV's date into database field m_last_csv_time : %s" % (
                    convert_UNIXTimeStamp_to_date(Script.m_last_csv_time)))

        except Error as e:
            print(e)
            print("Error happen!!!, current csv is: " + str(Script.m_csv_path + new_csvs[csv_index]))
            # if csv_index == len(new_csvs) - 1:
            date = new_csvs[csv_index].split("_")[2]
            time = new_csvs[csv_index].split("_")[3]
            Script.m_last_csv_time = convert_date_to_UNIXTimeStamp(date[0:4], date[4:6], date[6:], time[0:2],
                                                                   time[2:4], time[4:])
            c.execute(r"delete from Latest_Script_Parameter")  # clear the previous time parameter from the database
            c.execute(r"insert into Latest_Script_Parameter "  # insert the current time parameter into the database
                      + "(LAST_CSV_TIME)"
                      + " values('" + str(Script.m_last_csv_time) + "');")
            print("------Gonna skip current csv and continue------")
            insert_data_to_db()
        finally:
            if conn:
                conn.commit()
                if c:
                    c.close()
                conn.close()
    print("------Finish to write database, copy it onto google drive------")
    # Directly upload onto cloud instead of local disk drive
    # PyDrive init
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # Creates local webserver and auto handles authentication.
    drive = GoogleDrive(gauth)
    parent_folder_id = 'xxxxxxxxxxxx'
    team_drive_id = 'xxxxxxxxxxxxxx'

    new_database = drive.CreateFile({'title': 'rr_database_new.db', 'parents': [{
        'kind': 'drive#fileLink',
        'teamDriveId': team_drive_id,
        'id': parent_folder_id
    }]})  # Create GoogleDriveFile instance with title 'Hello.txt'.
    new_database.SetContentFile(Script.m_db_file_path)
    new_database.Upload(param={'supportsTeamDrives': True})
    print("------Upload new DB file finish------")
    file_list = drive.ListFile(
        {'q': "'xxxxxxxxxxxx' in parents and trashed=false", 'corpora': 'teamDrive',
         'teamDriveId': 'xxxxxxxxxxxxxx', 'includeTeamDriveItems': True, 'supportsTeamDrives': True}).GetList()
    old_database = ""  # Old rr_database
    for file1 in file_list:
        print('title: %s, id: %s' % (file1['title'], file1['id']))
        if file1['title'] == "rr_database.db":
            old_database = file1
            break
    old_database.Trash(param={'supportsTeamDrives': True})
    print("------Delete the old database finish------")
    new_database['title'] = "rr_database.db"
    new_database.Upload(param={'supportsTeamDrives': True})


    # # Due to bug of Google File Stream, we need to modify some python library source code:
    # # https://stackoverflow.com/questions/50439371/error-during-save-and-checkpoint-when-running-jupyter-notebook-in-google-dfs-f/54313002#54313002
    # if os.path.exists(Script.m_db_file_google_drive_path):
    #     print("------DB of Google Drive exist, just copy into dir------")
    #     shutil.copy(Script.m_db_file_path,
    #                 "G:\\Shared drives\\Facilities & Equipment\\Rotational Moulding Equipment\\Database")
    #     # shutil.copyfile(Script.m_db_file_path, Script.m_db_file_google_drive_path)
    # elif os.path.exists(r"G:/Shared drives/Facilities & Equipment/Rotational Moulding Equipment/Database"):
    #     print("------DB of Google Drive isn't exist, just copy into dir------")
    #     shutil.copy(Script.m_db_file_path,
    #                 "G:\\Shared drives\\Facilities & Equipment\\Rotational Moulding Equipment\\Database")
    # else:
    #     print("------Path of Google Drive isn't exist, do not copy!------")


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        # print("Succeed to connect the database: " + sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def init_latest_time():  # try to read latest time from the database

    conn = sqlite3.connect(Script.m_db_file_path)
    c = conn.cursor()
    c.execute(r"select * from Latest_Script_Parameter")
    paras = c.fetchall()
    for para in paras:
        Script.m_last_csv_time = round(float(para[0]))

    print("Read latest csv from the database, the csv date is : %s" % (convert_UNIXTimeStamp_to_date(Script.m_last_csv_time)))
    conn.commit()
    c.close()
    conn.close()


def refresh_read_date():  # refresh the csv read date
    print("Read time has been changed.")
    csv_mtime = int(os.path.getmtime(Script.m_csv_path))  # csv modify time
    Script.m_last_read_time = csv_mtime
    conn = sqlite3.connect(Script.m_db_file_path)
    c = conn.cursor()
    c.execute(r"delete from Latest_Script_Parameter")  # clear the previous time parameter from the database
    c.execute(r"insert into Latest_Script_Parameter "  # insert the current time parameter into the database
              + "(LAST_READ_TIME, LATEST_DATA_TIME, LATEST_DATE_TIME_MS)"
              + " values('" + str(Script.m_last_read_time) + "','" + str(
        Script.m_latest_data_time) + "'," + str(Script.m_latest_date_time_ms) + ");")
    conn.commit()
    c.close()
    conn.close()
    print("csv_mtime : %s" % csv_mtime)
    print("m_last_read_time : %s" % Script.m_last_read_time)


def back_up_csv():
    conn = sqlite3.connect(Script.m_db_file_path)
    c = conn.cursor()
    if Script.m_latest_back_up_date == 0:  # cache back up time is empty
        print("Read back up time from the database")
        c.execute(r"select * from Back_Up_Date")
        paras = c.fetchall()
        for para in paras:
            Script.m_latest_back_up_date = int(para[0])
        if Script.m_latest_back_up_date == 0:  # no back up date in database
            print("No back up in the database, insert current time into database")
            Script.m_latest_back_up_date = int(round(time.time() * 1000))
            c.execute(
                r"insert into Back_Up_Date (LAST_BACKUP_DAY) values('" + str(Script.m_latest_back_up_date) + "');")
            conn.commit()
            c.close()
            conn.close()
        # back up date is more than one week ago
        elif (int(round(time.time() * 1000)) - Script.m_latest_back_up_date) >= Script.const_week_millsecond:
            print("Back up date is one week ago, copy and clear the csv ")

            for file in listdir(Script.m_csv_path):
                if os.path.isfile(Script.m_csv_path + file) and r'HMI_Panel' in file:
                    print("Back up " + Script.m_csv_path + file)
                    now = str(datetime.datetime.now())[:19]
                    now = now.replace(r" ", "_")
                    now = now.replace(r":", "_") + ".csv"
                    shutil.copy2(Script.m_csv_path + file, Script.m_csv_copy_path + file)
                    # oldcsv = open(Script.m_csv_path + file, "w+")
                    # oldcsv.truncate()
                    # oldcsv.close()
                    # os.remove(Script.m_csv_path + file)# delete the old csv file
            Script.m_latest_back_up_date = int(round(time.time() * 1000))
            c.execute(r"delete from Back_Up_Date")  # clear the previous date
            c.execute(
                r"insert into Back_Up_Date (LAST_BACKUP_DAY) values('" + str(Script.m_latest_back_up_date) + "');")
            conn.commit()
            c.close()
            conn.close()

    elif (int(round(time.time() * 1000)) - Script.m_latest_back_up_date) >= Script.const_week_millsecond:
        print("Need to back up the csv file")
        for file in listdir(Script.m_csv_path):
            if os.path.isfile(Script.m_csv_path + file) and r'HMI_Panel' in file:
                now = str(datetime.datetime.now())[:19]
                now = now.replace(r" ", "_")
                now = now.replace(r":", "_") + ".csv"
                shutil.copy2(Script.m_csv_path + file, Script.m_csv_copy_path + file)
                # oldcsv = open(Script.m_csv_path + file, "w+")
                # oldcsv.truncate()  # delete the old csv file
                # oldcsv.close()
                # os.remove(Script.m_csv_path + file) # delete the old csv file
        Script.m_latest_back_up_date = int(round(time.time() * 1000))
        c.execute(r"delete from Back_Up_Date")  # clear the previous date
        c.execute(
            r"insert into Back_Up_Date (LAST_BACKUP_DAY) values('" + str(Script.m_latest_back_up_date) + "');")
        conn.commit()
        c.close()
        conn.close()


if __name__ == '__main__':
    print("Script started ... ")
    script = Script()
    while True:
        csvs = []
        for file in listdir(Script.m_csv_path):
            if os.path.isfile(Script.m_csv_path + file) and r'HMI_Panel' in file:
                csvs.append(file)
        if len(csvs) > 0 and os.path.exists(Script.m_csv_copy_path):
            init_database()
            if Script.m_last_csv_time == 0:
                init_latest_time()
            insert_data_to_db()
            try:
                back_up_csv()
                # print("Succeed to connect the database: " + sqlite3.version)
            except Error as e:
                print("Crash happen in back_up_csv()!! See the log: ")
                print(e)

            for i in range(Script.m_wait_time):
                print("Sleep " + str(i) + "th in total " + str(Script.m_wait_time) + " seconds")
                # Keep the token being valid.
                gauth = GoogleAuth()
                gauth.LocalWebserverAuth()
                drive = GoogleDrive(gauth)
                time.sleep(1)
        else:
            print("The google drive hasn't been mounted or there is no csv, wait 10s... ")
            print("Csv amount is " + str(len(csvs)))
            print("Csv path existence is " + str(os.path.exists(Script.m_csv_copy_path)))

            time.sleep(Script.m_sleep_time)
