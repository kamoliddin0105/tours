from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True

class Infrastructure(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ChildFacility(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
