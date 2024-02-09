from typing import Optional
import json

from django.http import HttpRequest

# from django.db.models.query import QuerySet
from django.conf import settings
from djongo import models as mongomod

from nosql_adapter import MongoPolar

# from .utils import _create_ttype_dict, _return_configttype, _set_cache_trainingdata


# Create your models here.
class AbstractSpeedModel(mongomod.Model):
    _id = mongomod.ObjectIdField(primary_key=False)
    avg = mongomod.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    max = mongomod.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    avg_corr = mongomod.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )

    class Meta:
        abstract = True


class SpeedModel(AbstractSpeedModel):
    _id = mongomod.ObjectIdField(primary_key=True)

    class Meta:
        abstract = False


class AbstractHeartrateModel(mongomod.Model):
    avg = mongomod.FloatField(null=True, blank=True)
    max = mongomod.FloatField(null=True, blank=True)
    min = mongomod.FloatField(null=True, blank=True)

    class Meta:
        abstract = True


class HeartrateModel(AbstractHeartrateModel):
    _id = mongomod.ObjectIdField(primary_key=True)

    class Meta:
        abstract = False


class CadenceModel(AbstractHeartrateModel):
    _id = mongomod.ObjectIdField(primary_key=True)

    class Meta:
        abstract = False


class PowerModel(AbstractHeartrateModel):
    _id = mongomod.ObjectIdField(primary_key=True)

    class Meta:
        abstract = False


class AbstractLapArray(mongomod.Model):
    lapNumber = mongomod.IntegerField()
    duration = mongomod.CharField(max_length=50)
    splitTime = mongomod.CharField(max_length=50)
    heartRate = mongomod.EmbeddedField(HeartrateModel, null=True, blank=True)
    speed = mongomod.EmbeddedField(SpeedModel, null=True, blank=True)
    distance = mongomod.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    ascent = mongomod.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    descent = mongomod.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    cadence = mongomod.EmbeddedField(CadenceModel, null=True, blank=True)
    power = mongomod.EmbeddedField(PowerModel, null=True, blank=True)

    class Meta:
        abstract = True


class AbstractLaps(AbstractLapArray):
    class Meta:
        abstract = True


class Laps(AbstractLaps):
    _id = mongomod.ObjectIdField(primary_key=True)

    class Meta:
        abstract = False


class AbstractTrainingtype(mongomod.Model):
    easyrun = mongomod.BooleanField(null=True)
    interval = mongomod.CharField(max_length=50, blank=True)
    roadrace = mongomod.BooleanField(null=True)
    sprint = mongomod.BooleanField(null=True)
    # other = mongomod.CharField(max_length=50)

    class Meta:
        abstract = True


class TrainingtypeModel(AbstractTrainingtype):
    _id = mongomod.ObjectIdField()

    class Meta:
        abstract = False


class AbstractTrainingDescr(mongomod.Model):
    description = mongomod.TextField(max_length=256, null=True, blank=True)
    type = mongomod.CharField(max_length=20, null=True, blank=True)

    class Meta:
        abstract = True


class TrainingDescription(AbstractTrainingDescr):
    _id = mongomod.ObjectIdField()

    class Meta:
        abstract = False


# class TrainingDescriptionForm(forms.ModelForm):
#     class Meta:
#         model = TrainingDescription
#         fields = "__all__"


