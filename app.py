import streamlit as st
import pandas as pd
import numpy as np

import datetime
import requests



'''
# TaxiFareModel front
'''

# st.markdown('''
# Remember that there are several ways to output content into your web page...

# Either as with the title by just creating a string (or an f-string). Or as with this paragraph using the `st.` functions
# ''')

# '''
# ## Here we would like to add some controllers in order to ask the user to select the parameters of the ride

# 1. Let's ask for:
# - date and time
# - pickup longitude
# - pickup latitude
# - dropoff longitude
# - dropoff latitude
# - passenger count
# '''
'''
### Please input the parameters for your ride:
'''
d = st.date_input(
    "Which day do you need the pick-up?",
    datetime.date(2019, 7, 6))
t = st.time_input('What time?', datetime.time(8, 45))

# people  = st.number_input('How many passengers?', 1, step=1)
people = st.slider('How many passengers?', 1, 8, 1)


direction = st.radio('What inputs do you have?', ('addres', 'coordinates'))

st.write(direction)
if direction == 'addres':
    p_address = st.text_input('Pick-up address', 'Trump Tower')
    d_address = st.text_input('Drop-off address', 'Empire State Building')

    url_address = 'https://nominatim.openstreetmap.org/search'

    p_response = requests.get(url_address, params={'q': p_address, 'format': 'json'}).json()
    p_lat = float(p_response[0]['lat'])
    p_lon = float(p_response[0]['lon'])

    d_response = requests.get(url_address, params={'q': d_address, 'format': 'json'}).json()
    d_lat = float(d_response[0]['lat'])
    d_lon = float(d_response[0]['lon'])

elif direction == 'coordinates':
    p_lat = st.number_input('Pick-up latitude', value=40.762428, min_value = 40.5, max_value = 40.9)
    p_lon = st.number_input('Pick-up longitude', value=-73.973793, min_value = -74.3, max_value = -73.7)
    d_lat = st.number_input('Drop-off latitude', value=40.748817, min_value = 40.5, max_value = 40.9)
    d_lon  = st.number_input('Drop-off longitude', value=-73.985428, min_value = -74.3, max_value = -73.7)

else:
    st.write('You need to pick an input!')


@st.cache
def get_map_data():
    return pd.DataFrame(
            np.array([[p_lat, p_lon], [d_lat, d_lon]]),
            columns=['lat', 'lon']
        )
df = get_map_data()

if st.checkbox('Click here to see a map!'):
    '''
    Check this map out!
    '''
    st.map(df)


# '''
# ## Once we have these, let's call our API in order to retrieve a prediction

# See ? No need to load a `model.joblib` file in this app, we do not even need to know anything about Data Science in order to retrieve a prediction...

# 🤔 How could we call our API ? Off course... The `requests` package 💡
# '''

url = 'https://taxifare.lewagon.ai/predict'

# if url == 'https://taxifare.lewagon.ai/predict':
#     st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')


# '''
# 2. Let's build a dictionary containing the parameters for our API...

# 3. Let's call our API using the `requests` package...

# 4. Let's retrieve the prediction from the **JSON** returned by the API...

# ## Finally, we can display the prediction to the user
# '''
paramsss = {
    'pickup_datetime': f"{d} {t}",
    'pickup_longitude': p_lon,
    'pickup_latitude': p_lat,
    'dropoff_longitude': d_lon,
    'dropoff_latitude': d_lat,
    'passenger_count': people
}

response = requests.get(url, params=paramsss).json()

'''
### Predicted fare price
'''
col1, col2, col3 = st.columns(3)
col1.metric("","")
col2.metric("",f"${response['fare']}")
col3.metric("","")
# st.write('Here is the predicted fare price:', response['fare'])
