from django.db import models

from accounts.models import User
from core.models import BaseModel, Infrastructure, ChildFacility
from currency.models import Currency


class Region(BaseModel):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'regions'

    def __str__(self):
        return self.name


class Country(BaseModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="countries")
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="countries")

    class Meta:
        db_table = 'countries'

    def __str__(self):
        return self.name


class TourOperator(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="operator")
    company_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    telegram_username = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.company_name


class TourDestination(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1000, blank=True, null=True)
    departure_city = models.CharField(max_length=255, default="Tashkent")
    destination_country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="tours")
    operator = models.ForeignKey(TourOperator, on_delete=models.SET_NULL, null=True, blank=True)

    start_date = models.DateField()
    end_date = models.DateField()
    nights = models.PositiveIntegerField(default=7)

    price_adult = models.DecimalField(max_digits=10, decimal_places=2)
    price_child = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    hotel_star = models.PositiveSmallIntegerField(choices=[(i, f"{i} stars") for i in range(1, 6)])
    hotel_rating = models.FloatField(null=True, blank=True)

    meal_type = models.CharField(
        max_length=10,
        choices=[
            ("BB", "Bed & Breakfast"),
            ("HB", "Half Board"),
            ("FB", "Full Board"),
            ("AI", "All Inclusive"),
        ],
        null=True,
        blank=True,
    )

    distance_to_sea = models.PositiveIntegerField(null=True, blank=True, help_text="meters")
    beach_type = models.CharField(
        max_length=20,
        choices=[("sand", "Qum"), ("pebble", "Tosh"), ("private", "Xususiy")],
        null=True,
        blank=True,
    )

    infrastructures = models.ManyToManyField(Infrastructure, blank=True)
    child_facilities = models.ManyToManyField(ChildFacility, blank=True)

    is_featured = models.BooleanField(default=False)
    is_hot = models.BooleanField(default=False)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.start_date and self.end_date:
            self.nights = (self.end_date - self.start_date).days
        super().save(*args, **kwargs)

    class Meta:
        db_table = "tour_destination"

class UserTour(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    tour = models.ForeignKey(TourDestination, on_delete=models.CASCADE, related_name="bookings")
    has_attended = models.BooleanField(default=False)
    status = models.CharField(max_length=10,
                              choices=[
                                  ("pending", "Pending"),
                                  ("confirmed", "Confirmed"),
                                  ("canceled", "Canceled")])

    def __str__(self):
        return f"{self.user} → {self.tour}"

class TourImage(models.Model):
    tour = models.ForeignKey(TourDestination, on_delete=models.CASCADE, related_name="images")
    url = models.URLField()


class TourInclude(models.Model):
    tour = models.ForeignKey(TourDestination, on_delete=models.CASCADE, related_name="includes")
    name = models.CharField(max_length=255)


class PriceCalendar(models.Model):
    tour = models.ForeignKey(TourDestination, on_delete=models.CASCADE, related_name='price_calendar')
    date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.tour.name} - {self.date} - {self.price}"
