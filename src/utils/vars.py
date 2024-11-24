import os
from datetime import datetime, timedelta

AUTH_TOKEN = os.getenv('AUTH_TOKEN')
API_KEY = os.getenv('API_KEY')
PAYMENT_ID = os.getenv('PAYMENT_ID')
LONG = 0
LAT = 0
RESY_BASE_URL = 'https://api.resy.com'

current_time = datetime.now() + timedelta(days=42) # change to however many days in advance needed
BOOKING_DATE = current_time.strftime('%Y-%m-%d')
# BOOKING_DATE = '2025-01-05' # manually set date instead and comment out the two lines above

# Kasama 

PARTY_SIZE = '2'
CITY = 'chi'
RESTAURANT_ID = '53324' # enter the restaurant ID here
BOOKING_TIME_RANGE_START = BOOKING_DATE + ' 16:00:00' # enter the earliest time you'd accept for your reservaiton in yyyy-mm-dd hh:mm:ss format
BOOKING_TIME_RANGE_END = BOOKING_DATE + ' 23:30:00' # enter the latest time you'd accept for your reservaiton in yyyy-mm-dd hh:mm:ss format
BOOKING_TIME_PREFERRENCE = BOOKING_DATE + ' 19:30:00' # enter the ideal time for your reservaiton in yyyy-mm-dd hh:mm:ss format