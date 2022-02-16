import pandas as pd
from sodapy import Socrata
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
results = client.get("c2es-76ed", limit=1000)

# Convert to pandas DataFrame
df = pd.DataFrame.from_records(results)
df['latitude'] = df['latitude'].astype(float)
df['longitude'] = df['longitude'].astype(float)

cols = ['issueddate', 'workclassgroup', 'latitude', 'longitude', 'contractorname', 'communityname',"originaladdress"]
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
Gengeojson = df_to_geojson(df_geo, cols)
print(Gengeojson)
import IPython
IPython.display.display({'application/geo+json': Gengeojson}, raw=True)
