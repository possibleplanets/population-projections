import pandas as pd
from . import fields

REMOTE_URL = "https://ghdx.healthdata.org/sites/default/files/record-attached-files/IHME_POP_2017_2100_POP_REFERENCE.zip"

def read_file(filename):
  # Parse the CSV.
  df = pd.read_csv(filename)
  # Filter rows by region, age and variant. Select population metric.
  projection_data = df.loc[ \
    (df[fields.SCENARIO]==fields.REFERENCE) & \
    (df[fields.REGION]==fields.WORLD) & \
    (df[fields.AGE_GROUP]==fields.ALL_AGES) & \
    (df[fields.METRIC]==fields.POPULATION) \
    ]
  # Sum male and female populations.
  summed_data = projection_data.groupby(
      by=[fields.YEAR],
      as_index=False
      ).agg({fields.VALUE: "sum"})
  # Extract the year and population columns.
  timeseries_data = summed_data.loc[
    :, [fields.YEAR, fields.VALUE]
    ]
  # Conform to schema.
  timeseries_data = timeseries_data.set_axis(
    ["year", "population"], axis="columns"
    ).astype(
    {"year":"float", "population":"float"}
    ).set_index("year")
  return timeseries_data