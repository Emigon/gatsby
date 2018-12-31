#!/usr/bin/python3

import requests
import io
import pandas as pd
from datetime import date

# afr S&P/ASX 300 stocks csv source
DAILY_URL = "https://www.afr.com/Tables/Share_Tables_Daily/{0}/GGsoda.csv"

date = date.today()
date = date.replace(day = date.day - 1) # only collect yesterdays data

# make sure the query date is a weekday
day = date.weekday()
if day in [5, 6]:
    date = date.replace(day = date.day - (day - 4))

# convert the date to afr's url format
datestring = date.strftime('%Y%m%d')

# retrieve the data set in pandas form
s = requests.get(DAILY_URL.format(datestring)).content
df = pd.read_csv(io.StringIO(s.decode('utf-8')),
                 skiprows = range(6),
                 index_col = False,
                 na_values = ['-']).set_index('ASX Code')

print(df)
