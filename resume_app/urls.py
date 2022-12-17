"""
            ------------------------------------------------------------
            |                   Aknowledgement                         |
            |----------------------------------------------------------|
            |   Project Name : Resume Screening Using Machine Learning |
            |   Coded By : Eng. Karim Mohammed Aboelazm                |
            |   Organization : Obour University                        |
            |----------------------------------------------------------|
"""
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

app_name = "resume_app"
urlpatterns = [
   
    path("", ResumeView.as_view(), name="resume"),
    path("hr/", HRView.as_view(), name="hr"),
    path("login/", HRLoginView.as_view(), name="login"),
    path("logout/", HRLogoutView.as_view(), name="logout"),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


