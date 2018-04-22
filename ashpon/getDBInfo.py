import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///belly_button_biodiversity.sqlite")
session = Session(engine)


# let's reflect the base tables
Base = automap_base()
Base.prepare(engine, reflect=True)

# let's get the table available - comment out for deployment
print(Base.classes.keys())
# otu, samples, samples_metadata

# create classed for the tables available
Otu = Base.classes.otu
Samples = Base.classes.samples
SamplesMetadata = Base.classes.samples_metadata

# # get the data sample - comment this out for deployment
# OtuFirstRow = session.query(Otu).first()
# print('Otu Dictionary')
# print(OtuFirstRow.__dict__)

# # get the data sample - comment this out for deployment
SamplesFirstRow = session.query(Samples).first()
print('Samples Dictionary')
# print(SamplesFirstRow.__dict__)

for aRow in (SamplesFirstRow.__dict__):
	print(aRow)

# # get the data sample - comment this out for deployment
# MetaFirstRow = session.query(SamplesMetadata).first()
# print('Samples Meta Dictionary')
# print(MetaFirstRow.__dict__)

# get some more data - remove for deployment
# vOtuId = input("Enter OTU ID between 1 thru 50")
# resStr = session.query(Otu.otu_id,Otu.lowest_taxonomic_unit_found).filter(Otu.otu_id == vOtuId).all()
# print(resStr)

# vsampleId = input("Enter SAMPLE ID between 940 thru 1601")
# resStr = session.query(SamplesMetadata.SAMPLEID,SamplesMetadata.ETHNICITY).filter(SamplesMetadata.SAMPLEID == vsampleId).all()
# print(resStr)

# # for aRow in resStr
# #      print(aRow)

# for aRow in session.query(Samples.otu_id,Samples.BB_940,Samples.BB_941,Samples.BB_943,Samples.BB_944, Samples.BB_945, Samples.BB_946).limit(15):
#      print(aRow)

# first_extant = session.query(MammalMasses.species, MammalMasses.status, MammalMasses.comb_mass_g).\
#     filter(MammalMasses.status == 'extant').\
#     first()
# print(first_extant)