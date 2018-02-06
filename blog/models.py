from django.contrib import auth
from django.db import models
from django.utils import timezone

USER = auth.get_user_model()

class Post(models.Model):
    author = models.ForeignKey(USER, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
