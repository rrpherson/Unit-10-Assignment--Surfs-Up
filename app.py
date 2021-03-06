import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False}, echo=True)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return """
<html lang="en-us">
<head>
   <meta charset="UTF-8">
   <title>Hawaii Climate App</title>
</head>
<body>
   <h1>Welcome to the Hawaii Climate App!</h1>
   <img src="https://tse1.mm.bing.net/th?id=OIP.wPYqpbSwIthiCJG9SjgWfwHaEL&pid=Api&P=0&w=304&h=172" alt="Hawaii Weather"/>
   <br>
   <h2>Informational Links:</h2>
   <p>Precipitation Analysis:</p>
   <ul>
      <li><a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a></li>
   </ul>
   <p>Station Analysis:</p>
   <ul>
      <li><a href="/api/v1.0/stations">/api/v1.0/stations</a></li>
   </ul>
   <p>Temperature Analysis:</p>
   <ul>
      <li><a href="/api/v1.0/tobs">/api/v1.0/tobs</a></li>
   </ul>
   <p>Start Day Analysis:</p>
   <ul>
      <li><a href="/api/v1.0/2017-05-19">/api/v1.0/2017-05-19</a></li>
   </ul>
   <p>Start & End Day Analysis:</p>
   <ul>
      <li><a href="/api/v1.0/2017-05-19/2017-05-31">/api/v1.0/2017-05-19/2017-05-31</a></li>
   </ul>
</body>
</html>
"""

# Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
        # Calculate the Date 1 Year Ago from the Last Data Point in the Database
        last_year = dt.date(2017,8,23) - dt.timedelta(days=365)
        # Design a Query to Retrieve the Last 12 Months of Precipitation Data Selecting Only the `date` and `prcp` Values
        prcp_data = session.query(Measurement.date, Measurement.prcp).\
                filter(Measurement.date >= last_year).\
                order_by(Measurement.date).all()
        # Convert List of Tuples Into a Dictionary
        prcp_data_list = dict(prcp_data)
        # Return JSON Representation of Dictionary
        return jsonify(prcp_data_list)

# Station Route
@app.route("/api/v1.0/stations")
def stations():
        # Design a Query to List All of the Stations Available in the Dataset
        stations = session.query(Station.station, Station.name).all()
        # Convert List of Tuples Into Normal List
        station_list = list(stations)
        # Return JSON List of Stations from the Dataset
        return jsonify(station_list)

# Temperature Observations Route
@app.route("/api/v1.0/tobs")
def tobs():
        # Design a Query for the Dates and Temperature Observations from a Year from the Last Data Point
        last_year = dt.date(2017,8,23) - dt.timedelta(days=365)
        # Design a Query to Retrieve the Last 12 Months of Precipitation Data Selecting Only the `date` and `prcp` Values
        tobs_data = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.date >= last_year).\
                order_by(Measurement.date).all()
        # Convert List of Tuples Into Normal List
        tobs_data_list = list(tobs_data)
        # Return JSON List of Temperature Observations (tobs) for the Previous Year
        return jsonify(tobs_data_list)

# Start Day Route
@app.route("/api/v1.0/<start>")
def start_day(start):
        # Design a Query to Retrieve Min, Ave, and Max Temperatures Starting on a Specific Day
        start_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                group_by(Measurement.date).all()
        # Convert List of Tuples Into Normal List
        start_day_list = list(start_day)
        # Return JSON List of Min, Avg, and Max Temperatures for the Starting Day
        return jsonify(start_day_list)

# Start-End Day Route
@app.route("/api/v1.0/<start>/<end>")
def start_end_day(start, end):
        # Design a Query to Retrieve Min, Ave, and Max Temperatures for a Specific Start-End Range
        start_end_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                filter(Measurement.date <= end).\
                group_by(Measurement.date).all()
        # Convert List of Tuples Into Normal List
        start_end_day_list = list(start_end_day)
        # Return JSON List of Min, Avg, and Max Temperatures for the Given Start-End Range
        return jsonify(start_end_day_list)

# Define Main Behavior
if __name__ == '__main__':
    app.run(debug=True)