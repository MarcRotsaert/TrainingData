from typing import Union

import tomli

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from .forms import UserProfileForm, UserForm

# from loginregister.models import Trainingtype  # , PolarModel#, Testpage, PolarModel


def login_page(request: HttpRequest) -> HttpRequest:
    return render(request, "login.html")


def register_page(request: HttpRequest) -> HttpRequest:
    return render(request, "register.html")


def registration(request: HttpRequest) -> HttpRequest:
    if request.method == "POST":
        userform = UserForm(data=request.POST)
        profileform = UserProfileForm(data=request.POST)
        if userform.is_valid() and profileform.is_valid():
            user = userform.save()
            user.set_password(user.password)

            profile = profileform.save(commit=False)
            profile.user = user
            # if profile_pics in request.FILES:
            #     profile.profile_pic = request.FILES["profile_pic"]
            profile.save()
            registered = True
            context = None
        else:
            print(userform.errors, profileform.errors)
            registered = False
            context = None
        return render(request, "register.html", context=context)
    else:
        userform = UserForm()
        profileform = UserProfileForm()
        context = {"userform": userform, "profileform": profileform}
        registered = False
        return render(request, "register.html", context=context)
