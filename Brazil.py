#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import macrobond_data_api as mda
import matplotlib.pyplot as plt

from macrobond_data_api.common.types import StartOrEndPoint
from macrobond_data_api.common.types import SeriesEntry
from macrobond_data_api.common.enums import SeriesFrequency
from macrobond_data_api.common.enums import SeriesToHigherFrequencyMethod
from macrobond_data_api.common.enums import SeriesToLowerFrequencyMethod
from macrobond_data_api.common.enums import CalendarMergeMode
from macrobond_data_api.common.enums import SeriesMissingValueMethod



################## Nominal GDP in USD #################
# Retriving the data - single series query:
series = mda.get_one_series('brnaac1005')
df = series.values_to_pd_data_frame()

# Data Manipulation and Calculations:
df['year'] = df['date'].apply(lambda x: x.year) # creating a column with just the year for filtering
df=df.loc[df['year']>2007] # filtering dataframe to include data only after 2007 (to match format in existing macrobond sheet)
df['value'] = df['value'].apply(lambda x: x/1000000000) # creating column with billions as unit for better readability and to match Macrobond desktop format

# creating the graphic using the above data: 
fig = plt.figure(figsize=(15, 10)) # creating the figure
ax = fig.add_subplot(111) # adding the ax space where actual plot will exist
ax.plot(df['date'], df['value'], 'red') # plotting nominal gdp against time in line plot format, setting the line color
ax.set_ylabel('USD, billion', ha='left', y=1, rotation=0, labelpad=0) # adding y axis label to the top of the figure to match Macrobond desktop formatting
ax.yaxis.set_label_position("right") # setting the y axis label to display on the right of the figure
ax.yaxis.tick_right() # moving the y axis to the right of the figure to match Macrobond desktop format
ax.grid(axis='y') # adding major gridlines
plt.title('Brazil, Nominal GDP in USD', loc='left') # adding title and specifying what location we want it to display in
fig.show() # if you are working in jupyter notebooks you don't always need to add this command in order for the figure display, but it is best practice as otherwise figures won't automatically display when run in a python text file for example




# In[5]:


################ Real GDP y/y % change: ##################
# Retriving the data - single series query:
series = mda.get_one_series('brnaac1005')
df = series.values_to_pd_data_frame()


# Data Manipulation and Calculations:
df['year'] = df['date'].apply(lambda x: x.year) # creating a column with just the year for filtering
df['y/y change'] = df['value'].pct_change(12) # calculating percent change, for this function you have to be aware of the frequency, since we have a montly frequency and want a yearly percent change, set the percent change paramter as 12 (calculating percetn change every 12 inctances, or in this case every 12 months)
df=df.loc[df['year']>2008] # filtering dataframe 
to include data only after 2008 (to match format in existing macrobond sheet)

# creating the graphic using the above data: 
fig = plt.figure(figsize=(15, 10)) # creating the figure
ax = fig.add_subplot(111) # adding the ax space where actual plot will exist
ax.plot(df['date'], df['y/y change'], 'red')  # plotting real gdp y/y against time in line plot format, setting the line color
ax.set_ylabel('Percent', ha='left', y=1, rotation=0, labelpad=0) # adding y axis label to the top of the figure to match Macrobond desktop formatting
ax.yaxis.set_label_position("right") # setting the y axis label to display on the right of the figure
ax.yaxis.tick_right() # moving the y axis to the right of the figure to match Macrobond desktop format
ax.grid(axis='y') # adding major gridlines
plt.title('Brazil: Reserve Assets', loc='left') # adding title and specifying what location we want it to display in
fig.show() # if you are working in jupyter notebooks you don't always need to add this command in order for the figure display, but it is best practice as otherwise figures won't automatically display when run in a python text file for example


# In[7]:


############# Reserve Assets ################
# Retriving the data - single series query:
series = mda.get_one_series('brfofi1030')
df = series.values_to_pd_data_frame()

# Data Manipulation and Calculations:
df['year'] = df['date'].apply(lambda x: x.year) # creating a column with just the year for filtering
df=df.loc[df['year']>2009] # filtering dataframe to include data only after 2009 (to match format in existing macrobond sheet)
df['value'] = df['value'].apply(lambda x: x/1000000000) # creating column with billions as unit for better readability and to match Macrobond desktop format

