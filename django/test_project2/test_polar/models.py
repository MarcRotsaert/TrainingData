from djongo import models as mongomod


# Create your models here.
class AbstractSpeedModel(mongomod.Model):
    _id = mongomod.ObjectIdField(primary_key=True)
    avg = mongomod.DecimalField(max_digits=5, decimal_places=2)
    max = mongomod.DecimalField(max_digits=5, decimal_places=2)
    avg_corr = mongomod.DecimalField(max_digits=5, decimal_places=2)

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

    class Meta:
        abstract = False


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
    description = mongomod.TextField(max_length=256)
    type = mongomod.CharField(max_length=20)

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
    duration = mongomod.DecimalField(decimal_places=1, max_digits=5)
    startTime = mongomod.CharField(max_length=20)
    stopTime = mongomod.CharField(max_length=20)

    latitude = mongomod.DecimalField(decimal_places=6, max_digits=8)
    longitude = mongomod.DecimalField(decimal_places=6, max_digits=8)
    speed = mongomod.EmbeddedField(model_container=SpeedModel)
    heartRate = mongomod.EmbeddedField(model_container=HeartrateModel)
    alaps = mongomod.ArrayField(model_container=Laps)
    laps = mongomod.ArrayField(model_container=Laps)
    trainingtype = mongomod.EmbeddedField(model_container=TrainingtypeModel)
    trainingdescription = mongomod.EmbeddedField(model_container=TrainingDescription)
    objects = mongomod.DjongoManager()

    class Meta:
        db_table = "polar2014"
        app_label = "test_training2"
        managed = False

    @classmethod
    def using_mongo(cls):
        return cls.objects.using("default")


class PolarModel_test(mongomod.Model):
    _id = mongomod.ObjectIdField(primary_key=True)
    sport = mongomod.CharField(max_length=256, default="RUNNING")
    speed = mongomod.EmbeddedField(model_container=SpeedModel)
    heartRate = mongomod.EmbeddedField(model_container=HeartrateModel)
    trainingtype = mongomod.EmbeddedField(model_container=TrainingtypeModel)
    objects = mongomod.DjongoManager()

    class Meta:
        db_table = "polar2014"
        app_label = "test_training2"
        managed = False
        abstract = False

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
