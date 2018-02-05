import pandas as pd
import numpy as np
from numpy import linalg

def find_nhood(row, nhoods, neighbourhoods):
    station = np.array([row['latitude'], row['longitude']])
    distances = np.array([  linalg.norm(station -
                               np.array([neighbourhoods.iloc[i]['latitude'], neighbourhoods.iloc[i]['longitude']]))
                            for i in range(len(neighbourhoods))
                        ])
    nhoods.append(distances.argmin()+1)

def getStations(file, nHoodFile):
    df = pd.read_csv(file)
    neighbourhoods = pd.read_csv(nHoodFile)

    df = df.drop_duplicates('start station id')
    uniq_stations1 = df[['start station id','start station name', 'start station latitude', 'start station longitude']]
    # print(uniq_stations1)

    df = df.drop_duplicates('end station id')
    uniq_stations2 = df[['end station id','end station name', 'end station latitude', 'end station longitude']]
    # print(uniq_stations2)

    all = {"station id":list(uniq_stations1['start station id']) + list(uniq_stations2['end station id']),
           "station name": list(uniq_stations1['start station name']) + list(uniq_stations2['end station name']),
           "latitude":list(uniq_stations1['start station latitude']) + list(uniq_stations2['end station latitude']),
           "longitude": list(uniq_stations1['start station longitude']) + list(uniq_stations2['end station longitude'])
           }

    stations = pd.DataFrame(all)
    # print(len(new))

    # Clear duplicates coming from uniq_start and uniq_end
    stations = stations.drop_duplicates('station id')

    # For each station, find the closest neighboorhood
    nhoods = []
    stations.apply(lambda row: find_nhood(row, nhoods, neighbourhoods), axis = 1)
    stations['nhood id'] = nhoods
    # print(stations)

    for i in range(1,len(neighbourhoods)+1):
        print('Nhood: ', i, " ",  len(stations['nhood id'][stations['nhood id'] == i]))
        # assert len(stations['nhood id'][stations['nhood id'] == i]) != 0

    stations.to_csv('stations.csv')

# Given raw data and neighborhods
# Finds nhoods for stations seen in that data
# Saves it in stations.csv
getStations('data/July_2016.csv', './neighbourhoods.csv')