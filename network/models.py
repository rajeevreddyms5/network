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


# create model for following users
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name='following')

    def follow(self, user):
        """
        Adds a user to the set of followers.

        Parameters:
            user (User): The user to be added as a follower.

        Returns:
            None
        """
        self.followers.add(user)

    def unfollow(self, user):
        """
        Removes a user from the list of followers.

        Parameters:
            user (str): The username of the user to be unfollowed.

        Returns:
            None
        """
        self.followers.remove(user)
    
    def __str__(self):
        return f"{self.user} : {self.followers}"
