import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models

from accounts.models import User
from core.models import BaseModel
from currency.models import Currency


class TourDestination(BaseModel):
    REGION_CHOICES = [
        ('EUROPE', 'Europe'),
        ('ASIA', 'Asia'),
        ('NORTH_AMERICA', 'North America'),
        ('SOUTH_AMERICA', 'South America'),
    ]

    DURATION_CHOICES = [
        ('7_DAYS', '7_days'),
        ('14_DAYS', '14_days'),
        ('1_MONTH', '1_month'),
    ]

    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, choices=REGION_CHOICES, default='Europe')
    description = models.TextField()
    start_point = models.CharField(max_length=255, default='Tashkent')
    start_date = models.DateField()
    end_date = models.DateField()
    duration = models.CharField(max_length=20, choices=DURATION_CHOICES, default='14_DAYS')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_children = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    available_seats = models.DecimalField(max_digits=10, decimal_places=2)
    is_featured = models.BooleanField(default=False)
    departure_dates = ArrayField(models.DateField(), blank=True, default=list)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, blank=True)
    includes = ArrayField(models.CharField(max_length=255), blank=True, default=list)
    images = ArrayField(models.URLField(max_length=500), blank=True, default=list)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tours'


class UserTour(BaseModel):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('PAYME', 'Payme'),
        ('CLICK', 'Click'),
        ('CASH', 'Cash')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey(TourDestination, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    has_attended = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='CASH')
    booking_code = models.CharField(max_length=12, unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.tour.name}"

    def save(self, *args, **kwargs):
        if not self.booking_code:
            self.booking_code = str(uuid.uuid4()).replace('-', '')[:12]
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'user_tours'
        unique_together = ('user', 'tour')

class TourPriceWatch(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey(TourDestination, on_delete=models.CASCADE)
    target_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_notified = models.BooleanField(default=False)

