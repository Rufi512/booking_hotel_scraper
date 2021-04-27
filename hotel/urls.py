from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import HotelView, RoomView

app_name = "hotel"

urlpatterns = [
    path('hotel', HotelView.as_view()),
    path('hotel/<int:hotel_id>/rooms', RoomView.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