# creating the graphic using the above data: 
fig = plt.figure(figsize=(15, 10)) # creating the figure
ax = fig.add_subplot(111) # adding the ax space where actual plot will exist
ax.plot(df['date'], df['value'], 'red')  # plotting reserve assets against time in line plot format, setting the line color
ax.set_ylabel('USD, billion', ha='left', y=1, rotation=0, labelpad=0) # adding y axis label to the top of the figure to match Macrobond desktop formatting
ax.yaxis.set_label_position("right") # setting the y axis label to display on the right of the figure
ax.yaxis.tick_right() # moving the y axis to the right of the figure to match Macrobond desktop format
ax.grid(axis='y') # adding major gridlines
plt.title('Brazil: Reserve Assets', loc='left') # adding title and specifying what location we want it to display in
fig.show() # if you are working in jupyter notebooks you don't always need to add this command in order for the figure display, but it is best practice as otherwise figures won't automatically display when run in a python text file for example




# In[9]:


########## Imports and Exports #################
# Checking timeseries natural frequency:
print(mda.get_one_entity('brtrad1153').metadata_to_pd_series()['Frequency'])
print(mda.get_one_entity('brtrad1015').metadata_to_pd_series()['Frequency'])
# after printing the above, we see that the two frequencies have the same natural frequencies so frequency is already aligned

# Retriving the data - multi series, unified query:
data_frame = mda.get_unified_series(
    SeriesEntry(missing_value_method=SeriesMissingValueMethod.NONE, name="brtrad1153"), # specifying the first timeseries we want to retrieve, as well as the missing value method we want to apply to it
    SeriesEntry(missing_value_method=SeriesMissingValueMethod.NONE, name="brtrad1015"), # specifying the first timeseries we want to retrieve, as well as the missing value method we want to apply to it
    currency="USD", # aligning the series currencies
    calendar_merge_mode=CalendarMergeMode.AVAILABLE_IN_ALL,
    start_point=StartOrEndPoint.data_in_all_series(), # including all dates that are available for the timeseries in the returned dataframe
    end_point=StartOrEndPoint.data_in_all_series(), # including all dates that are available for the timeseries in the returned dataframe
).to_pd_data_frame()
data_frame.columns = [
    "Date",
    "Imports",
    "Exports",
]
data_frame = data_frame.reset_index().drop('index', axis=1)


# In[11]:


# Data Manipulation and Calculations:
data_frame['year'] = data_frame['Date'].apply(lambda x: x.year) # creating a column with just the year for filtering
data_frame = data_frame.loc[data_frame['year']>2011] # filtering dataframe to include data only after 2011 (to match format in existing macrobond sheet)
data_frame['imports bil'] = data_frame['Imports'].apply(lambda x: x/1000000000) # creating column with billions as unit for better readability and to match Macrobond desktop format
data_frame['exports bil'] = data_frame['Exports'].apply(lambda x: x/1000000000) # creating column with billions as unit for better readability and to match Macrobond desktop format

# creating the graphic using the above data: 
fig = plt.figure(figsize=(15, 10)) # creating the figure
ax = fig.add_subplot(111) # adding the ax space where actual plot will exist
ax.plot(data_frame['Date'], data_frame['imports bil'], 'blue', label='Imports') # *** put a '#' at the start of this line if you don't want IMPORTS to be included in the figure
ax.plot(data_frame['Date'], data_frame['exports bil'], 'red', label='Exports') # *** put a '#' at the start of this line if you don't want EXPORTS to be included in the figure
ax.set_ylabel('USD, billion', ha='left', y=1, rotation=0, labelpad=0) # adding y axis label to the top of the figure to match Macrobond desktop formatting
ax.yaxis.set_label_position("right") # setting the y axis label to display on the right of the figure
ax.yaxis.tick_right() # moving the y axis to the right of the figure to match Macrobond desktop format
ax.legend(loc='upper left') # {choose from lower left / upper left / lower right / upper right}
ax.grid(axis='y') # adding major gridlines
plt.title('Brazil: Imports and Exports', loc='left') # adding title and specifying what location we want it to display in
fig.show() # if you are working in jupyter notebooks you don't always need to add this command in order for the figure display, but it is best practice as otherwise figures won't automatically display when run in a python text file for example


