import json
import requests
from datetime import datetime, timedelta
from utils.vars import *

class ResyClient:
    def timeInRange(self, start):
        start_in_range = start >= datetime.strptime(BOOKING_TIME_RANGE_START, '%Y-%m-%d %H:%M:%S')
        end_in_range = start <= datetime.strptime(BOOKING_TIME_RANGE_END, '%Y-%m-%d %H:%M:%S')
        return start_in_range and end_in_range
    
    def find_booking_config_token(self, openings):
        if len(openings) < 1:
            return ''
        ideal_time = datetime.strptime(BOOKING_TIME_PREFERRENCE, '%Y-%m-%d %H:%M:%S')
        best_time_difference = timedelta(hours=24) # a really large time delta so that first time found is set as best time difference between found times and preferred time
        config_token = ''
        for table in openings:
            start_time = datetime.strptime(table['date']['start'], '%Y-%m-%d %H:%M:%S')
            print('\nFound time: ', table['date']['start'], '\n')
            if self.timeInRange(start_time) and abs(start_time - ideal_time) < best_time_difference:
                best_time_difference = abs(start_time - ideal_time)
                config_token = table['config']['token']
        
        return config_token    

    def get_openings(self):
        params = {
            'day': BOOKING_DATE,
            'lat': LAT,
            'location': CITY,
            'long': LONG,
            'party_size': PARTY_SIZE,
            'venue_id': RESTAURANT_ID,
            'sort_by': 'available'
        }

        headers = {
            'Authorization': 'ResyAPI api_key="' + API_KEY + '"',
        }
        
        url = RESY_BASE_URL + '/4/find'
        r = requests.get(url, params=params, headers=headers)
        data = json.loads(r.content)
        print('\nAvailability results: ', data, '\n')
        openings = data['results']['venues'][0]['slots']
        return self.find_booking_config_token(openings)

        
    def get_reservation_details(self, config_token):
        headers = {
            'Authorization': 'ResyAPI api_key="' + API_KEY + '"',
            'accept': 'application/json',
            'content-type': 'application/x-www-form-urlencoded'
        }

        params = {
            'day': '2023-03-22',
            'party_size': 2,
            'config_id': config_token
        }
        
        r = requests.get(RESY_BASE_URL + '/3/details', params=params, headers=headers)
        data = json.loads(r.content)
        return data['book_token']['value']

    
    def make_reservation(self, book_token):
        headers = {
            'Authorization': 'ResyAPI api_key="' + API_KEY + '"',
            'accept': 'application/json',
            'content-type': 'application/x-www-form-urlencoded',
            'x-resy-auth-token': AUTH_TOKEN
        }

        newParams = {
                'book_token': book_token,
                'struct_payment_method': '{"id":13620270}',
                'source_id': 'resy.com-venue-details'
            }
        r = requests.post(RESY_BASE_URL + '/3/book', data=newParams, headers=headers)
        print('Status of reservation request: ', r.content)