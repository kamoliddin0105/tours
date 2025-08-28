from django.db import models

from accounts.models import User
from core.models import BaseModel
from tours.models import TourDestination


class Review(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    tour = models.ForeignKey(TourDestination, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    text = models.TextField()

    class Meta:
        db_table = "reviews"

    def __str__(self):
        return f"{self.user} - {self.tour} ({self.rating})"

class Notification(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    class Meta:
        db_table = "notification"

