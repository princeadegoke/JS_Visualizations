import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, render_template

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///belly_button_biodiversity.sqlite")
session = Session(engine)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# let's get the table available - comment out for deployment
print(Base.classes.keys())
# otu, samples, samples_metadata

# create classed for the tables available
Otu = Base.classes.otu
Samples = Base.classes.samples
SamplesMetadata = Base.classes.samples_metadata


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def index():
  return render_template("template.html")

@app.route("/api/names")
def names():
    """Return a list of samples"""

    SamplesFirstRow = session.query(Samples).first()
    results = SamplesFirstRow.__dict__ 

    names = []
    for aName in results:
        namesDict = {}
        # namesDict["Name"] = "Sample ID"
        namesDict["Value"] = aName
        # names.append(namesDict)
        names.append(aName)

    return jsonify(names)

@app.route("/api/otu")
def otuList():
    """Return a list of otu data including the ID, Description"""
    # Query all passengers
    results = session.query(Otu.otu_id,Otu.lowest_taxonomic_unit_found).all()

    # Create a dictionary from the row data and append to a list of all_passengers
    otus = []
    for aotu in results:
        # print(aotu.otu_id)
        otu_dict = {}
        # otu_dict["ID"] = aotu.otu_id
        otu_dict["Lowest"] = aotu.lowest_taxonomic_unit_found
        otus.append(otu_dict)
    return jsonify(otus)

@app.route("/api/metadata/<sampleId>")
def getSample(sampleId):
    """Return Metadata for the SampleId"""
    vsampleId = sampleId[3:]
    session = Session(engine)

    results = session.query(SamplesMetadata.SAMPLEID,SamplesMetadata.ETHNICITY, SamplesMetadata.AGE,\
        SamplesMetadata.BBTYPE, SamplesMetadata.GENDER, SamplesMetadata.LOCATION).filter(SamplesMetadata.SAMPLEID == vsampleId).\
    all()

    allData = []
    for data in results:
        # print(passenger.name)
        dataDict = {}
        dataDict["AGE"] = data.AGE
        dataDict["BBTYPE"] = data.BBTYPE
        dataDict["ETHNICITY"] = data.ETHNICITY
        dataDict["GENDER"] = data.GENDER
        dataDict["LOCATION"] = data.LOCATION
        dataDict["SAMPLEID"] = data.SAMPLEID
        allData.append(dataDict)

    return jsonify(allData)


@app.route("/api/samples/<sampleId>")
def retSample(sampleId):
    """Return a list dictionaries containing `otu_ids` and `sample_values`."""
    stmt = session.query(Samples).statement
    df = pd.read_sql_query(stmt, session.bind)

    # Make sure that the sample was found in the columns, else throw an error
    if sampleId not in df.columns:
        return jsonify(f"Error! Sample: {sampleId} Not Found!"), 400

    # remove header
    # df = df[1:]

    # Return any sample values greater than 1
    df = df[df[sampleId] > 1]

    # Sort the results by sample in descending order
    df = df.sort_values(by=sampleId, ascending=0)

    # Format the data to send as json
    data = [{
        "otu_ids": df[sampleId].index.values.tolist(),
        "sample_values": df[sampleId].values.tolist()
    }]

    return jsonify(data)

@app.route("/api/wfreq/<sampleId>")
def getFreq(sampleId):
    """Return Metadata for the SampleId"""
    vsampleId = sampleId[3:]
    results = session.query(SamplesMetadata.WFREQ, SamplesMetadata.SAMPLEID).filter(SamplesMetadata.SAMPLEID == vsampleId).all()

    allData = []
    for data in results:
        # print(passenger.name)
        dataDict = {}
        dataDict["Washing Frequency"] = data.WFREQ
        dataDict["SAMPLEID"] = data.SAMPLEID
        allData.append(dataDict)

    return jsonify(allData)

if __name__ == '__main__':
    app.run(debug=True)