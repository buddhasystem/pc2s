from django.contrib import admin

from .models import *

######################################################################
class GlobalTagAdmin(admin.ModelAdmin):
    list_display=['name', 'n_tags']
    empty_value_display = '-empty-'

    def n_tags(self, obj):
        cnt = GlobalTagMap.objects.filter(globaltag=obj.name).count()
        return cnt

    n_tags.short_description = '# of Tags' #   my_url_field.allow_tags = True

admin.site.register(GlobalTag, GlobalTagAdmin)

############
class GlobalTagMapAdmin(admin.ModelAdmin):
    list_display=['name', 'globaltag','tag']
    empty_value_display = '-empty-'
admin.site.register(GlobalTagMap, GlobalTagMapAdmin)

############
class TagAdmin(admin.ModelAdmin):
    list_display=['name', 'until', 'n_payloads']
    empty_value_display = '-empty-'

    def n_payloads(self, obj):
        cnt = Payload.objects.filter(tag=obj.name).count()
        return cnt

    n_payloads.short_description = '# of Payloads'

admin.site.register(Tag, TagAdmin)

############
class PayloadAdmin(admin.ModelAdmin):
    list_display=['tag','since','url','name',]
    empty_value_display = '-empty-'


admin.site.register(Payload, PayloadAdmin)
