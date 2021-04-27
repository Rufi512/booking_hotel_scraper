from django.db import models

try:
    from django.db.models import  JSONField, ArrayField
except:
    from django.contrib.postgres.fields import JSONField,ArrayField

# Create your models here.
class Hotel(models.Model):
    url_page = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    direction = models.CharField(max_length=255)
    score_review = models.CharField(max_length=255)
    score = models.CharField(max_length=255)

    photos = ArrayField(
        models.CharField(max_length=255),
        size=5
    )

    class Meta:
        db_table = 'scraper_hotel'

    def __str__(self):
        return f'{self.name} {self.score}'

class Room(models.Model):
    name = models.CharField(max_length=255)
    room_code = models.CharField(max_length=15, unique=True)
    size = models.CharField(max_length=15,null=True,blank=True)
    hotel = models.ForeignKey(Hotel, related_name='room', on_delete=models.CASCADE)
    
    photos = ArrayField(
        models.CharField(max_length=255),
        size=5
    )

    facilities = ArrayField(
        models.CharField(max_length=255)
    )

    class Meta:
        db_table = 'scraper_room'

    def __str__(self):
        return self.name