class PolarModel(mongomod.Model):
    _id = mongomod.ObjectIdField(primary_key=True)
    sport = mongomod.CharField(max_length=256, default="RUNNING")
    fname = mongomod.CharField(max_length=80)
    location = mongomod.CharField(max_length=30, blank=True)
    distance = mongomod.IntegerField()
    duration = mongomod.DecimalField(
        decimal_places=1, max_digits=5, null=True, blank=True
    )
    startTime = mongomod.CharField(max_length=20)
    stopTime = mongomod.CharField(max_length=20)

    latitude = mongomod.DecimalField(
        decimal_places=6, max_digits=8, null=True, blank=True
    )
    longitude = mongomod.DecimalField(
        decimal_places=6, max_digits=8, null=True, blank=True
    )
    speed = mongomod.EmbeddedField(model_container=SpeedModel, null=True, blank=True)
    maximumHeartRate = mongomod.IntegerField(null=True, blank=True)
    averageHeartRate = mongomod.IntegerField(null=True, blank=True)
    heartRate = mongomod.EmbeddedField(
        model_container=HeartrateModel, null=True, blank=True
    )
    alaps = mongomod.ArrayField(model_container=Laps, null=True, blank=True)
    laps = mongomod.ArrayField(model_container=Laps, null=True, blank=True)
    trainingtype = mongomod.EmbeddedField(
        model_container=TrainingtypeModel,
        null=True,
        blank=True,
        model_form_kwargs={
            "initial": {
                "easyrun": None,
                "interval": None,
                "roadrace": None,
                "sprint": None,
            }
        },
    )
    trainingdescription = mongomod.EmbeddedField(
        model_container=TrainingDescription,
        # model_form_class=TrainingDescriptionForm,
        model_form_kwargs={"initial": {"description": "Initial Description"}},
    )

    db_table = mongomod.CharField(max_length=28, default="polar2019")

    objects = mongomod.DjongoManager()

    def __str__(self):
        return f"PolarModel: id={self.pk}, sport={self.sport}, fname={self.fname}, location={self.location}"

    class Meta:
        db_table = "polar2019"
        app_label = "test_polar"
        managed = False

    @classmethod
    def set_dtable(cls, tablename):
        cls._meta.db_table = tablename

    @classmethod
    def return_lapdata(cls, fname: str) -> list[Optional[dict]]:
        training = cls.objects.filter(fname=fname).first()
        if training:
            lapdata = training.laps
            alapdata = training.alaps
            if lapdata is None or len(lapdata) == 0:
                return alapdata
            # else:
            return lapdata
        return []

    @classmethod
    def _return_trainrunning(cls) -> list[Optional[dict]]:
        training = cls.objects.filter(sport="RUNNING")
        if len(training) > 0:
            return list(training.values())

        else:
            return []

    @classmethod
    def _return_trainttype(cls, ttype: str) -> list[Optional[dict]]:
        if ttype == "sprint":
            comp = True
        elif ttype == "easy":
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

        training = cls.objects.filter(trainingtype={ttype: comp})
        trainingen = [t for t in training.values()]
        return trainingen

    @classmethod
    def _return_trainingdata(cls, fname: str) -> dict:
        trainingen = cls.objects.filter(fname=fname)
        return trainingen.values()[0]

    @classmethod
    def _return_trainingdate(cls, fname: str):
        training = cls._return_trainingdata(fname)
        trainingdate = training["startTime"]
        return trainingdate

    @classmethod
    def _return_training_adaptdata(cls, fname: str):
        training = PolarModel._return_trainingdata(fname)

        location = training["location"]

        training = PolarModel._return_trainingdata(fname)
        location = training["location"]
        try:
            description = training["trainingdescription"]["description"]
        except (KeyError, TypeError):
            description = "unknown"

        try:
            description = training["trainingdescription"]["description"]
        except (KeyError, TypeError):
            description = "unknown"

        interval = training["trainingtype"].get("interval")
        sprint = training["trainingtype"].get("sprint")
        easy = training["trainingtype"].get("easyrun")
        road = training["trainingtype"].get("roadrace")
        initdict = {
            "location": location,
            "fname": fname,
        }

        hackdict = {
            "trainingdescription": {"description": description, "type": ""},
            "trainingtype": {
                "interval": interval,
                "sprint": sprint,
                "easyrun": easy,
                "roadrace": road,
            },
        }
        return initdict, hackdict

    @classmethod
    def delete_training(cls, request):
        data = json.loads(request.body.decode("utf-8"))
        print(data)
        # xx
        fname = data.pop("fname", None)
        cls.objects.filter(fname=fname).delete()
        # trainingen = cls._return_trainrunning()

    @classmethod
    def _set_database_adapt(cls, request):
        new_trainingtype = _create_ttype_dict(request)
        new_description = request.POST["trainingdescription-description"]
        print(new_description)
        new_location = request.POST["location"]
        fname = request.POST["fname"]
        print(fname)

        training = cls._return_trainingdata(fname)

        obj_id = training["_id"]

        database = settings.DATABASES["default"]["NAME"]
        db_table = cls._meta.db_table

        mongpol = MongoPolar(database, db_table)
        mongpol.updateOne(
            obj_id,
            {
                "location": new_location,
                "trainingdescription": {"description": new_description},
                "trainingtype": new_trainingtype,
            },
        )

    # @classmethod
    # def using_mongo(cls):
    #     return cls.objects.using("default")


class FormModel(mongomod.Model):
    _id = mongomod.ObjectIdField(primary_key=True)
    fname = mongomod.CharField(max_length=80)
    location = mongomod.CharField(max_length=30)
    # trainingtype = mongomod.EmbeddedField(
    #     model_container=TrainingtypeModel, null=True, blank=True
    # )
    trainingdescription = mongomod.EmbeddedField(
        model_container=TrainingDescription,
    )

    class Meta:
        # db_table = "polar2022"
        # app_label = "test_training2"
        managed = False


def _create_ttype_dict(request: HttpRequest) -> dict:
    # terribly hacky, but for now it's alright
    ttype_db = {}
    ttypes = {"interval", "sprint", "roadrace", "easyrun"}
    for tt in ttypes:
        new_val = request.POST["trainingtype-" + tt]
        if tt != "interval":
            if new_val == "unknown" or "":
                new_val = None
            elif new_val == "false":
                new_val = False
            else:
                new_val = True
        ttype_db.update({tt: new_val})
    return ttype_db
