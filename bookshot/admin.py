from django.contrib import admin
from .models import Quote, Book



class QuoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'quotation')

admin.site.register(Quote, QuoteAdmin)
admin.site.register(Book)
