from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Tag(models.Model):
    name=models.CharField(max_length=30,null=False,blank=False)

    def __str__(self):
        return self.name

class Post(models.Model):
    title=models.CharField(max_length=30)
    writer=models.ForeignKey(User,null=False,blank=False,on_delete=models.CASCADE)
    content=models.TextField()
    created_time=models.DateTimeField()
    updated_time=models.DateTimeField()
    feeling=models.CharField(max_length=10)
    image = models.ImageField(upload_to="post/",blank=True,null=True)
    tags=models.ManyToManyField(Tag,related_name='posts',blank=True)

    def __str__(self):
        return self.title

    def summary(self):
        return self.content[:3]

class Comment(models.Model):
    content=models.TextField()
    pub_date=models.DateTimeField()
    writer=models.ForeignKey(User,null=False,blank=False,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,null=False,blank=False,on_delete=models.CASCADE)

    def __str__(self):
        return self.blog.title+":"+self.content[:20]+"by"+self.writer.profile.nickname
