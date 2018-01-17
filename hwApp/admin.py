from django.contrib import admin

# Register your models here.
from hwApp.models import Person, Group, Membership

admin.site.register(Person)
admin.site.register(Group)
admin.site.register(Membership)

#
# @admin.register(Person)
# class PersonAdmin(admin.ModelAdmin):
#     list_display = ('user',
#
#                     'email',
#                     'first_name',
#                     'last_name'
#                     )
#
#
# class MembershipInline(admin.TabularInline):
#     model = Membership
#     extra = 1
#     verbose_name_plural = 'Groups list'
#
#
# @admin.register(Group)
# class GroupAdmin(admin.ModelAdmin):
#     list_display = ('name', 'genre', 'description', 'pic')
#     # inlines = (BelongTOInline,)
