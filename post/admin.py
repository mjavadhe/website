from django.contrib import admin
from .models import CustomUser , Post , Comment , Message


class CustomUserAdmin(admin.ModelAdmin):
    listDisplay = ['username', 'email', 'password']


admin.site.register(CustomUser, CustomUserAdmin)


class PostAdmin(admin.ModelAdmin):
    listDisplay = ['author', 'text' , 'image']


admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    listDisplay = ['author', 'post', 'text']


admin.site.register(Comment, CommentAdmin)


class MessageAdmin(admin.ModelAdmin):
    listDisplay = ['sender', 'recipient', 'content', 'timestamp']


admin.site.register(Message, MessageAdmin)