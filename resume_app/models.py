"""
            ------------------------------------------------------------
            |                   Aknowledgement                         |
            |----------------------------------------------------------|
            |   Project Name : Resume Screening Using Machine Learning |
            |   Coded By : Eng. Karim Mohammed Aboelazm                |
            |   Organization : Obour University                        |
            |----------------------------------------------------------|
"""
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Resume(models.Model):
    resume = models.FileField(upload_to='resume/')
    def __str__(self):
        return "Resume - "+str(self.id)

class ResumeAnalysis(models.Model):
    R_name = models.ForeignKey(Resume, on_delete=models.CASCADE)
    E_name = models.CharField(max_length=255)
    E_email = models.EmailField()
    R_score = models.IntegerField()
    R_prediction = models.CharField(max_length=255)
    def __str__(self):
        return "Resume Analysis - "+ str(self.id)

class HR(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='HR/')
    phone = models.CharField(max_length=15,blank=True, null=True)
    join_on = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.full_name

