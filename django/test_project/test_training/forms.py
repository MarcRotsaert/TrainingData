from django import forms 
from .models import Trainingtype, Testpage
from django.core import validators

class TrainingForm(forms.Form):
    type_name = forms.CharField(max_length=50)
    image = forms.FileField(widget=forms.FileInput(attrs={
                            'class': 'form-control',
                            }))

# class Django_tut(forms.Form):
#     name = forms.CharField()
#     email = forms.EmailField(initial="mgl@testmail.up")
#     text = forms.CharField(widget=forms.Textarea, 
#                            initial="Whasup!", 
#                            help_text="Fill in Text!!")
#     date = forms.DateField()



class TrainingModelForm(forms.ModelForm):
    class Meta():
        model = Trainingtype
        fields = "__all__"
