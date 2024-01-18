from djongo import models as mongomod


# Create your models here.
class AbstractSpeedModel(mongomod.Model):
    _id = mongomod.ObjectIdField(primary_key=True)
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
    interval = mongomod.CharField(max_length=50)
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


class PolarModel(mongomod.Model):
    _id = mongomod.ObjectIdField(primary_key=True)
    sport = mongomod.CharField(max_length=256, default="RUNNING")
    fname = mongomod.CharField(max_length=80)
    location = mongomod.CharField(max_length=30)
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
        model_container=TrainingtypeModel, null=True, blank=True
    )
    trainingdescription = mongomod.EmbeddedField(model_container=TrainingDescription)
    objects = mongomod.DjongoManager()

    class Meta:
        db_table = "polar2022"
        app_label = "test_training2"
        managed = False

    # @classmethod
    # def using_mongo(cls):
    #     return cls.objects.using("default")
