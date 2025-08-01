from django.db import models

from core.models import BaseModel


class ContactRequest(BaseModel):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    message = models.TextField()

    class Meta:
        db_table = "contact"

    def __str__(self):
        return f"{self.name} - {self.phone}"

