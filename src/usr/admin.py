from django.contrib import admin
from usr.models import Person, Location, Institution, Class, Course, PageMessages, EmailChange




admin.site.register(Person)
admin.site.register(Institution)
admin.site.register(Location)
admin.site.register(Class)
admin.site.register(Course)
admin.site.register(PageMessages)
admin.site.register(EmailChange)
