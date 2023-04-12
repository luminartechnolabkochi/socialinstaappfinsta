from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.views.generic import CreateView,FormView,TemplateView,UpdateView
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy

from myapp.forms import SignUpForm,LoginForm,ProfileEditForm
from myapp.models import UserProfile


class SignUpView(CreateView):
    model=User
    form_class=SignUpForm
    template_name="register.html"
    success_url=reverse_lazy("signin")
    
    def form_valid(self, form):
        messages.success(self.request,"account has been created !!")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,"failed to create account!")
        return super().form_invalid(form)
    


    
class SignInView(FormView):
    form_class=LoginForm
    template_name="login.html"

    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                return redirect("index")
            messages.error(request,"inavlid credentilas")
        return render(request,self.template_name,{"form":form})



class IndexView(TemplateView):
    template_name="index.html"


class ProfileEditView(UpdateView):
    model=UserProfile
    form_class=ProfileEditForm
    template_name="profile_edit.html"
    success_url=reverse_lazy("index")
    


