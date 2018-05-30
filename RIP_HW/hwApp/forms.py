from django import forms
from .models import *


# форма регистрации
class RegistrationForm(forms.Form):
    username = forms.CharField(min_length=5, label='Логин')
    password = forms.CharField(min_length=8, widget=forms.PasswordInput, label='Пароль')
    password2 = forms.CharField(min_length=8, widget=forms.PasswordInput, label='Повторите ввод')
    email = forms.EmailField(label='Email')
    last_name = forms.CharField(label='Фамилия')
    first_name = forms.CharField(label='Имя')


class AuthorizationForm(forms.Form):
    username = forms.CharField(label='Логин')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')


class GroupForm(forms.ModelForm):
    class Meta(object):
        model = Group
        fields = ['name', 'genre', 'description', 'pic']

    # def save(self):
    #     group = Group()
    #
    #     group.name = self.cleaned_data.get('name')
    #
    #     group.genre = self.cleaned_data.get('genre')
    #
    #     group.description = self.cleaned_data.get('description')
    #     group.pic = self.cleaned_data.get('pic')
    #     group.save()


class CommentForm(forms.Form):
    text = forms.CharField(max_length=100, widget=forms.Textarea(attrs={'class': 'form-control'}))
