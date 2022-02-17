#ENGO 651 Lab 2
#Andrew Symes
#UCID 30033743

#imports, More than is needed but ok
import os
import re
import requests
import json
from flask import Flask, session
from flask import render_template, request
from flask import request
from flask_session import Session
import pandas as pd
#install sodapy
from sodapy import Socrata

app = Flask(__name__)

#Homepage, and only page
@app.route("/", methods = ["GET", "POST"])
def index():
    #Code modified from Socrata tutorial available at https://dev.socrata.com/blog/2014/11/04/data-visualization-with-python.html
    # Unauthenticated client only works with public data sets. Note 'None'
    # in place of application token, and no username or password:
    #Data information provided through https://dev.socrata.com/foundry/data.calgary.ca/c2es-76ed
    client = Socrata("data.calgary.ca", None)

    # Example authenticated client (needed for non-public datasets):
    # client = Socrata(data.calgary.ca,
    #                  MyAppToken,
    #                  userame="user@example.com",
    #                  password="AFakePassword")

    # First 2000 results, returned as JSON from API / converted to Python list of
    # dictionaries by sodapy.
    if request.method == "GET":
        query = ("https://data.calgary.ca/resource/c2es-76ed.json?")
            #"&issueddate=2019-09-09")
        results = pd.read_json(query)

    if request.method == "POST":
         ub = request.form.get("ub")
         lb = request.form.get("lb")
         query = ("https://data.calgary.ca/resource/c2es-76ed.json?"
            f"$where=issueddate+>+'{lb}'+and+issueddate+<+'{ub}'")
             #f"&issueddate={lb}")
         results = pd.read_json(query)
         #results = client.get("c2es-76ed", limit=2000)
         print(lb)

    # Convert to pandas DataFrame
    df = pd.DataFrame.from_records(results)
    df['latitude'] = df['latitude'].astype(float)
    df['longitude'] = df['longitude'].astype(float)

#Bump same place values a little bit to make it nicer.
#This is my simple approach to requirement 4
    for i in range(0,len(df['latitude'])):
        for j in range(0,len(df['longitude'])):
            if df['latitude'][i] == df['latitude'][j]:
                if df['longitude'][i] == df['longitude'][j]:
                    df['longitude'][j] = df['longitude'][j] + 0.01



    cols = ['issueddate', 'workclassgroup', 'latitude', 'longitude', 'contractorname', 'communityname',"originaladdress"]
    #cols = ['latitude', 'longitude','communityname',"originaladdress"]

    df_subset = df[cols]
    df_geo = df_subset.dropna(subset=['latitude', 'longitude'], axis=0, inplace=False)

    def df_to_geojson(df, properties, lat='latitude', lon='longitude'):
        # create a new python dict to contain our geojson data, using geojson format
        geojson = {'type':'FeatureCollection', 'features':[]}

        # loop through each row in the dataframe and convert each row to geojson format
        for _, row in df.iterrows():
            # create a feature template to fill in
            feature = {'type':'Feature',
                       'properties':{},
                       'geometry':{'type':'Point',
                                   'coordinates':[]}}

            # fill in the coordinates
            feature['geometry']['coordinates'] = [row[lon],row[lat]]

            # for each column, get the value and add it as a new feature property
            for prop in properties:
                feature['properties'][prop] = row[prop]

            # add this feature (aka, converted dataframe row) to the list of features inside our dict
            geojson['features'].append(feature)

        return geojson

    cols = ['issueddate', 'workclassgroup', 'contractorname', 'communityname',"originaladdress"]
    #cols = ['latitude', 'longitude','communityname',"originaladdress"]

    Gengeojson = df_to_geojson(df_geo, cols)

    return render_template("Mappingpage.html",Gengeojson=Gengeojson)

#the above code transforming the query to geoJSON was adapted from the code providded at
#https://notebook.community/captainsafia/nteract/applications/desktop/example-notebooks/pandas-to-geojson







#https://notebook.community/captainsafia/nteract/applications/desktop/example-notebooks/pandas-to-geojson

print("hello")
