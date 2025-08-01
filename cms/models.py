from django.db import models

from core.models import BaseModel


class StaticPage(BaseModel):
    SLUG_CHOICES = [
        ('ABOUT','About'),
        ('PRIVACY','Privacy Policy'),
        ('TERMS','Terms & Conditions'),
        ('FAQ','Faq'),
    ]
    slug = models.SlugField(max_length=50, choices=SLUG_CHOICES, unique=True)
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255, null=True, blank=True)
    title_en = models.CharField(max_length=255, null=True, blank=True)
    content_uz = models.TextField()
    content_ru = models.TextField(null=True, blank=True)
    content_en = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.slug

    class Meta:
        db_table = 'static_page'
