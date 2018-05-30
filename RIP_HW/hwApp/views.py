import operator

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, HttpResponseNotFound
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, View
from django.views.generic import DetailView
import datetime

from hwApp.paginator import paginate
from .models import *
from .forms import *


def groups_view(request):
    d = {group.id: Comment.objects.filter(group=group).count() for group in Group.objects.all()}
    print(d)
    group1 = Group.objects.all()
    page = request.GET.get('page')
    tag = Genre.objects.all()

    return render(request, "home.html", {'group_list': d, 'tag': tag, 'paginator': paginate(group1, page)})


def add(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        name1 = request.POST.get('name')
        user = Person.objects.get(user=request.user)
        # member = request.POST.get('member')
        date = request.POST.get('date')
        genres = request.POST.get('genre').split(' ')
        description = request.POST.get('description')
        pic1 = request.FILES.get('pic')
        rate = 0
        if name1 == None:
            form.add_error('name', ['Имя обязательно'])

        group1 = Group(user=user, name=name1, description=description, rating=rate,
                       pic=pic1)
        group1.save()
        print(group1.id)
        for i in genres:
            try:
                genre = Genre.objects.get(name=i)
                group1.genre.add(genre)

            except:
                genre = Genre(name=i)
                genre.save()
                group1.genre.add(genre)
            group1.save()
        group1.save()

        return HttpResponseRedirect('/item-' + str(group1.id))

    return render(request, 'add.html', locals())


# регистрация
def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        avatar = request.FILES.get('avatar')
        is_val = form.is_valid()
        data = form.cleaned_data

        if data['password'] != data['password2']:
            is_val = False
            form.add_error('password2', ['Пароли должны совпадать'])
        if User.objects.filter(username=data['username']).exists():
            form.add_error('username', ['Такой логин уже существует'])
            is_val = False

        if is_val:
            data = form.cleaned_data
            user = User.objects.create_user(data['username'], data['email'], data['password'])
            user.last_name = data['last_name']
            user.first_name = data['first_name']
            pers = Person()
            pers.user = user

            pers.avatar = avatar
            pers.save()
            print(pers)
            return HttpResponseRedirect('/authorization')
    else:
        form = RegistrationForm()
    tags = Genre.objects.all()
    return render(request, 'registration.html', {'form': form, 'tag': tags})


# авторизация django
def authorization(request):
    if request.method == 'POST':
        form = AuthorizationForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])
            # user = authenticate(request, username='petrov',password='12345678')
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/success_authorization')
            else:
                form.add_error('username', ['Неверный логин или пароль'])
                # raise forms.ValidationError('Имя пользователя и пароль не подходят')

    else:
        form = AuthorizationForm()
    tags = Genre.objects.all()
    return render(request, 'authorization.html', {'form': form, 'tag': tags})


# успешная авторизация django
@login_required(login_url='/authorization')
def success_authorization(request):
    return HttpResponseRedirect('/')


# выход
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def OneGroup(request, pk):
    try:
        group = Group.objects.get(id=pk)
    except:
        return HttpResponseNotFound('<h1>No Page Here</h1>')
    page = request.GET.get('page')
    comment = Comment.objects.filter(group=group)
    tag = Genre.objects.all()
    if request.method == 'POST':

        if request.user.is_authenticated:

            form = CommentForm(request.POST)
            is_val = form.is_valid()
            data = form.cleaned_data
            t = data['text']

            if is_val:
                comment = Comment.objects.create(
                    user=request.user.person,
                    group=group,
                    text=data['text'],
                )
                comment.save()

                return HttpResponseRedirect('/item-' + str(group.id))
        else:
            return HttpResponseRedirect('/authorization/')

    else:
        form = CommentForm()
    return render(request, 'object.html',
                  {'group': group, 'paginator': paginate(comment, page), 'form': form, 'tag': tag})


def tag(request):
    tag = Genre.objects.get(name=request.GET.get('tag'))
    data = Group.objects.filter(genre=tag)
    d = {group.id: Comment.objects.filter(group=group).count() for group in Group.objects.all()}

    print(tag)
    print(data)


    page = request.GET.get('page')
    tag = Genre.objects.all()

    return render(request, "home.html", {'group_list': d, 'tag': tag, 'paginator': paginate(data, page)})


def like(request):
    print((request.POST.get('group')))
    if request.method == 'POST':
        user = request.user
        group = Group.objects.get(id=int(request.POST.get('group')))
        if request.POST.get('positive') == 'true':
            print('positive')
            try:
                lk = Like(group=group, like_author=user, rate=True)
                lk.save()
                group.counter()
                group.save()
                return JsonResponse({'rating': group.rating}, status=200)
            except:
                lkk = Like.objects.get(group=group, like_author=user, rate=True)
                lkk.delete()
                group.counter()
                group.save()
                return JsonResponse({'rating': group.rating}, status=200)

        else:
            try:
                lk = Like(group=group, like_author=user, rate=False)
                lk.save()
                group.counter()
                group.save()
                return JsonResponse({'rating': group.rating}, status=200)
            except:
                lkk = Like.objects.get(group=group, like_author=user, rate=False)
                lkk.delete()
                group.counter()
                group.save()
                return JsonResponse({'rating': group.rating}, status=200)
    return HttpResponse()


def hot(request):
    d = {group.id: group.rating for group in Group.objects.all()}

    group1 = Group.objects.all().order_by("-rating")
    print(d)
    page = request.GET.get('page')
    tag = Genre.objects.all()

    return render(request, "home.html", {'group_list': d, 'tag': tag, 'paginator': paginate(group1, page)})
