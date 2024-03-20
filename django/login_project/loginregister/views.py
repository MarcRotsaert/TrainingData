import asyncio
import subprocess
import webbrowser
from pathlib import Path
from django.contrib.auth.decorators import login_required
from typing import Union

# Create your views here.
from django.shortcuts import render  # , redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth import get_user_model

from .models import UserProfile
from .forms import UserProfileForm, UserForm
from .utils import create_settings, create_toml  # , replace_input

# from loginregister.models import Trainingtype  # , PolarModel#, Testpage, PolarModel
# import main_start_djangopolar as startpolar


@login_required
def logout_user(request: HttpRequest) -> HttpResponse:
    logout(request)
    return HttpResponseRedirect("base.html")


def base(request: HttpRequest) -> HttpResponse:
    return render(request, "base.html")


def login_user(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        print(request.POST)
        username = request.POST.get("username")
        password = request.POST.get("password")
        usermodel = get_user_model()
        user = usermodel._default_manager.get_by_natural_key(username)

        # if authentication results in false, it doesn't give a clue why.
        user = authenticate(username=username, password=password)
        # print(user.check_password(password))
        # print(
        #     ModelBackend().authenticate(request, password=password, username=username)
        # )

        if user:
            if user.is_active:
                login(request, user)
                idnr = user.pk
                userprofile = UserProfile.get_entry(idnr)
                # print(x)
                create_settings(userprofile)
                create_toml(userprofile)
                asyncio.run(startpolar(request))
                return render(request, "base.html", {"logedin": True})
            else:
                HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("login failed")
            return HttpResponse("LOGIN FAILED")

    return render(request, "login.html")


def registration(request: HttpRequest) -> HttpResponse:
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
            # registered = True
            context = None
        else:
            print(userform.errors, profileform.errors)
            # registered = False
            context = None
        return render(request, "register.html", context=context)
    else:
        userform = UserForm()
        profileform = UserProfileForm()
        context = {"userform": userform, "profileform": profileform}
        # registered = False
        return render(request, "register.html", context=context)


@login_required
async def runserver_polar(request):
    rootpath = Path(__file__).parent.parent.parent.resolve()
    polarpath = Path(__file__).parent.parent.resolve()

    settingfile = "test_project2.settings"

    # os.system(
    #     "python django/test_project2/manage.py runserver "
    #     + "--settings="
    #     + settingfile
    #     + " "
    #     + "8001"
    # )
    process = subprocess.Popen(
        [
            # os.path.join(rootpath, "polar_env/Scripts/activate"),
            "python",
            "django/test_project2/manage.py",
            "runserver",
            "--settings=" + settingfile,
            "--noreload",
            "8001",
        ],
        shell=True,
        # stdout=open("stdout", "w"),
        # stderr=open("stdout", "w"),
    )
    print(process.poll())


def openpolar():
    webbrowser.open_new_tab("http://127.0.0.1:8001/home")


@login_required
async def startpolar(request):
    task1 = asyncio.create_task(runserver_polar(request))
    openpolar()
    await task1