# In[13]:


################ Trade balance in USD as % of GDP ##############
# Checking timeseries natural frequency:
print(mda.get_one_entity('brtrad1153').metadata_to_pd_series()['Frequency'])
print(mda.get_one_entity('brtrad1015').metadata_to_pd_series()['Frequency'])
print(mda.get_one_entity('brnaac1005').metadata_to_pd_series()['Frequency'])
# after printing the above, we see that the three frequencies have the same natural frequencies so frequency is already aligned

# Retriving the data - multi series, unified query:
data_frame = mda.get_unified_series(
    SeriesEntry(missing_value_method=SeriesMissingValueMethod.NONE, name="brtrad1153"),
    SeriesEntry(missing_value_method=SeriesMissingValueMethod.NONE, name="brtrad1015"),
    SeriesEntry(missing_value_method=SeriesMissingValueMethod.NONE, name="brnaac1005"),
    currency="USD", # aligning the series currencies
    calendar_merge_mode=CalendarMergeMode.AVAILABLE_IN_ALL,
    start_point=StartOrEndPoint.data_in_all_series(),
    end_point=StartOrEndPoint.data_in_all_series(),
).to_pd_data_frame()
data_frame.columns = [
    "Date",
    "Imports",
    "Exports",
    "GDP",
]
data_frame = data_frame.reset_index().drop('index', axis=1)

# Data Manipulation and Calculations:
data_frame['year'] = data_frame['Date'].apply(lambda x: x.year) # creating a column with just the year for filtering
data_frame = data_frame.loc[data_frame['year']>2011] # filtering dataframe to include data only after 2011 (to match format in existing macrobond sheet)
data_frame['trade balance'] = (data_frame['Exports'] - data_frame['Imports'])/data_frame['GDP'] *100 # subracting imports from exports to get trade balance, dividing by gdp to get trade balance percent of gdp

# creating the graphic using the above data: 
fig = plt.figure(figsize=(15, 10)) # creating the figure
ax = fig.add_subplot(111) # adding the ax space where actual plot will exist
ax.plot(data_frame['Date'], data_frame['trade balance'], 'red') # plotting trade balance against time in line plot format, setting the line color
ax.set_ylabel('percent', ha='left', y=1, rotation=0, labelpad=0)# adding y axis label to the top of the figure to match Macrobond desktop formatting
ax.yaxis.set_label_position("right") # setting the y axis label to display on the right of the figure
ax.yaxis.tick_right() # moving the y axis to the right of the figure to match Macrobond desktop format
ax.grid(axis='y') # adding major gridlines
plt.title('Trade Balance in USD as % of GDP', loc='left') # adding title and specifying what location we want it to display in
fig.show() # if you are working in jupyter notebooks you don't always need to add this command in order for the figure display, but it is best practice as otherwise figures won't automatically display when run in a python text file for example


# In[15]:


########### Inflation: y/y, 3m/3m, 1m/1m ###########
# Retriving the data - single series query:
series = mda.get_one_series('brpric1011')
series.metadata_to_pd_series() # from the metadata we can see that the frequency of the series is monthly, so for y/y, 3m/3m and 1m/1m pct changes we need to use 12, 3, and 1, respectively (speciff change in time period over months). 
df = series.values_to_pd_data_frame()

# Data Manipulation and Calculations:
df['year'] = df['date'].apply(lambda x: x.year) # creating a column with just the year for filtering
df['y/y'] = df['value'].pct_change(12) 
df['3m/3m'] = df['value'].pct_change(3)
df['1m/1m'] = df['value'].pct_change(1)

