import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Finally, add the code to import the dependencies that we need for Flask.

from flask import Flask, jsonify

# Setup the database engine for Flask application

engine = create_engine("sqlite:///hawaii.sqlite")

# The create_engine() function allows us to access and query our SQLite database file. 

# The create_engine() function allows us to access and query our SQLite database file. 

Base = automap_base()

# Now, we're going to reflect our tables.

Base.prepare(engine, reflect=True)

Base.classes.keys()

# With the database reflected, we can save our references to each table.

Measurement = Base.classes.measurement
Station = Base.classes.station

# Finally, create a session link from Python to our database 

session = Session(engine)

# Set up Flask

app = Flask(__name__)

# All of your routes should go after the app = Flask(__name__) line of code. Otherwise, your code may not run properly.

# We can define the welcome route

@app.route("/")

#  The next step is to add the routing information for each of the other routes. For this we'll create a function, 
# and our return statement will have f-strings as a reference to all of the other routes.

def welcome():
     return(
    '''
    WElcome to The Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

# The next route we'll build is for the precipitation analysis. This route will occur separately from the welcome route.

@app.route("/api/v1.0/precipitation")

# Next, we will create the precipitation() function.

def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

# First, we want to add the line of code that calculates the date one year ago from the most recent date in the database
# Next, write a query to get the date and precipitation for the previous year.
# Finally, we'll create a dictionary with the date as the key and the precipitation as the value. To do this, we will "jsonify" our dictionary.

# The stations route. For this route we'll simply return a list of all the stations.

@app.route("/api/v1.0/stations")

# We'll create a new function called stations()

def stations():
   # Now we need to create a query that will allow us to get all of the stations in our database.
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    # We want to start by unraveling our results into a one-dimensional array
    return jsonify(stations=stations)

# For this route, the goal is to return the temperature observations for the previous year.

@app.route("/api/v1.0/tobs")

# Next, create a function called temp_monthly()

def temp_monthly():

    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.date >= prev_year).\
        filter(Measurement.station == 'USC00519281').all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps) 

# 1. Calculate the date one year ago from the last date in the database
# 2. The next step is to query the primary station for all the temperature observations from the previous year.
# 3. Finally, as before, unravel the results into a one-dimensional array and convert that array into a list. 


# Our last route will be to report on the minimum, average, and maximum temperatures. However, 
# this route is different from the previous ones in that we will have to provide both a starting and ending date

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

# 1. We need to add parameters to our stats()function: a start parameter and an end parameter
# 2. With the function declared, we can now create a query to select the minimum, average, and maximum temperatures from our SQLite database
# 3. Since we need to determine the starting and ending date, add an if-not statement to our code. This will help us accomplish a few things.
# 4. In the following code, take note of the asterisk in the query
# 5. The asterisk is used to indicate there will be multiple results for our query: minimum, average, and maximum temperatures.
# 6. Now we need to calculate the temperature minimum, average, and maximum with the start and end dates

if __name__ == '__main__':
    app.run()