import pandas as pd
import datetime
import math

def convert(str, days):
    # HACK: for nan(-) use -1
    if(str == "-"):
        days.append(-1)
    else:
        year, month, day = (int(x) for x in str.split('-'))
        date = datetime.date(year, month, day)
        days.append(date.weekday())

def addDayColumn(inputFile, outputFile):
    # Read input file
    data = pd.read_csv(inputFile)

    # Get Date column
    Date = data['Date']

    # HACK: there is nan in November data, so replace with "-"
    Date.fillna('-', inplace=True)

    # Create a list of days converted from Date column
    days = []
    Date.apply(lambda str: convert(str, days))

    # Add a new days column to data
    data['Day'] = days
    print("Writing to file..")

    # Save the modified data
    data.to_csv(outputFile)

path = '/Users/sibela/Desktop/Project/data/'
inPrefix = 'Merged_'
outPrefix = 'Day_'
files = [
        'April_2016_Bike.csv',
         'August_2016_Bike.csv',
         'December_2016_Bike.csv',
         'February_2016_Bike.csv',
         'January_2016_Bike.csv',
         'July_2016_Bike.csv',
         'June_2016_Bike.csv',
         'March_2016_Bike.csv',
         'May_2016_Bike.csv',
          'November_2016_Bike.csv',
         'October_2016_Bike.csv',
         'September_2016_Bike.csv'
    ]




# for file in files:
#     print("Processing: ", file)
#     addDayColumn(path + inPrefix + file, path + outPrefix + file)