# creating the graphic using the above data: 
fig = plt.figure(figsize=(15, 10)) # creating the figure
ax = fig.add_subplot(111) # adding the ax space where actual plot will exist
ax.plot(df['date'], df['y/y'], 'blue', label='Y/Y pct change') # *** put a '#' at the start of this line if you don't want IMPORTS to be included in the figure
ax.plot(df['date'], df['3m/3m'], 'red', label='3m/3m pct change') # *** put a '#' at the start of this line if you don't want EXPORTS to be included in the figure
ax.plot(df['date'], df['1m/1m'], 'green', label='1m/1m pct change') # *** put a '#' at the start of this line if you don't want EXPORTS to be included in the figure
ax.set_ylabel('percent', ha='left', y=1, rotation=0, labelpad=0) # adding y axis label to the top of the figure to match Macrobond desktop formatting
ax.yaxis.set_label_position("right") # setting the y axis label to display on the right of the figure
ax.yaxis.tick_right() # moving the y axis to the right of the figure to match Macrobond desktop format
ax.legend(loc='upper left') # {choose from lower left / upper left / lower right / upper right}
ax.grid(axis='y') # adding major gridlines
plt.title('Brazil, Inflation: y/y, 3m/3m, 1m/1m', loc='left') # adding title and specifying what location we want it to display in
fig.show() # if you are working in jupyter notebooks you don't always need to add this command in order for the figure display, but it is best practice as otherwise figures won't automatically display when run in a python text file for example





# In[17]:


######## Current Account as % of GDP ###########
# Checking timeseries natural frequency:
print(mda.get_one_entity('brbopa1000').metadata_to_pd_series()['Frequency'])
print(mda.get_one_entity('brnaac1005').metadata_to_pd_series()['Frequency'])
# after printing the above, we see that the two frequencies have the same natural frequencies so frequency is already aligned

# Retriving the data - multi series, unified query:
data_frame = mda.get_unified_series(
    SeriesEntry(missing_value_method=SeriesMissingValueMethod.NONE, name="brbopa1000"),
    SeriesEntry(missing_value_method=SeriesMissingValueMethod.NONE, name="brnaac1005"),
    currency="USD", # aligning the series currencies
    calendar_merge_mode=CalendarMergeMode.AVAILABLE_IN_ALL,
    start_point=StartOrEndPoint.data_in_all_series(),
    end_point=StartOrEndPoint.data_in_all_series(),
).to_pd_data_frame()
data_frame.columns = [
    "Date",
    "Current Account",
    "GDP",
]
data_frame = data_frame.reset_index().drop('index', axis=1)

# Data Manipulation and Calculations:
data_frame['curr_pct_gdp'] = data_frame['Current Account']/data_frame['GDP']*100 # calculating percent of gdp

# creating the graphic using the above data: 
fig = plt.figure(figsize=(15, 10)) # creating the figure
ax = fig.add_subplot(111) # adding the ax space where actual plot will exist
ax.plot(data_frame['Date'], data_frame['curr_pct_gdp'], 'red')  # plotting current account % gdp against time in line plot format, setting the line color
ax.set_ylabel('Percent', ha='left', y=1, rotation=0, labelpad=0) # adding y axis label to the top of the figure to match Macrobond desktop formatting
ax.yaxis.set_label_position("right") # setting the y axis label to display on the right of the figure
ax.yaxis.tick_right() # moving the y axis to the right of the figure to match Macrobond desktop format
ax.grid(axis='y') # adding major gridlines
plt.title('Current Account as % of GDP', loc='left') # adding title and specifying what location we want it to display in
fig.show() # if you are working in jupyter notebooks you don't always need to add this command in order for the figure display, but it is best practice as otherwise figures won't automatically display when run in a python text file for example




# In[19]:


########### Central Bank Inflation Forecast ################
# Retriving the data - single series query:
series = mda.get_one_series('brrate0102')
df = series.values_to_pd_data_frame()

# Data Manipulation and Calculations:
df['year'] = df['date'].apply(lambda x: x.year) # creating a column with just the year for filtering
df=df.loc[df['year']>1999] # filtering dataframe to include data only after 1999 (to match format in existing macrobond sheet)

# creating the graphic using the above data: 
fig = plt.figure(figsize=(15, 10)) # creating the figure
ax = fig.add_subplot(111) # adding the ax space where actual plot will exist
ax.plot(df['date'], df['value'], 'red') # plotting central bank inflation against time in line plot format, setting the line color
ax.set_ylabel('Percent', ha='left', y=1, rotation=0, labelpad=0) # adding y axis label to the top of the figure to match Macrobond desktop formatting
ax.yaxis.set_label_position("right") # setting the y axis label to display on the right of the figure
ax.yaxis.tick_right() # moving the y axis to the right of the figure to match Macrobond desktop format
ax.grid(axis='y') # adding major gridlines
plt.title('Central Bank Inflation Forecast', loc='left') # adding title and specifying what location we want it to display in
fig.show() # if you are working in jupyter notebooks you don't always need to add this command in order for the figure display, but it is best practice as otherwise figures won't automatically display when run in a python text file for example


