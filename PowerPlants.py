#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  5 16:12:39 2019

@author: johnmartin
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#df = pd.read_csv('/Users/johnmartin/Documents/DataIncubator_Challenge/maestro.csv', delimiter = ',')
#df2 = pd.read_excel('/Users/johnmartin/Documents/DataIncubator_Challenge/PPD_PlanLevel.xlsx', index_col=0)
df = pd.read_csv('/Users/johnmartin/Documents/DataIncubator_Challenge/global_power_plant_database.csv', delimiter = ',')

#this block of code orders countries by ratio of global powerplants in ascending
#order
num_plants = len(df.country.index)
grouper = df.groupby('country_long').size().reset_index(name ='count')
series = [grouper.country_long, grouper['count'].to_frame()]
by_country = pd.concat(series, axis=1)
by_country['ratio'] = by_country['count'].apply(lambda x:x/num_plants)

max_ratio = max(by_country.ratio)
max_ratios = by_country[(by_country.ratio == max_ratio)]

by_ratio = by_country.sort_values('country_long', ascending=False)

#make a data frame that has totals, by country, of "green" energy plants
#green includes wind, biomass, solar, and geothermal.
green_plants = df[(df.fuel1=='Wind') | (df.fuel1=='Solar') |
                  (df.fuel1=='Biomass') | (df.fuel1=='Geothermal')]
grouper1 = green_plants.groupby('country_long').size().reset_index(name='count')
series1 = [grouper1.country_long, grouper1['count'].to_frame()]
green_by_country = pd.concat(series1, axis=1)

by_country_sub = by_country.loc[by_country['country_long'].isin(green_by_country['country_long'])]

#make a graph of countries that have "green" power plants with total number of 
#plants on the x-axis and ratio of green to total on y-axis.
N = len(green_by_country.index)
x_vals = [by_country_sub['count'].iloc[i] for i in range(N)]
y_vals = [green_by_country['count'][i]/by_country_sub['count'].iloc[i] for i in range(N)]

green_by_country['total'] = x_vals
green_by_country['ratio'] = y_vals

by_total = green_by_country.sort_values('total', ascending=True)

x_vals = green_by_country['total']
y_vals = green_by_country['ratio']

ax = by_total.plot.scatter(x='total', y='ratio', c='black')

#make a data frame with total number of power plants and total number of 
#plants that have been commissioned since 2014
after14 = df[(df.commissioning_year >= 2014)]
grouper = after14.groupby('country_long').size().reset_index(name='count')
series = [grouper.country_long, grouper['count'].to_frame()]
after14_country = pd.concat(series, axis=1)

by_country_sub = by_country.loc[by_country['country_long'].isin(after14['country_long'])]

by_country_sub = by_country_sub.sort_values('country_long', ascending=True)
after14_country = after14_country.sort_values('country_long', ascending=True)

after14_country['total'] = [by_country_sub['count'].iloc[i] for i in range(len(by_country_sub.index))]

ax = after14_country.plot.scatter(x='total',y='count', c='black')
