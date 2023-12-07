from djongo import models as mongomod


# Create your models here.
class AbstractSpeedModel(mongomod.Model):
    avg = mongomod.DecimalField(max_digits=5, decimal_places=2)
    max = mongomod.DecimalField(max_digits=5, decimal_places=2)
    avg_corr = mongomod.IntegerField()
    class Meta:
        abstract = True


class SpeedModel(AbstractSpeedModel):
    _id = mongomod.ObjectIdField(primary_key=True)

    class Meta:
        abstract = False


class AbstractHeartrateModel(mongomod.Model):
    avg = mongomod.IntegerField()
    max = mongomod.IntegerField()
    min = mongomod.IntegerField()


    class Meta:
        abstract = True


class HeartrateModel(AbstractHeartrateModel):
    _id = mongomod.ObjectIdField(primary_key=True)


class AbstractLapArray(mongomod.Model):
    lapNumber = mongomod.IntegerField()
    duration = mongomod.CharField(max_length=50)
    splitTime = mongomod.CharField(max_length=50)
    heartRate = mongomod.EmbeddedField(HeartrateModel)
    speed = mongomod.EmbeddedField(SpeedModel)
    distance = mongomod.DecimalField(max_digits=10, decimal_places=2)
    ascent = mongomod.DecimalField(max_digits=10, decimal_places=2)
    descent = mongomod.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        abstract = True


class AbstractLaps(AbstractLapArray):
    # mongomod.EmbeddedField(model_container=AbstractLapArray)
    class Meta:
        abstract = True


class Laps(AbstractLaps):
    _id = mongomod.ObjectIdField(primary_key=True)

    class Meta:
        abstract = False


class AbstractTrainingtype:
    easyrun = mongomod.BooleanField()
    interval = mongomod.CharField(max_length=50)
    roadrace = mongomod.BooleanField()

    class Meta:
        abstract = False


class TrainingtypeModel(AbstractTrainingtype):
    _id = mongomod.ObjectIdField(primary_key=True)

    class Meta:
        abstract = False


class PolarModel(mongomod.Model):
    _id = mongomod.ObjectIdField(primary_key=True)
    # garminfit = mongomod.JSONField()
    # sport = mongomod.CharField(max_length=256, default="RUNNING")

    sport = mongomod.CharField(max_length=256, default="RUNNING")
    fname = mongomod.CharField(max_length=80)
    locations = mongomod.CharField(max_length=30)
    distance = mongomod.IntegerField()
    duration = mongomod.DecimalField(decimal_places=1, max_digits=5)
    startTime = mongomod.CharField(max_length=20)
    stopTime = mongomod.CharField(max_length=20)

    latitude = mongomod.DecimalField(decimal_places=6, max_digits=8)
    longitude = mongomod.DecimalField(decimal_places=6, max_digits=8)
    speed = mongomod.EmbeddedField(model_container=SpeedModel)
    alaps = mongomod.ArrayField(model_container=Laps)
    laps = mongomod.ArrayField(model_container=Laps)
    # trainingtype = mongomod.EmbeddedField(model_containe=TrainingtypeModel)
    objects = mongomod.DjongoManager()

    class Meta:
        db_table = "polar2014"
        app_label = "test_training2"
        managed = False

    @classmethod
    def using_mongo(cls):
        return cls.objects.using("default")


# class Trainingtype(models.Model):
#    type_name = models.CharField(max_length=50, unique=True, primary_key=True)
# image = models.FileField(max_length=256)
#    datapath = models.FilePathField(max_length=256, path="C:/TEMP")

#    @classmethod
#    def using_sqlite(cls):
#        return cls.objects.using('mongo')
# class Trainingtype2(models.Model):
#     type_name = models.CharField(max_length=50, unique=True, primary_key=True)
#     image = models.FileField(max_length=256)
#     datapath = models.FilePathField(max_length=256, path="C:TEMP")


# class Testpage(models.Model):
#    name = models.CharField(max_length=20)
#    email = models.EmailField()
#    text = models.CharField(max_length=20)
#    date = models.DateField()
