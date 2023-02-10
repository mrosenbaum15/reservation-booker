import os

AUTH_TOKEN = os.getenv('AUTH_TOKEN')
API_KEY = os.getenv('API_KEY')
LONG = 0
LAT = 0
PARTY_SIZE = '2'
CITY = 'chi'
RESY_BASE_URL = 'https://api.resy.com'

RESTAURANT_ID = '' # enter the restaurant ID here
BOOKING_DATE = '' # enter the reservation date in yyyy-mm-dd format
BOOKING_TIME_RANGE_START = '' # enter the earliest time you'd accept for your reservaiton in yyyy-mm-dd hh:mm:ss format
BOOKING_TIME_RANGE_END =  '' # enter the latest time you'd accept for your reservaiton in yyyy-mm-dd hh:mm:ss format
BOOKING_TIME_PREFERRENCE = '' # enter the ideal time for your reservaiton in yyyy-mm-dd hh:mm:ss format
