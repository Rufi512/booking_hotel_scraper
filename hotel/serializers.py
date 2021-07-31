
from rest_framework import serializers
from .models import Hotel, Room, ReviewHotel, Commentary


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'



class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = ReviewHotel
        fields = '__all__'


class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Commentary
        fields = '__all__'


class HotelSerializer(serializers.ModelSerializer):
    room = serializers.StringRelatedField(many=True)
    review = serializers.StringRelatedField()
    #room = RoomSerializer(many=True)

    class Meta:
        model = Hotel
        fields = '__all__'
