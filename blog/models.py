from django.contrib import auth
from django.db import models
from django.utils import timezone
from django import forms
USER = auth.get_user_model()


CATEGORY_CHOICES= [
    (1, 'General'),
    (2, 'Technology'),
    (3, 'Inspirational')
    ]
class Post(models.Model):
    author = models.ForeignKey(USER, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)
    category = models.CharField(max_length=1, default="2")
    category = models.IntegerField(choices=CATEGORY_CHOICES, default=1)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