# In[21]:


################ Primary Budget Deficit as % of GDP ###########
# Checking timeseries natural frequency:
print(mda.get_one_entity('brgpfi1066').metadata_to_pd_series()['Frequency'])
print(mda.get_one_entity('brnaac1005').metadata_to_pd_series()['Frequency'])
# after printing the above, we see that the two frequencies have the same natural frequencies so frequency is already aligned

# Retriving the data - multi series, unified query:
data_frame = mda.get_unified_series(
    SeriesEntry(missing_value_method=SeriesMissingValueMethod.NONE, name="brgpfi1066"),
    SeriesEntry(missing_value_method=SeriesMissingValueMethod.NONE, name="brnaac1005"),
    currency="USD", # aligning the series currencies
    calendar_merge_mode=CalendarMergeMode.AVAILABLE_IN_ALL,
    start_point=StartOrEndPoint.data_in_all_series(),
    end_point=StartOrEndPoint.data_in_all_series(),
).to_pd_data_frame()
data_frame.columns = [
    "Date",
    "prim_budg",
    "GDP",
]
data_frame = data_frame.reset_index().drop('index', axis=1)

# Data Manipulation and Calculations:
data_frame['prim_pct_gdp'] = data_frame['prim_budg']/data_frame['GDP']*100 # calculating percent of gdp
data_frame['year'] = data_frame['Date'].apply(lambda x: x.year) # creating a column with just the year for filtering
data_frame = data_frame.loc[data_frame['year']>2015] # filtering dataframe to include data only after 2014 (to match format in existing macrobond sheet)

# creating the graphic using the above data: 
fig = plt.figure(figsize=(15, 10)) # creating the figure
ax = fig.add_subplot(111) # adding the ax space where actual plot will exist
ax.plot(data_frame['Date'], data_frame['prim_pct_gdp'], 'red') # plotting primary budget deficit % gdp against time in line plot format, setting the line color
ax.set_ylabel('Percent', ha='left', y=1, rotation=0, labelpad=0) # adding y axis label to the top of the figure to match Macrobond desktop formatting
ax.yaxis.set_label_position("right") # setting the y axis label to display on the right of the figure
ax.yaxis.tick_right() # moving the y axis to the right of the figure to match Macrobond desktop format
ax.grid(axis='y') # adding major gridlines
plt.title('Primary Budget Deficit in USD as % of GDP', loc='left') # adding title and specifying what location we want it to display in
fig.show() # if you are working in jupyter notebooks you don't always need to add this command in order for the figure display, but it is best practice as otherwise figures won't automatically display when run in a python text file for example


# In[23]:


######### Budget Deficit in USD as % of GDP ##############
# Checking timeseries natural frequency:
print(mda.get_one_entity('brgpfi1098').metadata_to_pd_series()['Frequency'])
print(mda.get_one_entity('brnaac1005').metadata_to_pd_series()['Frequency'])
# after printing the above, we see that the two frequencies have the same natural frequencies so frequency is already aligned

# Retriving the data - multi series, unified query:
data_frame = mda.get_unified_series(
    SeriesEntry(missing_value_method=SeriesMissingValueMethod.NONE, name="brgpfi1098"),
    SeriesEntry(missing_value_method=SeriesMissingValueMethod.NONE, name="brnaac1005"),
    currency="USD", # aligning the series currencies
    calendar_merge_mode=CalendarMergeMode.AVAILABLE_IN_ALL,
    start_point=StartOrEndPoint.data_in_all_series(),
    end_point=StartOrEndPoint.data_in_all_series(),
).to_pd_data_frame()
data_frame.columns = [
    "Date",
    "gov_budg",
    "GDP",
]
data_frame = data_frame.reset_index().drop('index', axis=1)

# Data Manipulation and Calculations:
data_frame['budg_pct_gdp'] = data_frame['gov_budg']/data_frame['GDP']*100 # calculating percent of gdp
data_frame['year'] = data_frame['Date'].apply(lambda x: x.year) # creating a column with just the year for filtering
data_frame = data_frame.loc[data_frame['year']>2014] # filtering dataframe to include data only after 2014 (to match format in existing macrobond sheet)

