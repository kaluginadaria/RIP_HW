"""RIP_HW URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import *
from hwApp.views import *
from RIP_HW.settings import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', groups_view, name='groups_url'),
    url(r'^listing_by_tag/', tag, name='listing_by_tag'),
    url(r'^registration/$', registration, name='registration'),
    url(r'^item-(?P<pk>[A-Za-z0-9- ]+)$', OneGroup, name='item_view'),
    url(r'^authorization/$', authorization, name='authorization'),
    url(r'^logout$', logout_view, name='logout'),
    url(r'^add/$', add, name='add'),
    url(r'^like1$', like, name='like'),
    url(r'^hot/$', hot, name='hot'),
    url(r'^success_authorization$', success_authorization, name='success_authorization'),
]
