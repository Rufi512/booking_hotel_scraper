from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Hotel, Room
from .serializers import RoomSerializer, HotelSerializer

import sys
sys.path.append('..')
from tools.scraper import ScraperHotel,ScraperRooms

# Create your views here.
class RoomView(APIView):

	def get(self,request,hotel_id):
		_hotel = Hotel.objects.get(id=hotel_id)
		_room = Room.objects.filter(hotel=_hotel)

		response = RoomSerializer(instance=_room,many=True)
		return Response(response.data, status = status.HTTP_201_CREATED)

class HotelView(APIView):

	def get(self,request):
		_hotel = Hotel.objects.all()
		response = HotelSerializer(instance=_hotel,many=True)
		return Response(response.data, status = status.HTTP_201_CREATED)
	
	def post(self, request):
		url = request.data['url']
		_hotel = Hotel.objects.get(url_page=url)

		response = HotelSerializer(instance=_hotel)
		return Response(response.data, status = status.HTTP_201_CREATED)
	