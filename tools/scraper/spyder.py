
from bs4 import BeautifulSoup 
from typing import Dict,List
from dotenv import load_dotenv


import json
import requests
import shutil
import re
import os
import logging



Response = requests.models.Response


class ScraperHandler:


	logging.basicConfig(
		level=logging.DEBUG,
	)


	def __init__(self,url:str,proxy:bool=False):
		self._url:str = url 
		self.headers:Dict[str]= {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
			}
		self.status_code:int = 0

		self.html:str = BeautifulSoup(self.get_page(proxy),'html5lib')

	def get_page(self,proxy = False) -> str:
		res:Response = self._proxy() if proxy else requests.get(self._url)
		self.status_code = res.status_code

		message:Dict[str,str] = {}

		if res.status_code == 200:
			return res.text
		elif res.status_code == 302:
			#Cabecera antigua puede redirigirte.
			return {'message': 'ruta movido, probablemente la cabecera no este funcionando', 'status': res.status_code}
		elif res.status_code:
			return {'message': 'ruta no encontrada', 'status':res.status_code}

	def _proxy(self) -> Response:
		script:str = """splash:go(args.url) return splash:html() """
		payload:str = json.dumps({'url': self._url, 'wait': 30}) 
		#res:Response =  requests.get('http://localhost:8050/render.html', params= payload)
		
		splash_url = os.getenv('SPLASH_URL_DOCKER')
		#splash_url = 'http://localhost:8050'

		return requests.post(f'{splash_url}/run', json={
			'lua_source': script,
			'url': self._url,
			'timeout':90
		},stream=True)


class ReviewHotel(ScraperHandler):
	def __init__(self, url:str,proxy:bool = True):
		super().__init__(url,proxy)
		self._score = ""
		self._categories:List[Dict] = []
		self._comments:List[Dict] = []


	@property
	def score(self):
		logging.info('init score scrapper ')
		
		query = "review-score-badge" 
		try:
			self._score = self.html.select(f'span[class={query}]')[0].text
			logging.debug(self._score)
		except:
			self._score = '0'

		logging.info('end score scrapper ')
		return self._score


	@property
	def categories(self):
		query_title = 'span[class="c-score-bar__title"]'
		query_score = 'span[class="c-score-bar__score"]'
		query_categories = 'div[class="c-score-bar"]'

		logging.info('INIT CATEGORIES SCRAPPER ')
		
		_categories = []
		
		#logging.debug(html_categories)

		html_categories = self.html.select(query_categories)
		for category in html_categories:
			try:
				name = category.select(query_title)[0].text
			except:
				name = ''
			try:
				score = category.select(query_score)[0].text
			except:
				score = '0.0'


			_categories.append([name,score])

		logging.info('END CATEGORIES SCRAPPER ')
		return _categories
	
	
	@property
	def comments(self):
		query = 'div[class="bui-grid"]'
		html_section_comments = self.html.select(query)
		
		self._comments = []

		logging.info("INIT COMMENTS SCRAPPER")
		for comment in html_section_comments:
			try:
				name_user = comment.select('span[class="bui-avatar-block__title"]')[0].text
			except:
				name_user = 'Anonymus'



			try:
				country_img = comment.select('span[class="bui-flag bui-avatar-block__flag"]	 > span >img')[0]['src']
				logging.debug(country_img)
			except:
				country_img = ''

			try:
				country = comment.select('span[class="bui-avatar-block__subtitle"]>span')[0].text
			except:
				country = ''


			try:
				positive_message = comment.select('div[class="c-review__row"] > p > span[class="c-review__body"]')[0].text
			except:
				positive_message = ''
			try:
				negative_message = comment.select('div[class="c-review__row lalala"] > p > span[class="c-review__body"]')[0].text
			except:
				negative_message = ''

			self._comments.append({
				'name_user':name_user,
				'country': country,
				'country_img':country_img,

				'positive_message':positive_message,
				'negative_message': negative_message,
				})


		logging.info("END COMMENTS SCRAPPER")
		return self._comments

			
	def __dict__(self):
		return {
			'score': self.score,
			'comments': self.comments,
			'categories':self.categories,
		}

