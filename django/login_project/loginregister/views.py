import asyncio
import re
import os
from pathlib import Path
from typing import Union

from django.contrib.auth.backends import ModelBackend

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings

from .models import UserProfile
from .forms import UserProfileForm, UserForm

# from loginregister.models import Trainingtype  # , PolarModel#, Testpage, PolarModel

import main_start_djangopolar as startpolar


# def login_page(request: HttpRequest) -> HttpResponse:
#     return render(request, "login.html")


# def register_page(request: HttpRequest) -> HttpResponse:
#     return render(request, "register.html")


# @login_required
# def start_test_project2(request: HttpRequest) -> HttpResponse:
#     start_project2 etcetera


@login_required
def logout_user(request: HttpRequest) -> HttpResponse:
    logout(request)
    return HttpResponseRedirect("login.html")


def base(request: HttpRequest) -> HttpResponse:
    return render(request, "base.html")


def login_user(request: HttpRequest) -> HttpResponse:

    if request.method == "POST":
        print(request.POST)
        username = request.POST.get("username")
        password = request.POST.get("password")
        usermodel = get_user_model()
        # print(settings)
        print(password)
        user = usermodel._default_manager.get_by_natural_key(username)
        user = authenticate(username=username, password=password)
        # print(user.check_password(password))
        # print(
        #     ModelBackend().authenticate(request, password=password, username=username)
        # )

        if user:
            if user.is_active:
                login(request, user)
                idnr = user.pk
                x = UserProfile.get_entry(idnr)
                print(dir(x.first()))
                print(x.first())
                # xx
                _create_settings(x.first())
                _create_toml(x.first())
                # print(x[0].databasename)
                # print(x[0].host)
                # print(x[0].inlogname)
                # print(x[0].password)
                # xx
                asyncio.run(startpolar.main())
                # return HttpResponseRedirect(reverse("base"), context={"logedin": True})
                return render(request, "base.html", {"logedin": True})
            else:
                HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("login failed")
            return HttpResponse("LOGIN FAILED")
    # else:
    # print("jojo")
    # return render(request, "login.html")

    return render(request, "login.html")


def _create_settings(userprofile):
    basedir = settings.BASE_DIR
    homedir = Path(basedir).parent.parent.resolve()
    print(homedir)
    # xx
    polardir = r"django\test_project2\test_project2"
    # dummyfile = r"C:\Users\marcr\Polar\Polar\django\test_project2\test_project2\settings_dummy.py"

    dummyfile = os.path.join(homedir, polardir, "settings_dummy.py")
    outputfile = os.path.join(homedir, polardir, "settings.py")
    # outputfile = (
    #     r"C:\Users\marcr\Polar\Polar\django\test_project2\test_project2\settings.py"
    # )
    with open(dummyfile, "r") as g:
        text = g.read()
    textout = _replace_input(text, userprofile)
    with open(outputfile, "w") as f:
        f.write(textout)


def _create_toml(userprofile):
    # basedir = settings.BASE_DIR
    basedir = settings.BASE_DIR
    homedir = Path(basedir).parent.parent.resolve()
    # dummyfile = r"C:\Users\marcr\Polar\Polar\config_dummy.toml"
    dummyfile = os.path.join(homedir, "config_dummy.toml")
    # outputfile = r"C:\Users\marcr\Polar\Polar\config.toml"
    outputfile = os.path.join(homedir, "config.toml")
    with open(dummyfile, "r", encoding="utf-8") as g:
        # g = open(dummyfile, "r")
        text = g.read()
        g.close()
    textout = _replace_input(text, userprofile)
    with open(outputfile, "w", encoding="utf-8") as f:
        f.write(textout)


def _replace_input(text: str, userprofile) -> str:
    # inputtext = g.read()
    regex = re.findall("\{\{(\w+)\}\}", text)
    print(regex)

    for pattern in regex:
        try:
            repl = getattr(userprofile, pattern)
        except AttributeError:
            # print(repl)
            continue
        text = re.sub("\{\{" + pattern + "\}\}", str(repl), text)
    # print(text)
    return text


def registration(request: HttpRequest) -> HttpRequest:
    if request.method == "POST":
        userform = UserForm(data=request.POST)
        profileform = UserProfileForm(data=request.POST)
        if userform.is_valid() and profileform.is_valid():
            user = userform.save()
            user.set_password(user.password)
            user.save()

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


# def custom_authenticate(request, username=None, password=None):
#     """
#     Custom authentication function that provides a reason for authentication failure.
#     """
#     print(User.objects)
#     user = User.objects.filter(username=username).first()

#     if user is None:
#         return None, "User does not exist"  # Return reason for failure

#     if not user.is_active:
#         return None, "User account is inactive"  # Return reason for failure

#     if not user.password == password:
#         return None, "Incorrect password"  # Return reason for failure

#     return user, None  # Authentication successful, no reason for failure
