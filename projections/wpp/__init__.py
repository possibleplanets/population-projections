import pandas as pd
from . import fields

REMOTE_URL = "https://population.un.org/wpp/Download/Files/1_Indicators%20(Standard)/EXCEL_FILES/1_General/WPP2022_GEN_F01_DEMOGRAPHIC_INDICATORS_COMPACT_REV1.xlsx"

def read_file(filename):
  # Parse the Excel sheet and header row.
  df = pd.read_excel(
    filename,
    sheet_name=fields.SHEET_NAME,
    header=fields.HEADER_ROW
    )
  # Filter the dataframe rows by region and variant.
  projection_data = df.loc[ \
    (df[fields.REGION] == fields.WORLD) & \
    (df[fields.VARIANT] == fields.MEDIUM) \
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