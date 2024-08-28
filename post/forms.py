from django import forms
from .models import Post, Comment, CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2' , 'is_active')


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=254)
    password = forms.CharField(label="Password", strip=False, widget=forms.PasswordInput)

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                "This account is inactive.",
                code='inactive',
            )