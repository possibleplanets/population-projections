import pandas as pd
from . import fields

REMOTE_URL = "https://raw.githubusercontent.com/guyabel/wcde/master/data-host-batch/2/pop-total.csv"

def read_file(filename):
  # Parse the CSV.
  df = pd.read_csv(filename)
  # Filter rows by region.
  projection_data = df.loc[ \
    (df[fields.REGION]==fields.WORLD) \
    ]
  # Extract the year and population columns.
  timeseries_data = projection_data.loc[
    :, [fields.YEAR, fields.POPULATION]
    ]
  # Conform to schema.
  timeseries_data = timeseries_data.set_axis(
    ["year", "population"], axis="columns"
    ).astype(
    {"year":"float", "population":"float"}
    ).set_index("year")
  # Convert from 1000s to number of people.
  timeseries_data["population"] *= 1000
  return timeseries_data