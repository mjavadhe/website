from django.shortcuts import render, redirect , get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Post , Comment , CustomUser
from django.http import HttpResponseRedirect
from .models import Post, Comment, CustomUser , Message
from django.contrib.auth import login, authenticate , get_user_model ,logout , update_session_auth_hash
from django.contrib.auth.decorators import login_required
import random
from django.db.models import Q
import mimetypes
from django.contrib import messages




@login_required(login_url='/login_register/')
def logout_view(request):
    logout(request)
    return redirect('login_register')


@login_required(login_url='/login_register/')
def homePage(request):
    return render(request, 'homepage.html')


@login_required(login_url='/login_register/')
def postList(request):
    posts = list(Post.objects.all())
    random.shuffle(posts)
    return render(request, 'explore.html', {'posts': posts})


@login_required(login_url='/login_register/')
def postDetail(request, postsId):
    post = Post.objects.get(pk=postsId)
    posts = Post.objects.get(pk=postsId), Post.objects.all()
    comments = Comment.objects.filter(post=post)
    context = {'posts': posts, 'comments': comments}
    return render(request, 'postdetail.html', context)


@login_required(login_url='/login_register/')
def createComment(request, postId):
    post = Post.objects.get(pk=postId)
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Comment.objects.create(author=request.user, post=post, text=text)
            return HttpResponseRedirect(reverse('post_detail', args=[postId]))
    return render(request, 'createcomment.html', {'post': post})


"""@login_required(login_url='/login_register/')
def createPost(request):
    user = CustomUser.objects.all()
    if request.method == 'POST':
        text = request.POST.get('text')
        image = request.FILES.get('image')
        if  text:
            post = Post(author=request.user, text=text , image=image)
            if image:
                post.image = image
            post.save()
            return redirect('post_detail', post_id=post.id)
    return render(request, 'createpost.html', {'user': user})
"""
@login_required(login_url='/login_register/')
def createPost(request):
    user = CustomUser.objects.all()
    if request.method == 'POST':
        text = request.POST.get('text')
        image = request.FILES.get('image')
        video = request.FILES.get('video')
        post = Post(author=request.user, text=text , image=image , video=video)
        post.text = request.POST.get('text')
        if 'file' in request.FILES:
            uploaded_file = request.FILES['file']
            if uploaded_file.content_type.startswith('image/'):
                post.image = uploaded_file
            elif uploaded_file.content_type.startswith('video/'):
                post.video = uploaded_file
        post.save()
        return redirect('post_detail', post_id=post.id)
    return render(request, 'createpost.html', {'user': user})


def login_register(request):
    if request.method == 'POST':
        if 'register' in request.POST:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = CustomUser.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('home')
        elif 'login' in request.POST:
            login_identifier = request.POST.get('login_identifier')
            password = request.POST.get('password')
            user = CustomUser.objects.filter(email=login_identifier).first() or CustomUser.objects.filter(username=login_identifier).first()
            if user:
                user = authenticate(request, username=user.username, password=password)
                if user is not None and user.is_active:
                    login(request, user)
                    return redirect('home')
    return render(request, 'form.html')


@login_required(login_url='/login_register/')
def profile(request):
    return render(request, 'profile.html')


@login_required(login_url='/login_register/')
def commentList(request, id):
    post = Post.objects.get(pk=id)
    posts = Post.objects.get(pk=id), Post.objects.all()
    comments = Comment.objects.filter(post=post)
    context = {'posts': posts, 'comments': comments}
    return render(request, 'commentlist.html', context)


@login_required(login_url='/login_register/')
def userProfile(request, usersId):
    users = CustomUser.objects.get(pk=usersId), CustomUser.objects.all()
    context = {'users': users}
    return render(request, 'usersprofile.html', context)
    

@login_required(login_url='/login_register/')
def myposts(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, 'mypost.html', {'posts': posts})


@login_required(login_url='/login_register/')
def editPost(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return render(request, 'donothavepermission.html')   
    if request.method == 'POST':
        post.text = request.POST.get('text')
        if 'file' in request.FILES:
            uploaded_file = request.FILES['file']
            if uploaded_file.content_type.startswith('image/'):
                post.image = uploaded_file
            elif uploaded_file.content_type.startswith('video/'):
                post.video = uploaded_file
        post.save()
        return redirect('post_detail', post_id=post.id)
    return render(request, 'editpost.html', {'post': post})


@login_required(login_url='/login_register/')
def deletePost(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return render(request , 'donothavepermission.html')   
    if request.method == 'POST':
        post.delete()
        return redirect('myposts')  
    
    return render(request, 'confirmdelete.html', {'post': post})


@login_required(login_url='/login_register/')
def chatroom(request, recipient_username):
    recipient = get_user_model().objects.get(username=recipient_username)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(sender=request.user, recipient=recipient, content=content)
        return redirect('chatroom', recipient_username=recipient_username)
    
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(recipient=recipient)) |
        (Q(sender=recipient) & Q(recipient=request.user))
    ).order_by('timestamp')
    
    return render(request, 'chatroom.html', {'recipient': recipient, 'messages': messages})


@login_required(login_url='/login_register/')
def my_chats(request):
    user = request.user
    sent_chats = Message.objects.filter(sender=user).values('recipient__username').distinct()
    received_chats = Message.objects.filter(recipient=user).values('sender__username').distinct()
    
    # Combine both querysets and remove duplicates
    chats = set(chat['recipient__username'] for chat in sent_chats).union(
            set(chat['sender__username'] for chat in received_chats))
    
    return render(request, 'my_chats.html', {'chats': chats})




User = get_user_model()

@login_required(login_url='/login_register/')
def edit_profile(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        user = request.user
        user.username = username
        user.email = email
        user.save()
        return redirect('profile')  # Redirect to profile page after saving changes
    return render(request, 'editprofile.html')
    
@login_required(login_url='/login_register/')

def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        if not request.user.check_password(old_password):
            messages.error(request, 'Old password is incorrect.')
        elif new_password1 != new_password2:
            messages.error(request, 'New passwords do not match.')
        else:
            request.user.set_password(new_password1)
            request.user.save()
            update_session_auth_hash(request, request.user)  # Keep the user logged in after password change
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')  # Redirect to profile page after changing password

    return render(request, 'changepassword.html')