from asyncio import threads
from functions import *
import os
import flask
import requests
import base64
import hashlib
import random
import psycopg2
import pyproj
import math
from flask import Flask, session, flash, render_template, url_for, redirect, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy import insert
from werkzeug.utils import redirect
import shapely.wkt
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_session import Session

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://enrjbwpogarfwo' \
                                        ':8c48c2461ae5556e202cf036c86a96fdb14272810befb99ac17103c333a14082@ec2-3-218' \
                                        '-47-9.compute-1.amazonaws.com:5432/d21fv63o2is7mq'

# set session secret key
app.secret_key = 'ENGO551_Lab1'

# set up database connection **MAKE SURE ITS postgresql AND NOT postgres**
engine = create_engine(os.getenv("DATABASE_URL"))

db = scoped_session(sessionmaker(bind=engine))

conn = psycopg2.connect(
    host="ec2-3-218-47-9.compute-1.amazonaws.com",
    database="d21fv63o2is7mq",
    user="enrjbwpogarfwo",
    password="8c48c2461ae5556e202cf036c86a96fdb14272810befb99ac17103c333a14082")

cur = conn.cursor()


@app.route('/', methods=["GET"])
def index():
    return render_template('homepage.html')


@app.route('/register', methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template('signup.html')


@app.route('/user', methods=["POST"])
def user_page():
    # if request.method == "GET":
    #     return render_template('signedin.html')
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        no_u_query = "SELECT COUNT (userid) FROM users;"
        no_u = db.execute(no_u_query).fetchall()
        new_userid = no_u[0][0] + 1

        new_user_query = "INSERT INTO users (userid,username,password) VALUES ('" + str(new_userid) + "', '" + username + "', '" + password + "')"
        db.execute(new_user_query)
        db.commit()

        # remember user
        session["user_name"] = username

        flash('You have been logged in!')

        # get user's tracked habits
        # remember to convert userid to str
        userid = "2"  # CHANGE DEPENDING ON NEEDS
        userhabits_q = "SELECT habitstreak FROM userhabits WHERE userid = '" + str(userid) + "'"
        userhabits = db.execute(userhabits_q).fetchall()

        # insert habit into array (might be wrong because im not sure what the userhabits format is)
        uh = []
        [uh.append(habit) for row in userhabits for habit in row]

        print(uh)
        return render_template('signedin.html', name=username, streaks=uh)


@app.route('/addHabit', methods=["GET","POST"])
def addHabit():
    if request.method == 'POST':
        locationID = request.form.get('location') # there should be a way to have the user choose a location and then return the ID instead

        # get habit category based on locationID
        getHabitCat_q = "SELECT HabitCategory FROM HabitLocations WHERE LocationID = '" + locationID + "'"
        HabitCat = db.execute(getHabitCat_q).fetchall();

        # insert habit into users table
        addHabit_q = "INSERT INTO users (" + HabitCat + ") VALUES ('" + locationID + "') WHERE userid = '" + session["userid"] + "'"

        return render_template('successfully_added_habit.html') # "success" page


@app.route('/logout', methods=["GET"])
def logOut():
    session.clear()
    flash('You have been logged out!')
    return render_template('homepage.html')



## All frontend/python calculations done here
@app.route("/pycalcs", methods=["POST"])
def pycalcs():

    # Get user coordiantes and accuracy (m)
    if request.method == "POST":
        #print(type(request.json))
        lat = request.json['lat']
        lng = request.json['lng']
        accuracy = request.json['accuracy']
        
        #print("lat: " + str(lat))
        #print("lng: " + str(lng))
        #print("accuracy: " + str(accuracy))

    user_x = 111111 * math.cos(lat)
    user_y = 111111 * lng
    ## Create user polygon
    userPolygon = create_user_polygon(user_x, user_y, accuracy)

    ## All tracked habit locations for the user from the database
        # TODO: SQL queries to get locations which are linked with a category from both databases
    

    # get name,lat,lon,radius values from table
    habitLocation_q = "SELECT placename, latitude, longitude, radius FROM habitlocations"
    habitLocation = db.execute(habitLocation_q).fetchall()
    habitsOfInterest = []
    
    # for each row: name
    for row in habitLocation:
        r = []
        for col in row:
            r.append(col)
        habitsOfInterest.append(r)
    #print("HOOOOOOOOOOOOO")
    #print(userPolygon)
    polygonsOfInterest = []
    for buildings in habitsOfInterest:
        build_x = 111111 * math.cos(buildings[1])
        build_y = 111111 * buildings[2]
        polygonsOfInterest.append(create_user_polygon(build_x, build_y, buildings[3]))
        print("Poly of Interest: ")
        print(polygonsOfInterest)
    print("User Location: ")
    print(userPolygon)
    #print("HEEYYYYYYYYYYYYYYYYYYYYYY")
    #print(polygonsOfInterest)

# # get user's tracked habits
#     # remember to convert userid to str
#     userid = "2"  # CHANGE DEPENDING ON NEEDS
#     userhabits_q = "SELECT habitcategory FROM userhabits WHERE userid = '" + str(userid) + "'"
#     userhabits = db.execute(userhabits_q).fetchall()

#     # insert habit into array (might be wrong because im not sure what the userhabits format is)
#     uh = []
#     [uh.append(habit) for row in userhabits for habit in row]

#     # ----------------------------------------------------------------
#     # get habit streak
#     # remember to convert userid AND habitcategory to str
#     userid = "2"  # CHANGE DEPENDING ON NEEDS
#     habitcategory = "Fitness"  # CHANGE DEPENDING ON NEEDS

#     userstreak_q = "SELECT habitstreak FROM userhabits WHERE userid = '" + str(userid) + "' AND habitcategory = '"\
#                    + str(habitcategory) + "'"
#     userstreak = db.execute(userstreak_q).fetchall()

#     # insert habit into array
#     us = []
#     [us.append(streak) for row in userstreak for streak in row]

#     # ----------------------------------------------------------------
#     # updating streak
#     # remember to convert userid AND habitcategory AND new_streak to str
#     userid = "2"  # CHANGE DEPENDING ON NEEDS
#     habitcategory = "Fitness"  # CHANGE DEPENDING ON NEEDS

    # get data from temp_status
    temp_status_q = "SELECT * FROM temp_status"
    temp_status = db.execute(temp_status_q).fetchall()
    ts = []
    [ts.append(stat) for row in temp_status for stat in row]


    inHabit = ts[1]
    print(inHabit)

    habitTime = ts[2]
    habitBuilding_index = int(ts[3])
    

    threshold = 20

    inHabit_str = "f"
    habitLocation = []
    # Does the calcs for the user location at T - 1
    if inHabit == True:

        inHabit_str = "t"
        print("inHabit")
        habitTime = habitTime + 10
        habitLocation_q = "SELECT placename, latitude, longitude, radius FROM habitlocations WHERE locationid = '" + str(habitBuilding_index) + "'"
        habitLocation = db.execute(habitLocation_q).fetchall()
        #print("HEREEE WE AARRREEE")
        print(habitLocation)
        habit_x = 111111 * math.cos(habitLocation[0][1])
        habit_y = 111111 * habitLocation[0][2]
        habitBuilding = create_user_polygon(habit_x, habit_y, habitLocation[0][3])
        print("userPolygon: ")
        print(userPolygon)
        print("habitBuilding: ")
        print(habitBuilding)
        print("name: ")
        print(habitLocation[0][0])
        userOverlap = is_overlap(userPolygon, habitBuilding)
        inHabit_still  = userOverlap[0]
        print("In habit still:")
        print(inHabit_still)
        if inHabit_still == False:
            inHabit = False
            inHabit_str = "f"
            
            print("Not still true")
            if habitTime > threshold:
                print("IN THRESHOLD")
                habitTime = 0
                # if intersection detected
                new_streak = userstreak[0][0] + 1  # get usertreak from previous code
                addstreak_q = "UPDATE userhabits  SET habitstreak = '" + str(new_streak) + "' WHERE userid = '" + str(userid) \
                            + "' AND habitcategory = '" + str(habitcategory) + "'"
                db.execute(addstreak_q)
                db.commit()

    else:
        print("Not inHabit")
        for i in range (0, len(polygonsOfInterest)):
            userOverlap = is_overlap(userPolygon, polygonsOfInterest[i])
            inHabit = userOverlap[0]
            if inHabit:
                print("Now in Habit")
                print(inHabit)
                inHabit_str = "t"
                habitBuilding_index = i + 1
                
        habitTime = 0
    print(habitTime)
    print(inHabit_str)
    if inHabit_str == "t":
        inHabit_str = 1
    else:
        inHabit_str = 0
    addinhabit_q = "UPDATE temp_status SET inhabit = '" + str(inHabit_str) + "' WHERE id = " + "1"
    print("final inhabit")
    
    db.execute(addinhabit_q)
    db.commit()

    addinhabittime_q = "UPDATE temp_status SET time = '" + str(habitTime) + "' WHERE id = " + "1"

    db.execute(addinhabittime_q)
    db.commit()

    addbuild_q = "UPDATE temp_status SET objectname = '" + str(habitBuilding_index) + "' WHERE id = " + "1"
    db.execute(addbuild_q)
    db.commit()
    # SQL update tempstatus 

    # ## Find the habit locations properties
    # if inHabit:
    #     habitLocationPolygon = userOverlap[1]

    # ## Loop that checks last inHabit 
    # ## boolean status if true, run calc to check if still true
    # ## then increment variables of interest (time)
    # ## if false, check if true, if so add execute sql stuff (happens once)
    # always pass inHabit vairable to the backend regardless of last value
    if habitLocation == []:
        return({'building_lat': 'none','building_lng': 'none', 'building_acc': 'none', 'inHabit_status': 'false'})
    else:
        return({'building_lat': habitLocation[0][1],'building_lng': habitLocation[0][2], 'building_acc': habitLocation[0][3], 'inHabit_status': 'true'})

# @app.route("/", methods = ["GET", "POST"])
# def index():

#     if not session.get('logged_in'): 
#         #return render_template("homepage.html")
#         #print("here")
#         return render_template("home.html")
#     else:
#         #habits = habits.query.filter().all() # 'habits' query is not defined *********************************
#         habits = "test"
#         print("here")
#         return render_template("home.html")
#         #return render_template("signedin.html", name=session.get('username'), habits=habits)
        

@app.route("/home", methods = ["GET","POST"])
def home():
    #name = request.form.get("name")
    if not session.get('logged_in'):
        return render_template("homepage.html")
    #habits = habits.query.filter().all() 
    habits = "test"
    return render_template("signedin.html", name=session.get('username'), habits=habits)

@app.route("/signup", methods = ["GET","POST"])
def signup():
    return render_template("signup.html")



@app.route("/api/generate", methods = ["GET"])
def generate_hash_key():
    """
    @return: A hashkey for use to authenticate agains the API.
    """
    username = session["user_name"]
    taken = False

    taken_q = "SELECT apikey FROM users WHERE username = '" + str(username) + "'"
    taken_temp = db.execute(taken_q).fetchone()
    print(taken_temp[0])
    if  taken_temp[0]!= None:
       taken = True

    
    if not taken:    
        message = str(random.getrandbits(256)).encode()

        key = hashlib.sha256(message).hexdigest()
        db.execute("UPDATE users SET apikey = :key WHERE username = :username", {
            "key": key, "username":username})
        db.commit()        
    else:
        print('in here')
        key = taken_temp[0]

    return jsonify({
        "API Key": key,
        "username": username,
    })

@app.route("/api/users/<string:userid>", methods=["GET"])
def apiuser(userid):
    username = session["user_name"]
    taken_q = "SELECT apikey FROM users WHERE username = '" + str(username) + "'"
    taken_temp = db.execute(taken_q).fetchone()
    print(taken_temp[0])
    if  taken_temp[0]== None:
        return jsonify({"error": "404 - Account does not have an APIkey."})

    result = db.execute("SELECT * FROM users WHERE userid = :userid", {
                        "userid": int(userid)}).fetchone()
    
    print(type(userid))
    # Check if user exists, in case user is typed in the address bar
    if result is None:
        return jsonify({"error": "404 - UserID is not in our database."}), 404  

    user_result = db.execute("SELECT * FROM userhabits WHERE userid = :userid", {
                        "userid": userid}).fetchall()

    print(user_result)
    habitcat1 = user_result[0][2]
    cat1_streak = user_result[0][3]

    habitcat2 = user_result[1][2]
    cat2_streak = user_result[1][3]

    return jsonify({
        "Username": username,
        "Habit 1": habitcat1,
        "Habit 1 Streak": cat1_streak,
        "Habit 2": habitcat2,
        "Habit 2 Streak": cat2_streak
    })
if __name__ == '__main__':
    app.run()