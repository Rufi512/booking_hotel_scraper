

from database import *
from database import db_hotel, db_room
from scraper import ScraperHotel,ScraperRooms
from queue import Queue

import  argparse
import logging
import threading

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] (%(threadName)-10s) %(message)s'
)

def thread_room_scraper(url:str, hotel_id:int, name:str, id:str,queue:Queue) ->ScraperRooms:
    logging.debug("Init Scraping room")
    
    res = ScraperRooms(url,name,id)

    result = {
		"name" : res.name,
		"photos" : res.photos,
        "hotel_id" : hotel_id,
        "room_code" : id,
        "size" : res.size,
        "facilities" : res.facilities
    }

    queue.put(result)
    #session.execute(query)

    logging.debug("Ending Scraping room")
    return 0

def main(url:str):
    res = ScraperHotel(url)

    if res.status_code != 200:
        return f'Scraper no funcionando. {res.status_code}'

    _hotel = session.query(db_hotel).filter_by(url_page=url)

    if _hotel == []:

        query = db.insert(db_hotel).values(
            url_page = url,
            name = res.name,
            direction = res.direction,
            photos = res.photos,
            score = res.score,
            score_review =res.score_review,
        ) 
        
        #connection.execute(query)
        session.execute(query)
        session.commit()

    _hotel = _hotel[0]
    threads:List = [] 
    que = Queue()

    for num in range(len(res.rooms)):
        room = res.rooms[num]

        
        _thread = threading.Thread(name='thread%s' %num, 
                                target=thread_room_scraper,
                                args=(  url,
                                        _hotel.id,
                                        room[0],
                                        room[1],
                                        que
                                )
                            )
        _thread.start()
        threads.append(_thread)

    for i in threads:
        i.join()
        data = que.get()
            
        #comprobar de que la habitacion no exista
        _room = session.query(db_room).filter_by(room_code=room[1]).first()

        if _room is not True :
            query = db.insert(db_room).values(**data) 
            session.execute(query)
        else:
            _room.update(**data)
            logging.info("ya existe la habitacion")
    
    session.commit()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description ='enter a URL to run the scraping. example: python scraper.py https://www.booking.com/hotel/cl/ibis-budget-providencia.en-gb.html?',
        usage='%(prog)s [options] URL',
        epilog='Enjoy the program! :)'
    )

    # Add the arguments
    parser.add_argument('URL',
                       metavar='URL',
                       type=str,
                       help='the url to list')

    args = parser.parse_args()

    input_path:str = args.URL

    main(input_path)