from django.db import models

from accounts.models import User


class TourDestination(models.Model):
    REGION_CHOICES = [
        ('Europe', 'Europe'),
        ('Asia', 'Asia'),
        ('North America', 'North America'),
        ('South America', 'South America'),
    ]

    DURATION_CHOICES = [
        ('7_days', '7_days'),
        ('14_days', '14_days'),
        ('1_month', '1_month'),
    ]

    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, choices=REGION_CHOICES, default='Europe')
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    duration = models.CharField(max_length=20, choices=DURATION_CHOICES, default='14 days')
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tours'


class UserTour(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey(TourDestination, on_delete=models.CASCADE)
    has_attended = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.tour.name}"

    class Meta:
        db_table = 'user_tours'
