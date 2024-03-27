from django import forms

from test_polar.models import PolarModel  # , FormModel, TrainingDescription


# class formType(forms.Form):
#     # def __init__(self, inittext):
#     ttype = forms.CharField(max_length=20)


class adaptForm(forms.ModelForm):
    # trainingdescription = TrainingDescriptionForm()

    def set_form_initial(self, initialdict, hackdict):
        # TODO: onderstaande netter maken. Het werkt niet.
        #  Waarschijnlijk op te lossen met apart model maken voor form ipv polarmodel
        # "trainingdescription": {"description": description, "type": ""},
        # "trainingdescription-description": "test",

        self.use_required_attribute = True
        self.initial = initialdict
        for vkey in hackdict:
            for skey in hackdict[vkey]:
                sval = hackdict[vkey][skey]
                self.fields[vkey].model_form_kwargs["initial"].update({skey: sval})
        print(self.fields)
        return self

    class Meta:
        model = PolarModel
        fields = ("fname", "location", "sport", "trainingdescription", "trainingtype")
        # fields = ["laps", "alaps"]
        # fields = "__all__"
