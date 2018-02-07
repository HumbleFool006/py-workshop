from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
class UserInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=30, null=False)
    mobile_no = models.CharField(max_length=30, null=False)
