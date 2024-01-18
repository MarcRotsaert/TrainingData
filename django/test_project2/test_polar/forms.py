from django import forms

from test_polar.models import PolarModel, TrainingDescription


class formType(forms.Form):
    # def __init__(self, inittext):
    ttype = forms.CharField(max_length=20)


class TrainingDescriptionForm(forms.ModelForm):
    class Meta:
        model = TrainingDescription
        fields = ("description", "type")


class locationForm(forms.ModelForm):
    trainingdescription = TrainingDescriptionForm()

    class Meta:
        model = PolarModel
        fields = ("fname", "location", "trainingdescription")
        # fields = ["laps", "alaps"]
        # fields = "__all__"
