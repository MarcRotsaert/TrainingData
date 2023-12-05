import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_project.settings")
import django
django.setup()

from test_training2.models import PolarModel

def populate(training: dict):
    for descr,fi in training.items():
        obj,res = Trainingtype.objects.get_or_create(type_name=descr, image=fi)
        if res:
            obj.save()


if __name__=="__main__":
    training = {"easy": "knmirotterdam_220616_11.png",
                "interval": "knmirotterdam_220719_15.png",
                "road race": "knmirotterdam_220814_07.png",
               }
    print("populate!!")
    # for t in training.items():
    populate(training)
    print("end populate")
