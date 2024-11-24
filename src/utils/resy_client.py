import json
import requests
from datetime import datetime, timedelta
from utils.vars import *

class ResyClient:
    common_headers = {
        "Authorization": 'ResyAPI api_key="' + API_KEY + '"',
        'content-type': "application/x-www-form-urlencoded; charset=utf-8",
        'origin': 'https://resy.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
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
            'lat': LAT,
            'long': LONG,
            'day': BOOKING_DATE,
            'location': CITY,
            'party_size': PARTY_SIZE,
            'venue_id': RESTAURANT_ID
        }
        
        url = RESY_BASE_URL + '/4/find'
        r = requests.get(url, params=params, headers=self.common_headers, timeout=1)
        print(r)
        data = json.loads(r.content)
        openings = data['results']['venues'][0]['slots']
        return self.find_booking_config_token(openings)

        
    def get_reservation_details(self, config_token):
        headers = self.common_headers
 
        params = {
            'day': BOOKING_DATE,
            'party_size': PARTY_SIZE,
            'config_id': config_token
        }
        
        r = requests.get(RESY_BASE_URL + '/3/details', params=params, headers=headers, timeout=5)
        print(r)
        data = json.loads(r.content)
        print(data)
        return data['book_token']['value']

    
    def make_reservation(self, book_token):
        headers = self.common_headers
        headers['accept'] = 'application/json'
        headers['x-resy-auth-token'] = AUTH_TOKEN
       
        # headers = {
        #     'Authorization': 'ResyAPI api_key="' + API_KEY + '"',
        #     'accept': 'application/json',
        #     'content-type': 'application/x-www-form-urlencoded',
        #     'X-Resy-Auth-Token': AUTH_TOKEN,
        #     'origin': 'https://widgets.resy.com/',
        #     'Cache-Control': 'no-cache'
        # }
        
        payment = f'{{"id":{PAYMENT_ID}}}'
        print(payment)
        newParams = {
                'book_token': book_token,
                'struct_payment_method': payment,
                'source_id': 'resy.com-venue-details'
            }
            
        r = requests.post(RESY_BASE_URL + '/3/book', data=newParams, headers=headers, timeout=10)
        print('Status of reservation request: ', r.content)
        if r.status_code != 201:
            print(r.status_code)
            raise Exception('Error making reservation. Trying again.')