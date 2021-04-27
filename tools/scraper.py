
from bs4 import BeautifulSoup 
from typing import Dict,List
from dotenv import load_dotenv


import json
import requests
import shutil
import re
import os
import logging


logging.basicConfig(
    level=logging.DEBUG,
)
Response = requests.models.Response


class ScraperHandler:
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


class ScraperHotel(ScraperHandler):
    def __init__(self, url:str,proxy:bool = True):
        super().__init__(url,proxy)

        self._name:str = ""
        self._direction:str = ""
        self._photos:List =[]
        self._rooms:List = []
        self._score:str = ""
        self._score_review:str = ""

    @property
    def score_review(self) -> str:
        return self.html.find_all('div',{'class':'bui-review-score__text'})[0].text

    @property
    def score(self) -> str:
        return self.html.find_all('div',{'class':'bui-review-score__badge'})[0].text

    @property
    def name(self) -> str:
        _name:str = self.html.select('h2[id="hp_hotel_name"]')[0].text.strip()
        return _name

    @property
    def direction(self) -> str:
        return self.html.select('p[class="address address_clean"] > span')[0].text

    @property
    def photos(self) -> List:
        _photos:List = self.html.select('div[class="bh-photo-grid-thumbs bh-photo-grid-thumbs-s-full"] > div > a')
        return [photo["href"] for photo in _photos]
            
    @property
    def rooms(self) -> List:
        html_rooms:List = self.html.select('div[class="room-info"] > a')
        css_name:str = 'data-room-name-en'
        return [(room[css_name], room['href'][3:]) for room in html_rooms]


class ScraperRooms(ScraperHandler):
    def __init__(self, url:str,name:str, id:str, proxy:bool= True):

        url = f"{url}?#room_{id}"
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
    r = ScraperHotel(url=url)

    id = r.rooms[3][1]
    name = r.rooms[0][0]
    result = ScraperRooms(url,name,id).facilities
    print(result)

    #r.write_html()

if __name__ == '__main__':
    test()