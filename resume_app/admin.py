"""
            ------------------------------------------------------------
            |                   Aknowledgement                         |
            |----------------------------------------------------------|
            |   Project Name : Resume Screening Using Machine Learning |
            |   Coded By : Eng. Karim Mohammed Aboelazm                |
            |   Organization : Obour University                        |
            |----------------------------------------------------------|
"""

from django.contrib import admin

from .models import *
# Register your models here.
admin.site.register(Resume)
admin.site.register(ResumeAnalysis)
admin.site.register(HR)