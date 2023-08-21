from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


# create class model for posts, like and unlike
class Posts(models.Model):
    content = models.TextField(blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    liked = models.ManyToManyField(User, related_name="liked_post", blank=True)
    
    def __str__(self):
        return f"{self.author} : {self.content}"
    
    # serialze for api
    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "author": self.author,
            "created_at": self.created_at.strftime("%b %d %Y, %I:%M %p"),
            "liked": [user.username for user in self.liked.all()]
        }




    
