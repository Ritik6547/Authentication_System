from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from AuthSystem import settings
from django.core.mail import send_mail



# Create your views here.
def home(request):
    if request.user.is_anonymous:
        return redirect('/')
    return render(request,'home.html')

def index(request):
    return render(request,'index.html')

def signup(request):
    context = {'fail':False}
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            return render(request,'signup.html',{'existed':True})

        if User.objects.filter(email=email):
            return render(request,'signup.html',{'register':True})

        if len(username)>10:
            return render(request,'signup.html',{'user_len':True})

        if not username.isalnum():
            return render(request,'signup.html',{'alpha':True})

        if pass1=='':
            return render(request,'signup.html',{'empty':True})
            
        if pass1==pass2:
            user = User.objects.create_user(username,email,pass1)
            user.first_name = fname
            user.last_name = lname
            user.save()

            subject = "Welcome to my auth system"
            message = "Hello "+user.first_name+"!!\n"+"Welcome to my auth system!! \n Thank you for visiting my website \n We have sent you a confirmation email,please confirm your email address to activate account. \n\n Thanking you\n Ritik Kumar"
            from_email = settings.EMAIL_HOST_USER
            to_list = [user.email]
            send_mail(subject,message,from_email,to_list,fail_silently=True)
            
            return render(request,'signin.html',{'success':True})
        else:
            context = {'fail':True}
            return render(request,'signup.html',context)

    return render(request,'signup.html')

def signin(request):
    context = {'wrong':False}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('/home')
        else:
            context = {'wrong':True}
            return render(request,'signin.html',context)
    return render(request,'signin.html')

def signout(request):
    logout(request)
    return redirect('/')