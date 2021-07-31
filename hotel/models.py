from django.db import models

try:
    from django.db.models import  JSONField, ArrayField
except:
    from django.contrib.postgres.fields import JSONField,ArrayField





class Hotel(models.Model):
    url_page = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    direction = models.CharField(max_length=255)
    score_review = models.CharField(max_length=255)
    score = models.CharField(max_length=255)

    description = models.CharField(max_length=10000)

    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)


    photos = ArrayField(
        models.CharField(max_length=255),
        size=5
    )

    class Meta:
        db_table = 'scraper_hotel'

    def __str__(self):
        return f'{self.name} {self.score}'



class Room(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    
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



class ReviewHotel(models.Model):
    score = models.CharField(max_length=100)
    categories = ArrayField(
        ArrayField(
            models.CharField(max_length=100, blank=True),
            size=2,
        ),
        size=100,
    )

    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name='review',
    )


    class Meta:
        db_table = 'scraper_review'

    def __str__(self):
        return self.score

# Create your models here.
class Commentary(models.Model):
    name_user = models.CharField(max_length=100)
    country = models.CharField(max_length=255)
    country_img = models.CharField(max_length=255)

    
    positive_message = models.CharField(max_length=1000)
    negative_message = models.CharField(max_length=1000)

    
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)


    review = models.ForeignKey(ReviewHotel, related_name='commentary', on_delete=models.CASCADE)


    class Meta:
        db_table = 'scraper_commentary'

    def __str__(self):
        return f'{self.name_user} {self.country}'



