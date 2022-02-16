
import os
import re
import requests
import json


from flask import Flask, session
from flask import render_template, request
from flask import request
from flask_session import Session
import pandas as pd
from sodapy import Socrata

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def index():


    # Unauthenticated client only works with public data sets. Note 'None'
    # in place of application token, and no username or password:
    client = Socrata("data.calgary.ca", None)

    # Example authenticated client (needed for non-public datasets):
    # client = Socrata(data.calgary.ca,
    #                  MyAppToken,
    #                  userame="user@example.com",
    #                  password="AFakePassword")

    # First 2000 results, returned as JSON from API / converted to Python list of
    # dictionaries by sodapy.
    results = client.get("c2es-76ed", limit=2000)

    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(results)
    return render_template("Mappingpage.html")
