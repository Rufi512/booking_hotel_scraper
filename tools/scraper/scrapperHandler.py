




import  argparse
import logging
import threading
import concurrent.futures

from queue import Queue
from typing import Dict, List, Tuple

try:
	from scraper import database
	from scraper import spyder 
except:
	import sys 
	print(sys.path)
	from tools.scraper import database
	from tools.scraper import spyder


from concurrent.futures import ThreadPoolExecutor


class BookingScrapperHandler:
	logging.basicConfig(
		level=logging.DEBUG,
		format='[%(levelname)s] (%(threadName)-10s) %(message)s'
	)


	def __init__(self,url:str):
		self.url = url 
		self.hotel:database.db_hotel = None
		self._rooms: spyder.ScraperRooms = None
		self.workers = 5


	def _thread_room_scraper(self,url:str, hotel_id:int, name:str, id:str) -> Dict:
		logging.debug("Init Scraping room")
		res = spyder.ScraperRooms(url,name,id)

		data = {
			"name" : res.name,
			"photos" : res.photos,
			"hotel_id" : hotel_id,
			"room_code" : id,
			"size" : res.size,
			"facilities" : res.facilities,
		}

		logging.debug("Ending Scraping room")
		return data





	def _scrapper_hotel(self) -> database.db_hotel:
		res  = spyder.ScraperHotel(self.url)
		if res.status_code != 200:
			raise f'Scraper no funcionando. {res.status_code}'


		#

		_hotel = database.session.query(database.db_hotel).filter_by(url_page=self.url)
		if _hotel.first():
			logging.info('UPDATE HOTEL INIT')
			_hotel.update({
				'name': res.name,
				'direction': res.direction,
				'photos':res.photos,
				'score' : res.score,
				'score_review' : res.score_review,
				"description": res.description,

			})


			"""

			query = database.db_hotel.update(database.db_hotel).where( database.db_hotel.url_page == self.url).values(
				name = res.name,
				direction = res.direction,
				photos = res.photos,
				score = res.score,
				score_review =res.score_review,
			)
			database.session.execute(query)
			"""    
			logging.info('UPDATE HOTEL END')


		else:
			logging.info('INIT CREATE HOTEL')
			query = database.db.insert(database.db_hotel).values(
				url_page = self.url,
				name = res.name,
				direction = res.direction,
				photos = res.photos,
				score = res.score,
				score_review =res.score_review,
				description=res.description,
			) 
			database.session.execute(query)
			logging.info('END CREATE HOTEL')



		database.session.commit()

		_hotel = database.session.query(database.db_hotel).filter_by(url_page=self.url).first()
		return (_hotel.id,res.rooms)


	def _room_save(self,url:str,hotel_id:int,response_rooms:List[Dict]) -> database.db_room:
		futures = []
		with ThreadPoolExecutor(max_workers=self.workers) as executor:
		
			for num in range(len(response_rooms)):
				room: Tuple[str,str] = response_rooms[num]
				url = f"{url}?#room_{room[1]}"
				futures.append(executor.submit(self._thread_room_scraper,url = url, hotel_id = hotel_id, name = room[0], id = room[1]))


			for future  in concurrent.futures.as_completed(futures):
				data = 	future.result()
				#comprobar de que la habitacion no exista
				code:str = data['room_code']
				_room = database.session.query(database.db_room).filter_by(room_code=code)

				if _room.first():
					logging.info("UPDATE ROOM INIT")
					_room.update({
						'name': data.get('name'),
						'facilities': data.get('facilities'),
						'photos':data.get('photos'),
						'size': data.get('size')
					})

					logging.info("UPDATE ROOM END")
				
				else:
					logging.info("CREATE ROOM INIT")
					query = database.db.insert(database.db_room).values(**data) 
					database.session.execute(query)
					logging.info("CREATE ROOM END")

		
		database.session.commit()


	def _model_to_dict(self,res_review,hotel_id) -> Dict:
		return {
			'score': res_review.score,
			'comments': res_review.comments,
			'categories':res_review.categories,
			'hotel_id': hotel_id,
		}



	def _review_save(self,url:str,hotel_id:int) -> database.db_review:
		url = f"{url}#tab-reviews"

		data = spyder.ReviewHotel(url)
		data = self._model_to_dict(data,hotel_id)
		message = data.pop('comments')

		#	_hotel =  database.session.query(database.db_hotel).filter_by(hotel_id=hotel_id).first()
		_review = database.session.query(database.db_review).filter_by(hotel_id = hotel_id)
		logging.info("INIT SAVE REVIEW HOTEL")



		if _review.first():
			logging.info("INIT UPDATE REVIEW HOTEL")
			_review.update(data)
			database.session.commit()
			logging.info("EMD UPDATE REVIEW HOTEL")
		else:
			query = database.db.insert(database.db_review).values(**data) 
			database.session.execute(query)
		
		_review = database.session.query(database.db_review).filter_by(hotel_id = hotel_id).first()


		logging.info("END SAVE REVIEW HOTEL")
		database.session.commit()
		self._comments_save(message,_review.id)



	def _comments_save(self,data:List[str],review_id):
		
		logging.info("INIT SAVE COMMENTS REVIEW HOTEL")
		_comments = database.session.query(database.db_commentary).filter_by(review_id=review_id).delete()

		for comment in data:
			comment['review_id'] = review_id
			logging.info("INIT CREATE COMMENTARY REVIEW HOTEL")

			logging.debug(comment)

			query = database.db.insert(database.db_commentary).values(**comment) 
			database.session.execute(query)
			

			logging.info("END CREATE COMMENTARY REVIEW HOTEL")
		

		_comments = database.session.query(database.db_commentary).filter_by(review_id = review_id)


		logging.info("END SAVE COMMENTS REVIEW HOTEL")
		database.session.commit()
