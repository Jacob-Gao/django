from django.shortcuts import render,redirect,HttpResponse
from app01 import models
from django.urls import reverse

def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        user = request.POST.get('username')
        pwd = request.POST.get('password')
        obj = models.Login_User.objects.all().first()
        if user == obj.name and pwd == obj.pwd:
            if request.POST.get('box') == "1":
                request.session['is_login'] = 'True'
            return render(request, 'index.html')
        else:
            return render(request, 'login.html', {'msg':'用户米或密码错误'})


def logout(request):
    request.session.clear()
    return redirect(reverse('login'))



def index(request):
    if request.session.get('is_login'):
        return render(request, 'index.html')
    else:
        return redirect(reverse('login'))