# creating the graphic using the above data: 
fig = plt.figure(figsize=(15, 10)) # creating the figure
ax = fig.add_subplot(111) # adding the ax space where actual plot will exist
ax.plot(data_frame['Date'], data_frame['budg_pct_gdp'], 'red') # plotting budget deficit % gdp against time in line plot format, setting the line color
ax.set_ylabel('Percent', ha='left', y=1, rotation=0, labelpad=0) # adding y axis label to the top of the figure to match Macrobond desktop formatting
ax.yaxis.set_label_position("right") # setting the y axis label to display on the right of the figure
ax.yaxis.tick_right() # moving the y axis to the right of the figure to match Macrobond desktop format
ax.grid(axis='y') # adding major gridlines
plt.title('Budget Deficit in USD as % of GDP', loc='left') # adding title and specifying what location we want it to display in
fig.show() # if you are working in jupyter notebooks you don't always need to add this command in order for the figure display, but it is best practice as otherwise figures won't automatically display when run in a python text file for example




# In[25]:


############ General Government Debt as % of GDP ##############
# Checking timeseries natural frequency:
print(mda.get_one_entity('brfofi1043').metadata_to_pd_series()['Frequency'])
print(mda.get_one_entity('brnaac1005').metadata_to_pd_series()['Frequency'])
# after printing the above, we see that the two frequencies have different natural frequencies, so we need to either choose to work in the higher or lower frequency and ajust the other freqyency accordingly

# Retriving the data - multi series, unified query:
data_frame = mda.get_unified_series(
    SeriesEntry(missing_value_method=SeriesMissingValueMethod.NONE, name="brfofi1043"), # specifying the first timeseries we want to retrieve, as well as the missing value method we want to apply to it
    SeriesEntry(missing_value_method=SeriesMissingValueMethod.NONE, name="brnaac1005"), # specifying the first timeseries we want to retrieve, as well as the missing value method we want to apply to it
    SeriesEntry(missing_value_method=SeriesToHigherFrequencyMethod.LINEAR_INTERPOLATION, name="brfofi1043"), # specifying to use linear interpolation to retrieve Brazil Foreign Debt in a higher frequency than it is naturally recorded in
    currency="USD", # aligning the series currencies
    calendar_merge_mode=CalendarMergeMode.AVAILABLE_IN_ALL,
    start_point=StartOrEndPoint.data_in_all_series(), # including all dates that are available for the timeseries in the returned dataframe
    end_point=StartOrEndPoint.data_in_all_series(), # including all dates that are available for the timeseries in the returned dataframe
).to_pd_data_frame()
data_frame.columns = [
    "Date",
    "gov_budg",
    "GDP",
]
data_frame = data_frame.reset_index().drop('index', axis=1) # reseting the index of the dataframe 

# Data Manipulation and Calculations:
data_frame['budg_pct_gdp'] = data_frame['gov_budg']/data_frame['GDP']*100 # calculating general government debt as a % of GDP and adding it as a new column to the dataframe
data_frame['year'] = data_frame['Date'].apply(lambda x: x.year) # creating a column with just the year for filtering
data_frame = data_frame.loc[data_frame['year']>2006] # filtering dataframe to include data only after 2006 (to match format in existing macrobond sheet)

# creating the graphic using the above data: 
fig = plt.figure(figsize=(15, 10)) # creating the figure
ax = fig.add_subplot(111) # adding the ax space where actual plot will exist
ax.plot(data_frame['Date'], data_frame['budg_pct_gdp'], 'red') # plotting gov debt % gdp against time in line plot format, setting the line color
ax.set_ylabel('Percent', ha='left', y=1, rotation=0, labelpad=0) # adding y axis label to the top of the figure to match Macrobond desktop formatting
ax.yaxis.set_label_position("right") # setting the y axis label to display on the right of the figure
ax.yaxis.tick_right() # moving the y axis to the right of the figure to match Macrobond desktop format
ax.grid(axis='y') # adding major gridlines
plt.title('General Government Debt as % of GDP', loc='left') # adding title and specifying what location we want it to display in
fig.show() # if you are working in jupyter notebooks you don't always need to add this command in order for the figure display, but it is best practice as otherwise figures won't automatically display when run in a python text file for example

