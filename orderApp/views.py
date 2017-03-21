#coding:utf-8
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpRequest
from orderApp.models import User
from django import forms

# Create your views here.


class UserForm(forms.Form):
    username = forms.CharField(label='用户名:', max_length=100)
    password = forms.CharField(label='密码:', widget=forms.PasswordInput())
    

def login(request):
    if request.method == 'GET':
        uf = UserForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            user = User.objects.filter(username__exact=username, password__exact=password)
            if user:
                return render(request, 'orderApp/index.html', {'username': username})
        else:
            uf = UserForm()
        return render(request, 'orderApp/login.html', {'uf': uf})
