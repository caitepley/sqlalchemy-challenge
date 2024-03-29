# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# create the engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

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
    #List all available api routes.
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )


@app.route("/api/v1.0/precipitation")
def prcp():
    
    # Return all precipitation values
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date<='2017-08-23',Measurement.date>='2016-08-23').all()

    # Create a dictionary from the row data and append to a list of all_prcp
    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def station():

    # Return a list of all station names
    results = session.query(Station.station).all()

    # Convert list of tuples into normal list
    station_names = list(np.ravel(results))

    return jsonify(station_names)

@app.route("/api/v1.0/tobs")
def tobs():

    #Return a list of the temperatures over the previous year for the most active station
    results = session.query(Measurement.date,Measurement.tobs).filter(Measurement.station =='USC00519281', Measurement.date<='2017-08-23',Measurement.date>='2016-08-23').all()

    # Convert list of tuples into normal list
    tobs_list = list(np.ravel(results))

    return jsonify(tobs_list)


@app.route("/api/v1.0/<start>")
def start_date(start):

    # run the query to pull the min, max, and average temperatures for the range of dates
    start_date_temps = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date>=start).all()
    
     # Convert list of tuples into normal list
    temp_list = list(np.ravel(start_date_temps))
    return jsonify(temp_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start,end):

    # run the query to pull the min, max, and average temperatures for the range of dates
    start_date_temps = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date>=start).filter(Measurement.date<=end).all()
    
     # Convert list of tuples into normal list
    temp_list = list(np.ravel(start_date_temps))
    return jsonify(temp_list)

# close the session
session.close()  


if __name__ == '__main__':
    app.run(debug=True)