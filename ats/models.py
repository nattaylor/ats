from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import ModelForm
from django import forms


# Create your models here.

class Job(models.Model):
    def __str__(self):
        return self.job_title
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    job_title = models.CharField(max_length=255)
    location = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    question = models.TextField(null=True)
    skill = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

class JobForm(ModelForm):
    class Meta:
        model = Job
        fields = '__all__'
        widgets = {
            "job_title": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full max-w-xs",
                }
            ),
            "location": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full max-w-xs",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered w-full max-w-xs",
                    "rows": 5,
                }
            ),
            "status": forms.Select(
                attrs={"class": "select select-bordered w-full max-w-xs"}
            ),
            "user": forms.HiddenInput()
        }

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.TextField()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.DO_NOTHING)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    resume = models.FileField()
    video = models.FileField(null=True)
    resume_text = models.TextField(null=True)
    transcription = models.TextField(null=True)
    job_title = models.TextField(null=True)
    analysis = models.TextField(null=True)
    score = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

class ApplyForm(ModelForm):
    class Meta:
        model = JobApplication
        fields = ['first_name', 'last_name', 'email', 'resume', 'video', 'job']
        widgets = {
            "job": forms.HiddenInput(),
            "first_name": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full max-w-xs",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full max-w-xs",
                }
            ),
            "email": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full max-w-xs",
                }
            ),
            "video": forms.FileInput(
                attrs={
                    "style": "display: none;",
                    "id": "videocap",
                }
            ),
        }