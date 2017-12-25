from django.contrib import admin

# Register your models here.
from hwApp.models import Person, Group, Membership

admin.site.register(Person)
admin.site.register(Group)
admin.site.register(Membership)