from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.views.generic import CreateView,FormView,TemplateView,UpdateView,ListView,DetailView
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy

from myapp.forms import SignUpForm,LoginForm,ProfileEditForm,PostForm
from myapp.models import UserProfile,Posts,Comments


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


class IndexView(CreateView,ListView):
    template_name="index.html"
    form_class=PostForm
    model=Posts
    context_object_name="posts"
    success_url=reverse_lazy("index")
    def form_valid(self,form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    def get_queryset(self):
        return self.model.objects.all().order_by("-created_date")


class ProfileEditView(UpdateView):
    model=UserProfile
    form_class=ProfileEditForm
    template_name="profile_edit.html"
    success_url=reverse_lazy("index")
    

# localhost:8000/posts/1/like/
def add_like_view(request,*args,**kwargs):
    id=kwargs.get("pk")
    post_obj=Posts.objects.get(id=id)
    post_obj.liked_by.add(request.user)
    return redirect("index")

  
# localhost:8000/posts/{id}/comments/add/

def add_comment_view(request,*args,**kwargs):
    id=kwargs.get("pk")
    post_obj=Posts.objects.get(id=id)
    comment=request.POST.get("comment")
    Comments.objects.create(user=request.user,post=post_obj,comment_text=comment)
    return redirect("index")


# localhost:8000/comments/{id}/remove/
def remove_comment_view(request,*args,**kwrags):
    id=kwrags.get("pk")
     
    comment_obj=Comments.objects.get(id=id)
    if request.user == comment_obj.user:
        comment_obj.delete()
        return redirect("index")
    else:
        messages.error(request,"plz contact admin")
        return redirect("signin")



class ProfileDetailView(DetailView):
    model=UserProfile
    template_name="profiledetail.html"
    context_object_name="profile"
