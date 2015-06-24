from django.contrib import admin

from books.models import *
# Register your models here.
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Book)