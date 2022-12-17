"""
            ------------------------------------------------------------
            |                   Aknowledgement                         |
            |----------------------------------------------------------|
            |   Project Name : Resume Screening Using Machine Learning |
            |   Coded By : Eng. Karim Mohammed Aboelazm                |
            |   Organization : Obour University                        |
            |----------------------------------------------------------|
"""
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from django.views.generic import CreateView,TemplateView,FormView,View
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth import authenticate , login ,logout
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier
from django.urls import reverse_lazy,reverse
from .models import Resume,ResumeAnalysis
from pyresparser import ResumeParser
from django.shortcuts import render
from django.db.models import Q
from .courses import *
from .forms import *
import pandas as pd
import numpy as np
import random
import spacy
import fitz
# Create your views here.
spacy.load('en_core_web_sm')

def train_test_sgd_classifier():
    # Train and test algorithm
    df = pd.read_csv('job_desc_csv_fixed_url.csv')
    X_train, X_test, y_train, y_test = train_test_split(df.job_descriptions, df.search_term, random_state=0)

    count_vect = CountVectorizer(stop_words='english')
    X_train_counts = count_vect.fit_transform(X_train)

    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

    clf = SGDClassifier(loss='hinge', penalty='l1', alpha=1e-3, random_state=42, max_iter=5, tol=None)
    clf.fit(X_train_tfidf, y_train)

    preds = clf.predict(count_vect.transform(X_test))
    accuracy = np.mean(preds==np.array(y_test))

    return clf, count_vect, accuracy


class ResumeMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and HR.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/login/")
        return super().dispatch(request, *args, **kwargs)

class ResumeView(CreateView):
    template_name = 'home.html'
    form_class = ResumeForm
    success_url = '/'
    def form_valid(self, form):
        resume = form.cleaned_data.get('resume')
        return super(ResumeView,self).form_valid(form)

    def Convert_Pdf_To_Text(self,pdf_url):
        with fitz.open(pdf_url) as doc:
            text = ""
            for page in doc:
                text += page.get_text()
        return text

    def predict_resume(self,resume_text):
        # Run predict on trained algorithm
        text_as_series = pd.Series(resume_text)
        clf, count_vect, _ = train_test_sgd_classifier()
        prediction = clf.predict(count_vect.transform(text_as_series))
        return prediction[0]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resume_path= Resume.objects.latest('id')
        resume_name = resume_path.resume.name
        name_resume = resume_name[resume_name.index('/')+1:]
        text = self.Convert_Pdf_To_Text(f"media\\resume\\{name_resume}")
        resume_data = ResumeParser(f"media\\resume\\{name_resume}").get_extracted_data()
        context['res']=resume_path
        context['prediction'] = self.predict_resume(text)
        context['name'] = resume_data['name']
        context['email'] = resume_data['email']
        if resume_data['mobile_number'] == None:
            context['mobile'] = 'Not Found'
        elif resume_data['mobile_number']:
            context['mobile'] = resume_data['mobile_number']
        else:
            context['mobile'] = resume_data['phone_number']
        context['skills'] = resume_data['skills']
        context["resume_score"] = 0
        if 'Objective' in text:
            context['objective'] = "Awesome! You have added Objective"
            context["resume_score"] += 20
        else:
            context['objective'] = "According to our recommendation please add your career objective, it will give your career intension to the Recruiters."
        
        if 'Declaration' in text:
            context['declaration'] = "Awesome! You have added Declaration"
            context["resume_score"] += 20
        else: 
            context['declaration'] = "According to our recommendation please add Declaration✍. \nIt will give the assurance that everything written on resume is true and fully acknowledged by you"
        
        if 'Hobbies' or 'Interests'in text:
            context['hobbies'] = "Awesome! You have added Hobbies"
            context["resume_score"] += 20
        else:
            context['hobbies'] = "According to our recommendation please add Hobbies⚽.\nIt will show your persnality to the Recruiters and give the assurance that you are fit for this role or not."
        
        if 'Achievements' in text:
            context['achievements'] = "Awesome! You have added Achievements"
            context["resume_score"] += 20
        else:
            context['achievements'] = "According to our recommendation please add Achievements🏅. \nIt will show that you are capable for the required position."
        
        if 'Projects' in text:
            context['projects'] = "Awesome! You have added Projects"
            context["resume_score"] += 20
        else:
            context['projects'] = "According to our recommendation please add Projects📝. \nIt will show your skills and knowledge about the required position."
        
        if 'Python' in context['prediction']:
            context['courses_list']= [link for link in random.sample(Python_Courses, 6)]
        if 'ui' in context['prediction']:
            context['courses_list']= [link for link in random.sample(Ui_Courses, 6)]
        if 'web' in context['prediction']:
            context['courses_list']= [link for link in random.sample(Web_Courses, 6)]
        if 'JavaScript' in context['prediction']:
            context['courses_list']= [link for link in Js_Courses]
        elif 'android' in context['prediction']:
            context['courses_list']= [link for link in random.sample(Android_Courses, 6)]

        context['resume_improve']= [link for link in random.sample(resume_videos, 4)]

        context['interview_improve']= [link for link in random.sample(interview_videos, 4)]
        
       
        if not ResumeAnalysis.objects.filter(E_email=context['email']):
            ResumeAnalysis.objects.create(R_name=resume_path,E_name=context['name'],E_email=context['email'],R_score=context['resume_score'],R_prediction=context['prediction'])
        else:
            pass
        return context

class HRView(ResumeMixin,TemplateView):
    template_name = 'hr.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get('keyword')
        if kw:
            context['resume_analysis']= ResumeAnalysis.objects.filter(Q(R_prediction__icontains=kw)) 
        else:
            context['resume_analysis']= ResumeAnalysis.objects.all()
        current_user = self.request.user
        context["hr"] = HR.objects.get(user=current_user) 
        return context
    
class HRLoginView(FormView):
    template_name = 'login.html'
    form_class = HRLoginForm
    success_url = reverse_lazy('resume_app:hr')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self,form):
        user_name = form.cleaned_data.get('username')
        pass_word = form.cleaned_data['password']
        usr = authenticate(username=user_name,password=pass_word)
        if usr is not None and HR.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request,self.template_name,{'form':self.form_class})
        return super().form_valid(form)
    
    def get_success_url(self):
        if 'next' in self.request.GET:
            next_url = self.request.GET.get('next')
            return next_url
        else:
            return self.success_url

# customer logout
class HRLogoutView(View):
    def get(self,request):
        logout(request)
        return redirect('resume_app:resume')
