from typing import Union
import asyncio

from django.contrib.auth.backends import ModelBackend

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings

from .forms import UserProfileForm, UserForm

# from loginregister.models import Trainingtype  # , PolarModel#, Testpage, PolarModel

import main_start_djangopolar as startpolar


def login_page(request: HttpRequest) -> HttpResponse:
    return render(request, "login.html")


def register_page(request: HttpRequest) -> HttpResponse:
    return render(request, "register.html")


# @login_required
# def start_test_project2(request: HttpRequest) -> HttpResponse:
#     start_project2 etcetera


@login_required
def logout_user(request: HttpRequest) -> HttpResponse:
    logout(request)
    return HttpResponseRedirect("login.html")


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
        # print(user)
        # print(user.check_password(password))
        # ccc
        # print(
        #     ModelBackend().authenticate(request, password=password, username=username)
        # )
        # print(ModelBackend)
        # xxx
        # print(username)
        # print(password)
        # print(user)
        # xxx
        # user, auth_failure_reason = custom_authenticate(
        #     request, username=username, password=password
        # )
        # if user is not None:
        #     print("yes")
        # Authentication successful
        # Continue with your logic...
        # else:
        # Authentication failed
        # if auth_failure_reason:
        #     print(f"Authentication failed: {auth_failure_reason}")
        # else:
        #     print("Authentication failed for unknown reason")

        # print(user)
        if user:
            if user.is_active:
                login(request, user)
                # asyncio.run(startpolar.main())
                # startpolar.main()
                return HttpResponseRedirect("/clienthandling/login")
            else:
                HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("login failed")
            return HttpResponse("LOGIN FAILED")
    else:
        print("jojo")
        return render(request, "login.html")

    return render(request, "login.html")


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
