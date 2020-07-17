import numpy as np

import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func ,inspect

from flask import Flask, jsonify

# Engine create
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Database to new model
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

# Tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session
session = Session(engine)

inspector = inspect(engine)
inspector.get_table_names()

# Flask app
app = Flask(__name__)


# Query for the dates and temperature observations from the last year.

@app.route("/")
def home():
    return (f"Climate Flask App - Tina's Climate API for Hawaii<br/>"
            f"--------------------------------------<br/>"
            f"Routes for data below:<br/>"
            f"/stations - Weather observation station listing<br/>"
            f"/precipitation - Precip data for latest year<br/>"
            f"/temperature - Temp data for latest year<br/>"
            f"--------------------------------------<br/>"
            f"~~~ datesearch (yyyy-mm-dd)<br/>"
            f"/datesearch/2014-03-01  ~~~~~~~~~~~ low, high, and average temp for date given and each date after<br/>"
            f"/datesearch/2014-03-01/2015-01-30 ~~ low, high, and average temp for date given and each date up to and including end date<br/>"
            f"--------------------------------------<br/>"
            f"~ data available from 2010-01-01 to 2017-08-23 ~<br/>")

@app.route("/precipitation")
def precipitation():
    results1 = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>="2016-08-23").all()
    first_dict = list(np.ravel(results1))

#  Return JSON of the dictionary
    return jsonify(first_dict)


@app.route("/stations")
def stations():
    results2 = session.query(Station.station, Station.name).all()

    sec_dict = list(np.ravel(results2))

# # #  Return the JSON representation of your dictionary.

    return jsonify(sec_dict)

# #   * Return a JSON list of Temperature Observations (tobs) for the previous year.

@app.route("/tobs")
def tobs():
    results3 = session.query(Measurement.date, Measurement.tobs).\
            filter(Measurement.date>="2016-08-23").\
            filter(Measurement.date<="2017-08-23").all()

            
    temp_dict = list(np.ravel(results3))

# #  Return the JSON representation of your dictionary.

    return jsonify(temp_dict)


# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

# When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

# When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.


@app.route("/datesearch/<start>")
def single_date(start):
	# Set up for user to enter date
	Start_Date = dt.datetime.strptime(start,"%Y-%m-%d")

	# Query Min, Max, and Avg based on date
	summary_stats = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.round(func.avg(Measurement.tobs))).\
	filter(Measurement.date >= Start_Date).all()
	# Close the Query
	session.close() 
	
	summary = list(np.ravel(summary_stats))

	# Jsonify summary
	return jsonify(summary)

# Same as above with the inclusion of an end date
@app.route("/datesearch/<start>/<end>")
def trip_dates(start,end):
	# Set up for user to enter dates 
	Start_Date = dt.datetime.strptime(start,"%Y-%m-%d")
	End_Date = dt.datetime.strptime(end,"%Y-%m-%d")

	# Query Min, Max, and Avg based on dates
	summary_stats = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.round(func.avg(Measurement.tobs))).\
	filter(Measurement.date.between(Start_Date,End_Date)).all()
	# Close the Query
	session.close()    
	
	summary = list(np.ravel(summary_stats))

	# Jsonify summary
	return jsonify(summary)

    
if __name__ == '__main__':
    app.run(debug=True)

