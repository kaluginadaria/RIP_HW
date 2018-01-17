from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, View
from django.views.generic import DetailView
import datetime

from hwApp.paginator import paginate
from .models import *


# Create your views here.
def home(request):
    parameters = {
        'header': "Содержимое"
    }
    return render(request, 'home.html', context=parameters)


# class GroupsView(ListView):
#     model = Group
#     template_name = 'home.html'
#     context_object_name = 'group_list'


def groups_view(request):
    group = Group.objects.all()
    print(group)
    page = request.GET.get('page')
    print(page)
    return render(request, "home.html", {'group_list': group, 'paginator': paginate(group, page)})


class PersonsView(ListView):
    model = Person
    template_name = 'home.html'
    context_object_name = 'persons_list'


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

    def save(self):
        group = Group()

        group.name = self.cleaned_data.get('name')

        group.genre = self.cleaned_data.get('genre')

        group.description = self.cleaned_data.get('description')
        group.pic = self.cleaned_data.get('pic')
        group.save()


def add(request):
    if request.method == 'POST':
        name1 = request.POST.get('name')
        genre1 = request.POST.get('genre')
        member = request.POST.get('member')
        date = request.POST.get('date')

        description1 = request.POST.get('description')
        pic1 = request.FILES.get('pic')
        group1 = Group(name=name1, genre=genre1, description=description1,
                       pic=pic1)

        group1.save()

        return HttpResponseRedirect('/item-' + str(group1.id))

    return render(request, 'add.html', locals())


# регистрация
def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
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
            pers = Person()
            pers.user = user
            pers.first_name = data['first_name']
            pers.last_name = data['last_name']

            pers.save()
            return HttpResponseRedirect('/authorization')
    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})


# авторизация django
def authorization(request):
    if request.method == 'POST':
        form = AuthorizationForm(request.POST)
        print(form)
        data = form.cleaned_data

        if form.is_valid():
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

    return render(request, 'authorization.html', {'form': form})


# успешная авторизация django
@login_required(login_url='/authorization')
def success_authorization(request):
    return HttpResponseRedirect('/')


# выход
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


class OneItem(DetailView):
    model = Group
    context_object_name = 'group'
    template_name = 'object.html'

    def get_context_data(self, **kwargs):

        context = super(OneItem, self).get_context_data(**kwargs)

        relation = Membership.objects.filter(group=self.kwargs['pk'])
        # print(relation)
        customers_list = []
        for rel in relation:
            group = Group.objects.get(id=rel.group_id)
            # print(group)
            member = Person.objects.get(id=rel.person_id)
            # print(member)
            if member not in customers_list:
                # print(member.user)
                customers_list.append(member.user)
        # print(customers_list)
        context['customers_list'] = customers_list
        context['group_id'] = self.kwargs['pk']

        return context


def enter(request):
    if request.method == "GET":
        user = User.objects.filter(username=request.GET['user_name'])
        pers = Person.objects.get(user=user)
        group = Group.objects.get(id=request.GET['group_id'])
        mem = Membership.objects.create(person=pers, group=group,
                                        date_joined=datetime.datetime.now().date())
        return HttpResponse('ok')
        print(group.id)
    #return HttpResponseRedirect('/item-' + str(group.id))
