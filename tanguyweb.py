import streamlit as st
import datetime
import requests
import pandas as pd
import numpy as np

st.title('TaxiFare Prediction 🚕😎💸')

st.header('What are the info of the ride you want to predict ?')


max_value = datetime.date(2020, 1, 1)
min_value = datetime.date(2009, 1, 1)

pickup_date = st.date_input("date of pickup",
                            value=datetime.date(2015, 1, 1),
                            max_value=max_value, min_value=min_value)
pickup_time = st.time_input("time of pickup",
                            value=datetime.time(12, 0),
                            step=60)

pickup_longitude = st.number_input(
    "pickup longitude", value=-73.950655, placeholder="Type a longitude...", format="%0.6f"
    )
pickup_latitude = st.number_input(
    "pickup latitude", value=40.783282, placeholder="Type a latitude...", format="%0.6f"
    )
dropoff_longitude = st.number_input(
    "dropoff longitude", value=-73.984365, placeholder="Type a longitude...", format="%0.6f"
    )
dropoff_latitude = st.number_input(
    "dropoff latitude", value=40.769802, placeholder="Type a latitude...", format="%0.6f"
    )
passenger_count = st.number_input(
    "Passenger count",
    value=1,
    placeholder="Type a number of passenger...",
    min_value=1, max_value=8,
    step=1,
    format="%d"
    )

if st.button("Predict fare"):
    try:

        pickup_datetime = datetime.datetime.combine(pickup_date, pickup_time)

        params = {
        'pickup_datetime':pickup_datetime,
        'pickup_longitude':pickup_longitude,
        'pickup_latitude':pickup_latitude,
        'dropoff_longitude':dropoff_longitude,
        'dropoff_latitude':dropoff_latitude,
        'passenger_count':passenger_count,
        }

        url = f'https://taxifare.lewagon.ai/predict'

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            fare = round(data["fare"], 2)

            st.success(f"This ride will probably cost **${fare}** 💰")

            df = pd.DataFrame(
                {
                    'lon':[pickup_longitude, dropoff_longitude],
                    'lat':[pickup_latitude, dropoff_latitude],
                    'color':["#008000", "#FF0000"]
                })

            st.title('See on the map :')

            st.markdown('-> pickup location in :green[green] :large_green_square:')
            st.markdown('-> dropoff location in :red[red] :large_red_square:')


            map = st.map(df, color="color", zoom=9)

        else:
            st.error(f"Error from API: {response.status_code}\n{response.text}")

    except Exception as e:
        st.error(f"Unexpected error: {e}")
