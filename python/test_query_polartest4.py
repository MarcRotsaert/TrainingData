from nosql_adapter import MongoPolar
import polar_json as pj
import time
from matplotlib import pyplot as pp

path = r"C:\Users\marcr\Polar\Polar\data\polar-user-data-export"
# files = glob.glob(os.path.join(path, "training-session-2015-*.json"))


# mongad = MongoPolar("polartest4", "polar2019")
mongad = MongoPolar("polartest4", "polar2018")

curs = mongad.simplequery("trainingtype.roadrace", True)

for res in curs:
    fname = res["fname"]
    print(fname)
    trainses = pj.Trainses(path, fname)
    samsess = pj.SamAnalExtra(trainses.samples)
    try:
        samsess.plot("speed")
    except:
        pass
    # samsess.plot("heartRate")
