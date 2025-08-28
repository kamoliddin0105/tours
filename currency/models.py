from django.db import models


class Currency(models.Model):
    CURRENCY_CHOICES = [
        ('EUR', 'Euro'),
        ('USD', 'USD'),
        ('UZS', 'UZS'),
    ]
    code = models.CharField(max_length=3, choices=CURRENCY_CHOICES, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'currencies'

    def __str__(self):
        return self.code
