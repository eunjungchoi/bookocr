from django.contrib import admin

# Register your models here.

from django.contrib import admin

from .models import Quote, Book



class QuoteAdmin(admin.ModelAdmin):
    list_display = ('date',)

admin.site.register(Quote, QuoteAdmin)
admin.site.register(Book)
