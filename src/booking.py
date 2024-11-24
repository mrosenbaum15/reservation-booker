import time
from utils.vars import *
from utils.resy_client import ResyClient
from datetime import datetime

def main():
    # dow = datetime.now().weekday()
    # if dow != 4 or dow != 6:
    #     print('rerturning')
    #     return

    resy = ResyClient()
    while 1:
        try:
            config_token = resy.get_openings()
        except Exception as e:
            print(e)
            print('Error getting reservations. Will try again in 1 second...')
            time.sleep(5)
            continue


        if config_token is None or len(config_token) == 0:
            print('No booking config token. Will try again in 1 second...')
            time.sleep(5)
            continue

        if len(config_token) > 0:
            print('Found a reservation for you!')
        else:
            print('Found 0 openings. Will try again in 1 second...')
            time.sleep(5)
            continue
        
        try:
            book_token = resy.get_reservation_details(config_token)
            resy.make_reservation(book_token)
        except Exception as e:
            print('Error making reservation. Will try again in 1 second...')
            print(e)
            return
            # continue

        break

if __name__ == '__main__':
    main()