class ScraperHotel(ScraperHandler):
	def __init__(self, url:str,proxy:bool = True):
		super().__init__(url,proxy)

		self._name:str = ""
		self._direction:str = ""
		self._photos:List =[]
		self._rooms:List = []
		self._score:str = ""
		self._score_review:str = ""
		self._comments:List[ReviewHotel] = []

		self._description:str = [] 


	@property
	def description(self):
		try:
			#query = "div[]"
			#self._description = self.html.select(query)
			return 'NOT IMPLEMENT YET'
		except:
			return ""

	@property
	def score_review(self) -> str:
		try:
			_score_review = self.html.select('div[class="hp-review-score-cta-container-remote"] > div > div > div > div > div')
			return _score_review[1].text
		except IndexError:
			return '0'

	@property
	def score(self) -> str:
		try:
			score = self.html.select('div[class="hp-review-score-cta-container-remote"] > div > div > div > div')
			logging.debug(score[0].text)
			return score[0].text
		except IndexError as es:
			return '0'

	@property
	def name(self) -> str:
		try:
			_name:str = self.html.select('h2[id="hp_hotel_name"]')[0].text.strip()
			return _name
		except:
			return 'N/A'

	@property
	def direction(self) -> str:
		try:
			return self.html.select('p[class="address address_clean"] > span')[0].text
		except:
			return 'N/A'


	@property
	def photos(self) -> List:
		_photos:List = self.html.select('div[class="bh-photo-grid-thumbs bh-photo-grid-thumbs-s-full"] > div > a')
		return [photo["href"] for photo in _photos]
			
	@property
	def rooms(self) -> List:
		css_name:str = 'data-room-name-en'
		try:
			html_rooms:List = self.html.select('div[class="room-info"] > a')
			return [(room[css_name], room['href'][3:]) for room in html_rooms]
		except:
			return []


class ScraperRooms(ScraperHandler):
	def __init__(self, url:str,name:str, id:str, proxy:bool= True):

		super().__init__(url,proxy)

		self.id = id
		self.name = name
		self._size:str = ""
		self._photos:List=[]
		self._equipments:List = []
		self._facilities = []

	@property
	def photos(self) -> List:
		_html_photos:List = self.html.select('div[class="slick-list draggable"] > div[class="slick-track"] > div[class="slick-slide"] > img')
		photos:List = []
		for photo in _html_photos:
			try:
				photos.append(photo['src'])
			except:
				photos.append(photo['data-lazy'])

		#photo['src'] if photo['src'] else photo['data-lazy']
		#return [ photo['src']  for photo in _photos]
		return photos

	@property
	def size(self) -> str:
		try:
			_size = self.html.select('div[class="hprt-lightbox-right-container"]')[0].text
			pattern = r"Room size\n.+\n.+\n\n.+\n\s+([0-9]+\s.+)"
			return re.search(pattern,_size).group(1)
		except:
			return '0'

	@property
	def facilities(self) -> List:
		__facilities = self.html.select('ul[class="hprt-lightbox-list js-lightbox-facilities"] > li > span')
		return [ items.text for items in __facilities]

	def write_html(self):
		result = self.get_page(proxy=True)
		with open(f"room_{self.id}.html","w") as f:
			f.write(result)


def test():
	url = 'https://www.booking.com/hotel/cl/ibis-budget-providencia.html'
	print('rute CSM')
	logging.debug("prueba")

	r = ScraperHotel(url=url)

	id = r.rooms[3][1]
	name = r.rooms[0][0]
	
	url = f"{url}?#room_{id}"
	result = ScraperRooms(url,name,id).facilities
	print(result)

	#r.write_html()

if __name__ == '__main__':
	test()