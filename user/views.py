from django.shortcuts import render
from django.shortcuts import render,redirect,HttpResponse,reverse
from django.contrib import auth
from django.contrib.auth import authenticate,login


# Create your views here.
def index(request):
    return HttpResponse("index")

def userlogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username,password)
        user_obj = authenticate(username=username, password=password)
        print(user_obj)
        # print(request.user.is_authenticated())
        if user_obj:
            login(request, user_obj)
            return redirect('user:index')
        return redirect(reverse('user:login'))
    return HttpResponse("没有get")