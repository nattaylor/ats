from django.contrib import admin

from .models import Job, Profile, JobApplication

admin.site.register(Job)
admin.site.register(Profile)
admin.site.register(JobApplication)

# Register your models here.
