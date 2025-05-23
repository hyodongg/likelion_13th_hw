from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    email_address=models.EmailField(unique=True)
    profile_image=models.ImageField(upload_to="accounts/",blank=True,null=True)
