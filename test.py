import pandas as pd
import re
from pprint import pprint

fac = "Accra Site CHPS   (4083)"

data = pd.read_csv('Health_Facilities.csv')
nests = data['NEST_NAME'].unique().tolist()
nests.sort()

facilities = {}

for nest in nests:
    nests_facilities = data.loc[data['NEST_NAME'] == nest]
    facs = nests_facilities[["DELIVERY_SITE_NAME", "DELIVERY_SITE_ID"]].sort_values("DELIVERY_SITE_NAME")
    facilities[nest] = [f'{row[1]}  ({row[2]})' for row in facs.itertuples()]
is_unique = data["HEALTH_FACILITY_KEY"].nunique() == data["HEALTH_FACILITY_KEY"].count()

print(is_unique)