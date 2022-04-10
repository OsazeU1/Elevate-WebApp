from functions import *
import os
import flask
import requests
from flask import Flask, session, render_template, url_for, redirect, request, jsonify
from sqlalchemy import create_engine
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

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    if session.get('signed_in'):
         return render_template("home.html")
    else:
         return render_template("home.html")

# All frontend/python calculations done here
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

    ## Create user polygon
    userPolygon = create_user_polygon(lat, lng, accuracy)

    ## All tracked habit locations for the user from the database
        # TODO: SQL queries to get locations which are linked with a category from both databases
    habitsOfInterest = [1, 2, 3] #Placeholder

    # ## Create polygons for each habit location
    # polygonsOfInterest = []
    # for i in habitsOfInterest:
    #     polygonsOfInterest.append(create_building_polygon(i))
    
    

    # ## Checks if user is in location every two minutes
    # userOverlap = is_overlap(polygon1, polygon2)
    # inHabit = userOverlap[0]

    # ## Find the habit locations properties
    # if inHabit:
    #     habitLocationPolygon = userOverlap[1]

    # ## Loop that checks last inHabit 
    # ## boolean status if true, run calc to check if still true
    # ## then increment variables of interest (time)
    # ## if false, check if true, if so add execute sql stuff (happens once)
    # always pass inHabit vairable to the backend regardless of last value
    return({'test_response1': 'success1', 'test_response2': 'success2'})
    

    