from django import forms

# from test_polar.models import PolarModel, TrainingDescription, TrainingtypeModel
from test_polar.models import PolarModel, FormModel, TrainingDescription


class formType(forms.Form):
    # def __init__(self, inittext):
    ttype = forms.CharField(max_length=20)


class adaptForm(forms.ModelForm):
    # trainingdescription = TrainingDescriptionForm()

    class Meta:
        model = PolarModel
        fields = ("fname", "location", "trainingdescription", "trainingtype")
        # fields = ["laps", "alaps"]
        # fields = "__all__"
