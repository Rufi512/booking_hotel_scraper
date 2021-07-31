from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Hotel, Room, ReviewHotel, Commentary
from .serializers import RoomSerializer, HotelSerializer, ReviewSerializers, CommentSerializers


"""
import sys
sys.path.append('..')
from tools.scraper import scrapperHandler
"""
	
# Create your views here.
class RoomView(APIView):

	def get(self,request,hotel_id):
		_hotel = Hotel.objects.get(id=hotel_id)
		_room = Room.objects.filter(hotel=_hotel)

		response = RoomSerializer(instance=_room,many=True)
		return Response(response.data, status = status.HTTP_201_CREATED)



class ReviewView(APIView):
	def get(self,request,hotel_id):
		#_hotel = Hotel.objects.get(id=hotel_id)
		_review = ReviewHotel.objects.all().filter(hotel_id=hotel_id)

		response = ReviewSerializers(instance=_review,many=True)
		return Response(response.data, status = status.HTTP_201_CREATED)



class HotelView(APIView):
	def get(self,request):
		hotel_id = request.GET.get('hotel_id')
		if hotel_id: 
			_hotel = Hotel.objects.get(id=hotel_id)
		else:
			_hotel = Hotel.objects.all()

		response = HotelSerializer(instance=_hotel,many=True)
		return Response(response.data, status = status.HTTP_201_CREATED)
	


	def post(self, request):
		url = request.data['url']
		try:
			hotel = scrapperHandler.BookingScrapperHandler(url)
			hotel_id,response_rooms = hotel._scrapper_hotel()

			hotel._room_save(url=url, hotel_id=hotel_id, response_rooms=response_rooms)
			hotel._review_save(url=url,hotel_id=hotel_id)


			__hotel = Hotel.objects.get(url_page=url)
			response = HotelSerializer(instance=__hotel)

			return Response(response.data, status = status.HTTP_201_CREATED)


		except:
			return Response({"message":'model not created'})


class CommentView(APIView):

	def get(self, request, hotel_id):
		_review = ReviewHotel.objects.all().filter(hotel_id=hotel_id)
		_review_id = [ review.id for review in _review]
		
		_comments = Commentary.objects.all().filter(review_id__in=_review_id)
		response = CommentSerializers(instance=_comments,many=True)
		return Response(response.data)