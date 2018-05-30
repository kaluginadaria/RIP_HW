from django.contrib import admin

# Register your models here.
from hwApp.models import Person, Group, Comment, Genre, Like




class PersonAdmin(admin.ModelAdmin):
    list_display = ('user',


                    )



class GroupAdmin(admin.ModelAdmin):
    list_display = ('user',
                    'name',

                    'rating'
                    )
admin.site.register(Person, PersonAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Comment)
admin.site.register(Genre)
admin.site.register(Like)

#
#
# @admin.register(Group)
# class GroupAdmin(admin.ModelAdmin):
#     list_display = ('name', 'genre', 'description', 'pic')
#     # inlines = (BelongTOInline,)
