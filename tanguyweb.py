import streamlit as st
import datetime
import requests
import pandas as pd
import numpy as np

'''
# TaxiFareModel
'''


'''
## What are the info of the ride you want to predict ?
'''
max_value = datetime.date(2016, 1, 1)
min_value = datetime.date(2009, 1, 1)
pickup_date = st.date_input("date of pickup", value=None, max_value=max_value, min_value=min_value)
pickup_time = st.time_input("time of pickup", value=None, step=60)
pickup_longitude = st.number_input(
    "pickup longitude", value=None, placeholder="Type a longitude...", format="%0.6f"
    )
pickup_latitude = st.number_input(
    "pickup latitude", value=None, placeholder="Type a latitude...", format="%0.6f"
    )
dropoff_longitude = st.number_input(
    "dropoff longitude", value=None, placeholder="Type a longitude...", format="%0.6f"
    )
dropoff_latitude = st.number_input(
    "dropoff latitude", value=None, placeholder="Type a longitude...", format="%0.6f"
    )
passenger_count = st.number_input(
    "Passenger count",
    value=1,
    placeholder="Type a number of passenger...",
    min_value=1, max_value=8,
    step=1,
    format="%d"
    )


if pickup_date and pickup_time and passenger_count:

    pickup_datetime = datetime.datetime.combine(pickup_date, pickup_time)

    params = {
    'pickup_datetime':pickup_datetime,
    'pickup_longitude':pickup_longitude,
    'pickup_latitude':pickup_longitude,
    'dropoff_longitude':dropoff_longitude,
    'dropoff_latitude':dropoff_longitude,
    'passenger_count':passenger_count,
    }

if st.button("Predict fare"):

    url = f'https://taxifare.lewagon.ai/predict'

    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code == 200:

        st.write(f'Prediction of the taxifare is {np.round(data['fare'], 2)}$')

        df = pd.DataFrame(
            {
                'lon':[pickup_longitude, dropoff_longitude],
                'lat':[pickup_latitude, dropoff_latitude],
                'color':["#008000", "#FF0000"]
            })

        '''### See on the map :

        pickup location in green
        dropoff location in red
        '''

        map = st.map(df, color="color")
    else:
        st.error(f"Error from API: {response.status_code}\n{response.text}")

# color=("#008000", "#FF0000")
