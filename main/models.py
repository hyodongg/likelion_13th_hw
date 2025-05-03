from django.db import models

# Create your models here.
class Post(models.Model):
    title=models.CharField(max_length=30)
    writer=models.CharField(max_length=20)
    content=models.TextField()
    created_time=models.DateTimeField()
    updated_time=models.DateTimeField()
    feeling=models.CharField(max_length=10)
    image = models.ImageField(upload_to="post/",blank=True,null=True)

    def __str__(self):
        return self.title

    def summary(self):
        return self.content[:3]