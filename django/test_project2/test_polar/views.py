from typing import Union, Optional
import json
import tomli

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet
from django.core.cache import cache

from test_polar.forms import adaptForm  # , formType
from test_polar.models import PolarModel  # , PolarModel_test  # , Testpage

from nosql_adapter import MongoPolar


def _return_configttype() -> list[str]:
    # config = tomli.load(open("../../config.toml", "rb"))
    config = tomli.load(open("config.toml", "rb"))
    return config["running"]["trainingtypes"]


def _return_trainttype(connection: QuerySet, ttype: str) -> list[Optional[dict]]:
    if ttype == "easy":
        ttype = "easyrun"
        comp = True
    elif ttype == "road":
        ttype = "roadrace"
        comp = True
    elif ttype == "interval":
        comp = "interval"
    else:
        print(ttype)
        return []

    training = connection.filter(trainingtype={ttype: comp})
    trainingen = [t for t in training.values()]
    return trainingen


def _return_trainrunning(connection: QuerySet) -> list[Optional[dict]]:
    training = connection.filter(sport="RUNNING")
    if len(training) > 0:
        return [t for t in training.values()]
    else:
        return []


def _return_trainingdata(connection: QuerySet, fname: str) -> dict:
    trainingen = connection.filter(fname=fname)
    return trainingen.values()[0]


def _return_lapdata(connection: QuerySet, fname: str) -> list[Optional[dict]]:
    trainingen = connection.filter(fname=fname)
    if trainingen.values()[0]["laps"] is not None:
        return trainingen.values()[0]["laps"]
    else:
        return trainingen.values()[0]["alaps"]


def _set_cache_trainingdata(trainingen: list, cachetime: float):
    cache_key = "training_data"
    cache.clear()
    cache.set(cache_key, trainingen, cachetime)


def _set_database(request: HttpRequest, connection):
    new_description = request.POST["trainingdescription-description"]
    print(new_description)
    new_location = request.POST["location"]
    fname = request.POST["fname"]
    training = _return_trainingdata(connection, fname)
    obj_id = training["_id"]
    print(fname)
    db_table = PolarModel._meta.db_table
    config = tomli.load(open("config.toml", "rb"))
    database = config["mongodb"]["database"]

    mongpol = MongoPolar(database, db_table)
    mongpol.updateOne(
        obj_id,
        {
            "location": new_location,
            "trainingdescription": {"description": new_description},
        },
    )


def show_polar(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        connection = PolarModel.objects.using("default")

        if "ttypes" not in request.GET:
            trainingen = _return_trainrunning(connection)
            # training = connection.filter(sport="RUNNING")
        else:
            ttype = request.GET["ttypes"]
            print(len(ttype))
            print(ttype)

            trainingen = _return_trainttype(connection, ttype)
            print(len(trainingen))

        _set_cache_trainingdata(trainingen, 60)

        ttypes = _return_configttype()
        return render(
            request,
            "summary.html",
            context={
                "trainingen": trainingen,
                "ttypes": ttypes,
            },
        )
    else:
        return HttpResponse()


def action_adapt(request: HttpRequest) -> HttpResponse:
    connection = PolarModel.objects.using("default")
    trainingen = _return_trainrunning(connection)

    if request.method == "GET":
        # TODO: add logging
        print("GET action_adapt")
        # _set_cache_trainingdata(trainingen, 60)
    elif request.method == "POST":
        print(request.POST)
        # print(xx)
        _set_database(request, connection)
        trainingen = _return_trainrunning(connection)
    _set_cache_trainingdata(trainingen, 60)

    return render(
        request,
        "adapt.html",
        context={
            "trainingen": trainingen,
        },
    )


def _set_form_initial(form_class, initialdict, hackdict):
    # TODO: onderstaande functionerend maken. Het werkt niet.
    #  Waarschijnlijk op te lossen met apart model maken voor form ipv polarmodel
    # "trainingdescription": {"description": description, "type": ""},
    # "trainingdescription-description": "test",
    form_inst = form_class(
        use_required_attribute=True,
        initial=initialdict,
    )

    for vkey in hackdict:
        for skey in hackdict[vkey]:
            sval = hackdict[vkey][skey]

            form_inst.fields[vkey].model_form_kwargs["initial"].update({skey: sval})
    return form_inst


def show_form(request: HttpRequest, fname: str):
    print(__name__)
    connection = PolarModel.objects.using("default")
    if request.method == "GET":
        return request
    elif request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        fname = data.pop("fname", None)
        lapdata = _return_lapdata(connection, fname)

        training = _return_trainingdata(connection, fname)
        location = training["location"]
        try:
            description = training["trainingdescription"]["description"]
        except:
            description = "unknown"

        initdict = {
            "location": location,
            "fname": fname,
        }
        hackdict = {
            "trainingdescription": {"description": description, "type": ""},
        }
        adaptform = _set_form_initial(adaptForm, initdict, hackdict)

        print(adaptform.fields)
        print(adaptform.is_valid())
        print(adaptform.errors)
        print(dir(adaptform.fields["trainingdescription"]))

        print(adaptform.fields["trainingdescription"].model_form_class)
        # xx

        return render(
            request,
            "adapt.html",
            context={
                "lapdata": lapdata,
                "adaptform": adaptform,
            },
        )


def show_lapdata(request: HttpRequest, fname: str) -> Union[HttpResponse, JsonResponse]:
    if request.method == "GET":
        print(fname)

        connection = PolarModel.objects.using("default")
        lapdata = _return_lapdata(connection, fname)
        ttypes = _return_configttype()

        return render(
            request,
            "summary.html",
            context={
                "lapdata": lapdata,
                "ttypes": ttypes,
                # "trainingen": trainingen,
            },
        )
    return JsonResponse(
        {"status": "error", "message": "Invalid request method in " + __name__}
    )
