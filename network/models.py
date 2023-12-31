from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    # serialze for api
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name
        }


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
            "author": str(User.objects.get(id=self.author.id)),
            "created_at": self.created_at.strftime("%b %d %Y, %I:%M %p"),
            "liked": [user.username for user in self.liked.all()]
        }


# create model for following users
class UserProfile(models.Model):
    user_name = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE, null=True)
    follows = models.ForeignKey(User, related_name='followed_by', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.follows}"

    # serialze for api
    def serialize(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "follows": self.follows
        }