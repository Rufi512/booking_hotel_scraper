
from rest_framework import serializers
from .models import Hotel,Room


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class HotelSerializer(serializers.ModelSerializer):
    room = serializers.StringRelatedField(many=True)
    #room = RoomSerializer(many=True)

    class Meta:
        model = Hotel
        fields = '__all__'
