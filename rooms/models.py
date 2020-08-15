from datetime import datetime
from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField
from core import models as core_models
from users import models as user_models
from cal import Calendar

# import 순서: python package -> django -> third party apps -> custom apps


class AbstractItem(core_models.TimeStampedModel):
    """ Abstract Item """

    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class RoomType(AbstractItem):
    """ RoomType Model Definition"""

    class Meta:
        verbose_name = "Room Type"
        ordering = ["name"]  # 역순으로 하려면 -name으로 하면 된다.


class Amenity(AbstractItem):
    """ Amenity Model Definition"""

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):
    """ Facility Model Definition"""

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):
    """ HouseRule Model Definition"""

    class Meta:
        verbose_name = "House Rule"


class Room(core_models.TimeStampedModel):
    """ Room model definition """

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField()
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(
        user_models.User, related_name="rooms", on_delete=models.CASCADE
    )  # 모델과 모델을 연결 - many to one relationship
    # on_delete는 User를 삭제했을 때 어떤 식으로 동작하게 할지, CASCADE는 폭포수라는 의미로 USER를 삭제하면 USER와 연결되었던 ROOM도 같이 삭제되도록 한다.
    # related_name은 user가 room과의 관계를 찾을 때 room_set을 찾는 것이 아닌 rooms를 찾아도 되도록 이름을 짓는 것이다. 기본적으로 장고가 room_set을 만들어줌.
    # 즉, related name은 대상이 너를 찾는 방식이라는 사실
    room_type = models.ForeignKey(
        RoomType, related_name="rooms", on_delete=models.SET_NULL, null=True
    )
    # many to many relationship
    amenities = models.ManyToManyField(Amenity, related_name="rooms", blank=True)
    facilities = models.ManyToManyField(Facility, related_name="rooms", blank=True)
    house_rules = models.ManyToManyField(HouseRule, related_name="rooms", blank=True)

    def save(self, *args, **kwargs):
        self.city = str.capitalize(self.city)
        super().save(*args, **kwargs)  # Call the real save() method

    def __str__(self):
        return self.name

    def total_rating(self):
        result = 0
        all_reviews = self.reviews.all()
        if len(all_reviews) > 0:
            for review in all_reviews:
                result += review.rating_average()
            return round(result / len(all_reviews), 2)
        return 0

    def get_absolute_url(self):
        return reverse("rooms:detail", kwargs={"pk": self.pk})

    def first_photo(self):
        try:
            (photo,) = self.photos.all()[:1]
            return photo.file.url
        except ValueError:
            return None

    def get_next_four_photos(self):
        photos = self.photos.all()[1:5]
        return photos

    def get_calendars(self):
        year = datetime.today().year
        month = datetime.today().month
        this_month = Calendar(year, month)
        if month != 12:
            next_month = Calendar(year, month + 1)
        else:
            next_month = Calendar(year + 1, 1)
        return [this_month, next_month]


class Photo(core_models.TimeStampedModel):
    """ Photo Model Definition """

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="room_photos")
    room = models.ForeignKey(Room, related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption

