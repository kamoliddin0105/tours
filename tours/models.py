from django.contrib.postgres.fields import ArrayField
from django.db import models

from accounts.models import User
from core.models import BaseModel
from currency.models import Currency


class Country(BaseModel):
    REGION_CHOICES = [
        ('EUROPE', 'Europe'),
        ('ASIA', 'Asia'),
        ('NORTH_AMERICA', 'North America'),
        ('SOUTH_AMERICA', 'South America'),
        ('AFRICA', 'Africa'),
    ]

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)  # Optional: ISO code like "TR", "EG"
    currency = models.ForeignKey(Currency, max_length=10, related_name='countries', on_delete=models.CASCADE)
    region = models.CharField(max_length=20, choices=REGION_CHOICES)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'countries'


class TourOperator(BaseModel):
    name = models.CharField(max_length=255)
    website = models.URLField(blank=True, null=True)
    contact_info = models.TextField(blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tour_operator'


class TourDestination(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1000, blank=True, null=True)
    departure_city = models.CharField(max_length=255, default='Tashkent')
    destination_country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='tours')
    operator = models.ForeignKey(TourOperator, on_delete=models.SET_NULL, null=True, blank=True)

    start_date = models.DateField()
    end_date = models.DateField()
    nights = models.PositiveIntegerField(default=7)

    price_adult = models.DecimalField(max_digits=10, decimal_places=2)
    price_child = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    hotel_star = models.PositiveSmallIntegerField(choices=[(i, f'{i} stars') for i in range(1, 6)])
    includes = ArrayField(models.CharField(max_length=255), blank=True, default=list)

    images = ArrayField(models.URLField(), blank=True, default=list)
    available_seats = models.PositiveIntegerField(default=0)

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
        db_table = 'tour_destination'


class PriceCalendar(models.Model):
    tour = models.ForeignKey(TourDestination, on_delete=models.CASCADE, related_name='price_calendar')
    date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.tour.name} - {self.date} - {self.price}"
