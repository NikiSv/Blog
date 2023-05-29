from django import forms
from django.contrib.auth.models import User
from .models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['author']
        labels = {
            'text': 'Текст',
            'pub_date': 'Дата и время публикации',
            'author': 'Автор публикации',
            'location': 'Местоположение',
            'category': 'Категория'
        }
        widgets = {
            'text': forms.Textarea(),
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        help_texts = {
            'text': 'Введите текст публикации',
            'pub_date': 'Если установить дату и время в будущем — '
            'можно делать отложенные публикации.'
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'username']
