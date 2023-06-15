from django.db import models
from django.contrib.auth.models import User

class BlogUser(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50, default='')
    interests = models.CharField(max_length=50, default='')
    skills = models.CharField(max_length=50, default='')
    profession = models.CharField(max_length=50, default='')
    picture = models.FileField(upload_to='uploads/')

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(max_length=50)
    user = models.ForeignKey(to=BlogUser, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    file = models.FileField(upload_to='uploads/')
    creation_date = models.DateTimeField(auto_now_add=True)
    last_modified_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(to=BlogPost, on_delete=models.CASCADE)
    user = models.ForeignKey(to=BlogUser, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

class Block(models.Model):
    blocker = models.ForeignKey(to=BlogUser, on_delete=models.CASCADE, related_name="user_blocker")
    blocked = models.ForeignKey(to=BlogUser, on_delete=models.CASCADE, related_name="user_blocked")


    def __str__(self):
        return str(self.blocker) + " blocked " + str(self.blocked)
