from django.db import models

from tours.models import TourDestination


class TourSchedule(models.Model):
    tour = models.ForeignKey(TourDestination, on_delete=models.CASCADE, related_name='tour_schedules')
    start_date = models.DateField()
    end_date = models.DateField()
    is_full = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seats = models.IntegerField(default=0)

    class Meta:
        db_table = 'tour_schedules'
        ordering = ['start_date']

    def __str__(self):
        return f"{self.tour.name} | {self.start_date} - {self.end_date}"
