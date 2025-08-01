import uuid

from django.db import models

from core.models import BaseModel


class ContentBlock(BaseModel):
    key = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    title = models.CharField(max_length=100)
    body = models.TextField()
