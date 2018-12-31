#!/usr/bin/python3

import requests
import io
import pandas as pd
from datetime import date
from alpha_vantage.timeseries import TimeSeries

# afr S&P/ASX 300 stocks csv source
AFR_DAILY_SOURCE = "https://www.afr.com/Tables/Share_Tables_Daily/{0}/GGsoda.csv"
TIMESERIES_SOURCE = "https://alphavantage.co/"

date = date.today()
date = date.replace(day = date.day - 1) # only collect yesterdays data

# make sure the query date is a weekday
day = date.weekday()
if day in [5, 6]:
    date = date.replace(day = date.day - (day - 4))

# convert the date to afr's url format
datestring = date.strftime('%Y%m%d')

# retrieve the data set in pandas form
s = requests.get(AFR_DAILY_SOURCE.format(datestring)).content
df = pd.read_csv(io.StringIO(s.decode('utf-8')),
                 skiprows = range(6),
                 index_col = False,
                 na_values = ['-']).set_index('ASX Code')

# filter the data
df = df.iloc[:2]

# retrieve timeseries stock data for each of the filtered stocks over the last
# 12 months
start_date = date.replace(year = date.year - 1)
ts = TimeSeries(output_format='pandas', indexing_type='date')
# NOTE: API key is required as environment variable: ALPHAVANTAGE_API_KEY

ts_dfs = {}
for symbol in df.index:
    try:
        data, metadata = ts.get_daily(symbol=symbol + '.AX', outputsize = 'full')
        data.index = pd.to_datetime(data.index, format='%Y-%m-%d')
        ts_dfs[symbol] = data.loc[start_date:]
    except:
        pass
