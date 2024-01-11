from django import forms

from test_polar.models import PolarModel


class formType(forms.Form):
    # def __init__(self, inittext):
    ttype = forms.CharField(max_length=20)


class locationForm(forms.ModelForm):
    class Meta:
        model = PolarModel
        fields = ("location",)
        # fields = ["laps", "alaps"]
        # fields = "__all__"
