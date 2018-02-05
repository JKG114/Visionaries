import pandas as pd
import numpy as np
from heapq import nlargest
import datetime

# Calculates the delta as number of bikes incoming/outgoing at previous hour
# The higher the delta, the more bikes in the station
def setDelta(station_id, day, hour, data, delta):
    # Find tours coming to this station previous hour on the same day
    bool_starting = data['start station id'] == station_id
    bool_ending = data['end station id'] == station_id
    bool_day = data['Day'] == day
    incoming = data[bool_ending & bool_day]
    outgoing = data[bool_starting & bool_day]
    # assert(len(incoming) != 0)
    # assert(len(outgoing) != 0)

    # Find tours coming/leaving this station previous hour
    if(hour == 0):
        incoming = incoming[incoming['Time'] == 2300]
        outgoing = outgoing[outgoing['Time'] == 2300]
    else:
        hour -= 1;
        hour *= 100; # HACK, Times are 100 multiplied!!
        incoming = incoming[incoming['Time'] == hour]
        outgoing = outgoing[outgoing['Time'] == hour]

    # assert(len(incoming) != 0)
    # assert(len(outgoing) != 0)

    # Set the difference of coming/going
    delta.append(len(incoming) - len(outgoing))

# Given nhood id, day in [0..6] and hour in [0...23]
# Returns data frame including top k highest likely stations to find a bike.
# The higher the delta, the more higher the chance to find bike
# The headers of the data frame is "delta", "station id", "latitude", "longitude"
def getDelta(nhood, day, hour, k):

    data = pd.read_csv('data/March_2016.csv')
    stations = pd.read_csv('./stations.csv')

    # Stations in the given neighborhood
    # Mask keeps the original indices
    statsInNhood = stations[['station id', 'latitude', 'longitude']][stations['nhood id'] == nhood]
    # print(len(statsInNhood.unique()))
    # print(len(statsInNhood))

    # For every station, find coming/going delta
    delta = []
    statsInNhood.apply(lambda row: setDelta(row['station id'], day, hour, data, delta), axis=1)

    # # print(len(delta))
    statsDelta = pd.DataFrame({"station id": statsInNhood['station id'].tolist(),
                               "delta": delta,
                               "latitude": statsInNhood['latitude'].tolist(),
                               "longitude":statsInNhood['longitude'].tolist()})
    # print(statsDelta)

    # Return top-k highest delta (meaning more bikes)
    return statsDelta.nlargest(k, 'delta')
#
# best = getDelta(12, 1, 10, 123123)
# print(best)