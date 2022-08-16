#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# import dependencies
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# setup flask app
app = Flask(__name__)

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# save to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask routes
@app.route("/")
def welcome():
    return (
        f"Available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/StartDate(YYYY-MM-DD)/EndDate(YYYY-MM-DD)")
        
@app.route("/api/v1.0/precipitation")
def precipitation():
    # create python session to database
    session = Session(engine)
    
    # query for last year's data
    sel = [Measurement.date, func.sum(Measurement.prcp)]
    year_data = session.query(*sel).filter(func.strftime(Measurement.date)>=dt.date(2016, 8, 23)).        order_by(Measurement.date).group_by(Measurement.date).all()
    
    # close
    session.close
    
    # store the data into a dictionary
    precipitation_dict = []
    for date, prcp in year_data:
        dict = {}
        dict["date"] = date
        dict["prcp"] = prcp
        precipitation_data.append(dict)
    
    # Return dictionary jsonified for the API route
    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    # create python session to database
    session = Session(engine)

    # query for stations
    stations = session.query(Station.station).all()

    # close
    session.close

    # make list jsonified for api
    stations_list = list(np.ravel(stations))
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # create python session to database
    session = Session(engine)

    # query for last year's data of the most active station
    temp_data = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281',        func.strftime(Measurement.date)>=dt.date(2016, 8, 23)).all()
    
    # close
    session.close

    # make list jsonified for api
    temp_data = list(np.ravel(temp_data))
    return jsonify(temp_data)

@app.route("/api/v1.0/<start>")
def temps(start):
    # take user input in the appropriate format
    year, month, day = map(int, start.split("-"))
    date1 = dt.date(year, month, day)
    
    # create python session to database
    session = Session(engine)

    # query to get average, lowest, and highest temperature from the most used station
    sel = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    temp = session.query(*sel).filter(Measurement.station == 'USC00519281',        func.strftime(Measurement.date)>=date1).all()
    
    # close
    session.close

    # store the data into a dictionary
    low_high_avg = []
    for low, high, avg in temp:
        dict = {}
        dict["min temp"] = low
        dict["max temp"] = high
        dict["avg temp"] = avg
        low_high_avg.append(dict)
    
    # return dictionary
    return jsonify(low_high_avg)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # take user input in the appropriate format
    year, month, day = map(int, start.split("-"))
    date1 = dt.date(year, month, day)
    
    # take 2nd user input in the appropriate format
    year, month, day = map(int, end.split("-"))
    date2 = dt.date(year, month, day)

    # create python session to database
    session = Session(engine)

    # query to get average, lowest, and highest temperature from the most used station
    sel = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    temp = session.query(*sel).filter(Measurement.station == 'USC00519281',        func.strftime(Measurement.date)>=date1, func.strftime(Measurement.date)<=date2).all()
    
    # close
    session.close

    # store the data into a dictionary
    low_high_avg = []
    for low, high, avg in temp:
        dict = {}
        dict["min temp"] = low
        dict["max temp"] = high
        dict["avg temp"] = avg
        low_high_avg.append(dict)
    
    # make list jsonified for api
    return jsonify(low_high_avg)

if __name__ == "__main__":
    app.run(debug=True)

