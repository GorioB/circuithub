from django.contrib import admin
from circuits.models import RawList,CircuitList,RawElement

# Register your models here.
class RawElementInline(admin.StackedInline):
	model = RawElement
	extra = 3
class RawListAdmin(admin.ModelAdmin):
	fieldsets=[(None,{'fields':['owner','name']}),]
	inlines = [RawElementInline]

admin.site.register(RawList,RawListAdmin)