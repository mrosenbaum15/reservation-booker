import time
from utils.vars import *
from utils.resy_client import ResyClient

def main():

    resy = ResyClient()

    while 1:
        try:
            config_token = resy.get_openings()
        except Exception as e:
            print('Error getting reservations. Will try again in 10 seconds...')
            time.sleep(10)
            continue

        if len(config_token) > 0:
            print('Found a reservation for you!')
        else:
            print('Found 0 openings. Will try again in 10 seconds...')
            time.sleep(10)
            continue
        
        try:
            book_token = resy.get_reservation_details(config_token)
            resy.make_reservation(book_token)
        except Exception as e:
            print('Error making reservation. Will try again in 10 seconds...')
            time.sleep(10)
            continue

        break

if __name__ == '__main__':
    main()