"""
URL configuration for project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from ats import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", views.index, name="jobs"),
    path("jobs/<int:job_id>/", views.opening, name="opening"),
    path("jobs/<int:job_id>/edit/", views.edit, name='edit'),
    path("jobs/<int:job_id>/apply/", views.apply, name='apply'),
    path("jobs/<int:job_id>/candidates/", views.candidates, name='candidates'),
    path("jobs/<int:job_id>/candidates/<int:candidate_id>/", views.candidate, name='candidate'),
    path("jobs/create", views.create, name="create"),
    path("__debug__/", include("debug_toolbar.urls")),
    path("hire/", views.hire, name="signup"),
    path("logout/", views.logout_view, name="logout"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
