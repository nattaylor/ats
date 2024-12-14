from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
import json
from .models import Job, JobForm, JobApplication, ApplyForm
from django.contrib.auth.models import User
import ats.helpers
from django_q.tasks import async_task
from django.contrib.auth import logout
from django.db.models import Count
from django.contrib.auth import login

def index(request):
    return jobs(request)

@login_required
def jobs(request):
    jobs = Job.objects.filter(user=request.user).order_by('-id').annotate(othermodel_count=Count('jobapplication'))
    return render(request, 'ats/jobs.html', {"jobs":jobs})

@login_required
def edit(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    if request.user.id != job.user_id and not request.user.is_staff:
        return HttpResponse("You are not authorized to edit this job")
    if request.method == "POST":
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
        else:
            return HttpResponse("Invalid form")
        return HttpResponseRedirect(reverse("jobs"))
    return render(request, 'ats/job.html', {"job":job, "form":JobForm(instance=job)})

@login_required
def create(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")
    job = Job(job_title=request.POST["job_title"], location="", description='', user=request.user)
    job.save()
    print(job.id)
    ats.helpers.generate_job_description, request.POST["job_title"], job.id
    return render(request, 'ats/creating.html', {"job":job})
    # return HttpResponseRedirect(reverse("edit", args=(job_id,)))

def opening(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    employer = get_object_or_404(User, pk=job.user_id)
    return render(request, 'ats/opening.html', {"job":job, "employer":employer})

def apply(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    employer = get_object_or_404(User, pk=job.user_id)
    if request.method == "POST":
        form = ApplyForm(request.POST, request.FILES)
        if form.is_valid():
            # breakpoint()
            ja = form.save()
            # async_task(ats.helpers.extract_resume, request.FILES["resume"].file, ja.id)
            ats.helpers.extract_resume(ja.id)
            ats.helpers.transcribe(ja.id)
        else:
            return HttpResponse(json.dumps(form.errors))
        return render(request, 'ats/applied.html', {"job":job})
    return render(request, 'ats/apply.html', {"job":job, "employer":employer, "form":ApplyForm()})

def candidates(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    if request.user.id != job.user_id and not request.user.is_staff:
        return HttpResponse("You are not authorized to edit this job")
    candidates = JobApplication.objects.filter(job=job).order_by('-score')
    return render(request, 'ats/candidates.html', {"job":job, "candidates":candidates})

def hire(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("jobs"))
    if request.method == "POST":
        if ats.helpers.is_free(request.POST["username"]):
            return HttpResponse("Use work email")
        user = User(username=request.POST["username"], email=request.POST["username"])
        user.set_password(request.POST["password"])
        user.save()
        if request.POST['description']:
            job = Job(job_title=request.POST["description"], location="", description='', user=user)
            job.save()
            ats.helpers.generate_job_description(request.POST["description"], job.id)
            # async_task(ats.helpers.generate_job_description, request.POST["description"], job.id)
        login(request, user)
        return HttpResponseRedirect(reverse("jobs"))    
    return render(request, 'ats/hire.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("jobs"))

def candidate(request, job_id, candidate_id):
    job = get_object_or_404(Job, pk=job_id)
    if request.user.id != job.user_id and not request.user.is_staff:
        return HttpResponse("You are not authorized to edit this job")
    return render(request, 'ats/candidate.html', {
        "candidate":get_object_or_404(JobApplication, pk=candidate_id),
        "job": get_object_or_404(Job, pk=job_id),
    })