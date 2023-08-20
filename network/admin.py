from django.contrib import admin
from .models import User, Posts

class PostsAdmin(admin.ModelAdmin):
    postdisplay = ("content", "created_at", "liked", "author")


# Register your models here.
admin.site.register(User)
admin.site.register(Posts, PostsAdmin)