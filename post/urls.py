from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('posts/<int:postsId>/', views.postDetail , name = 'post_detail'),
    path('' , views.homePage , name = 'home'),
    path('posts/', views.postList , name = 'post_list'),
    path('postlist/', views.createPost, name='create_post'),
    path('commentlist/<int:postId>/comments/', views.createComment, name='create_comment'),
    path('comments/<int:id>/', views.commentList, name='commentlist'),
    path('login_register/', views.login_register, name='login_register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/' , views.profile , name='profile'),
    path('posts/<int:post_id>/', views.postDetail, name='post_detail'),
    path('posts/new/', views.createPost, name='create_post'),
    path('users/<int:usersId>/', views.userProfile, name='user_detail'),
    path('myposts/', views.myposts, name='myposts'),
    path('edit/<int:post_id>/', views.editPost, name='editpost'),
    path('delete/<int:post_id>/', views.deletePost, name='deletepost'),
    path('chatroom/<str:recipient_username>/', views.chatroom, name='chatroom'),
    path('my_chats/', views.my_chats, name='my_chats'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

