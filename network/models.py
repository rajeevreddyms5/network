from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


# create class model for posts, like and unlike
class Post(models.Model):
    content = models.TextField(blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    liked = models.ManyToManyField(User, related_name="liked_post", blank=True)
    
    def __str__(self):
        return f"{self.author} : {self.content}"
    
    
    from django.db import models
from django.contrib.auth.models import User




    
