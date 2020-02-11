import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """List precipitation on days JSONIFIED."""
    
    #Get all the precipitation by date
    results = session.query(Measurement.date, Measurement.prcp).group_by(Measurement.date).all()
    
    #Close the session
    session.close()
    
    #Create a dictionary using date as the key and prcp as the value.
    prcp_date = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["precipitation"] = prcp
        prcp_date.append(prcp_dict)

    return jsonify(prcp_date)

@app.route("/api/v1.0/stations")
def stations():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """List of Stations."""
    
    #Get all the Sations
    results = session.query(Station.name).all()
    
    #Close the session
    session.close()
    
    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """List of Temperature Observations (tobs) for the 12 months prior to the maximum date."""
    
    from_date = dt.datetime(2017, 8, 23)
    to_date = from_date - dt.timedelta(days=365)
    
    #Get the TOBS of the 12 months prior to the max date
    results = session.query(Measurement.date, Measurement.tobs)\
                .filter(Measurement.date <= from_date)\
                .filter(Measurement.date > to_date)\
                .order_by(Measurement.date.desc())\
                .all()
    
    #Close the session
    session.close()
    
    return jsonify(results)

@app.route("/api/v1.0/<startdate>")
def startdate(startdate):
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """List of minimum temperature, the average temperature, and the max temperature for a given date."""
    
    results = session.query(Measurement.date, func.min(Measurement.tobs),func.max(Measurement.tobs),
                            func.avg(Measurement.tobs))\
                      .filter(Measurement.date >= startdate)\
                      .all()
   
    #Close the session
    session.close()
    
    return jsonify(results)

@app.route("/api/v1.0/<startdate>/<enddate>")
def startandend(startdate, enddate):
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """List of minimum temperature, the average temperature, and the max temperature between given dates."""
    
    results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),
                            func.avg(Measurement.tobs))\
                      .filter(Measurement.date >= startdate)\
                      .filter(Measurement.date <= enddate)\
                      .all()
   
    #Close the session
    session.close()
    
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)
