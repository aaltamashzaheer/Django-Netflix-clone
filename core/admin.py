from django.contrib import admin
from .models import Profile,CustomUser,Movie,Video


admin.site.register(Movie)
admin.site.register(Profile)
admin.site.register(CustomUser)
admin.site.register(Video)