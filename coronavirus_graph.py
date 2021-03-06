# -*- coding: utf-8 -*-
"""coronavirus-graph.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Jq_jrjHEpZS5AJ-7NXrhE91T96AT4Fb-
"""

import requests
import pandas as pd
import io
import datetime
import pytz
import time
from jinja2 import Template, Environment, FileSystemLoader

# Get original data from CSSE github

url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/"\
      "csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
      
r = requests.get(url)

# create original dataframe.
df = pd.read_csv(io.StringIO(r.text))

# Original dataframe is made column by date.
df

# Clone original dataframe and delete latitude/longitude column
df2 = df[:]
del df2["Lat"]
del df2["Long"]
df2

# unpivot
df3 = df2.melt(id_vars=["Province/State", "Country/Region"])

# convert date string to date type.
df3["date"] = pd.to_datetime(df3["variable"], format="%m/%d/%y")
del df3["variable"]
df3

# Summarize by country
df4 = df3.groupby(["Country/Region", "date"]).sum()
df4

# create pivot table by date/country
df5=df4.pivot_table(values="value", index="date", columns="Country/Region")
df5

# make coutry list sorted by cases at last day
lastday = df.columns[-1]
top5_countries = set(df[:].sort_values(lastday, ascending=False)[:5]["Country/Region"].values)

countries = list(top5_countries | {"Japan", "Spain", "United Kingdom", "France", "Italy", "US", "Korea, South", "Philippines", "Singapore", "Germany", "Russia"})
countries.sort(key=lambda c:df5.iloc[-1][c], reverse=True)
countries

# format timestamp text
local_tz = pytz.timezone('Asia/Tokyo')
now = datetime.datetime.now().astimezone(local_tz)
datestring = "{0:%Y-%m-%d %H:%M} (JST)".format(now)
datestring

# Extract data from Feb 20th 2020
# Draw graph
from_date = "2020-02-10"
plt = df5[countries][df5.index >= from_date].plot(
    logy=True, 
    figsize=(15,10),
    title="COVID-19 Cases",
)
plt.set_ylabel("Cumulative cases\n(Logarithmic scale)")
plt.figure.text(0.30, 0.80, "Data from https://github.com/CSSEGISandData/COVID-19", size=10, fontfamily="Monospace")
plt.figure.text(0.30, 0.78, "Source code: https://bit.ly/2QSj1Wl", size=10, fontfamily="Monospace")
plt.figure.text(0.30, 0.83, "Last Update: "+ datestring, size=24)
plt.figure.savefig("dist/a.png")

df6 = df4.copy()
df6["relative_date"] = -1

# set relative date column
# create new date frame(index=relative_date)

rel_df = pd.DataFrame()
for country in countries:
  dfc = df6.loc[country]
  rd = 0
  for index, row in dfc.iterrows():
    if row.value > 100:
      row.relative_date = rd
      rd += 1
  drop_index = dfc[dfc["relative_date"] == -1].index
  dfc=dfc.drop(index=drop_index)
  rel_df[country] = pd.Series(dfc.value.values, dfc.relative_date.values)
rel_df

# draw graph
plt = rel_df.plot(logy=True,
    figsize=(15,10),
    title="COVID-19 Cases since place's first day wih 100 more cumulative cases")
plt.set_ylabel("Cumulative cases\n(Logarithmic scale)")
plt.set_xlabel("Days since place's first day with 100 or more cases")
plt.figure.text(0.30, 0.80, "Data from https://github.com/CSSEGISandData/COVID-19", size=10, fontfamily="Monospace")
plt.figure.text(0.30, 0.78, "Source code: https://bit.ly/2QSj1Wl", size=10, fontfamily="Monospace")
plt.figure.text(0.30, 0.83, "Last Update: "+datestring, size=24)
plt.figure.savefig("dist/b.png")

env = Environment(loader=FileSystemLoader("dist"))
template = env.get_template("template.html")
with open("dist/index.html", "w") as f:
    f.write(template.render(tstamp=datestring, tstampserial=int(time.time())))
