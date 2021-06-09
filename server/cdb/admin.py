from django.contrib import admin

from .models import *
############
class TagAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    
admin.site.register(Tag, TagAdmin)
