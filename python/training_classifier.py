# Setting training data in Mongo DB.
#
import polar_json as pj
import nosql_adapter as mongodb
from polar_base import Base_training_classifier
import time


class MongoRunningClassifier:
    def __init__(self, dbase, collection):

        self.mongo = mongodb.MongoPolar(dbase, collection)
        self.sport = "RUNNING"
        self.trainingtype Base_training_classifier.trainingtypes

    def print_trainingtypes(self):
        print(self.trainingtypes)

    def return_sesion(self, training):
        return pj.Trainses_mongo(training)

    def _generator_training(self):
        # yield all trainingen, from self.sport
        trainingen = self.mongo.simplequery("sport", self.sport)
        for training in trainingen:
            yield self.return_sesion(training)

    def set_roadrace(self):
        fnamerr = self._return_roadrace()
        for fname in fnamerr:
            result = self.mongo.simplequery("fname", fname)
            for res in result:
                objid = res["_id"]
                self.mongo.updateOne(objid, {"trainingtype.roadrace": True})

    def _return_interval(self):
        traingen = self._generator_training()
        intervaltr = {}
        for training in traingen:

            if training.laps != None:
                lapses = pj.RManualLapAnalyzer(training.laps)
                if (len(lapses.laps) != 0) & (lapses.laps["speed"] != None):
                    print(training.abstract["fname"])
                    print(lapses.laps["speed"])
                    print(len(lapses.laps))
                    # try:
                    su_laps = lapses.return_startuprunoutlaps()
                    ignorelaps = su_laps[0] + su_laps[1]
                    x = lapses.identify_interval()
                    # if x == True:
                    # print(lapses["fname"])
                    # print(training.abstract["fname"])
                    intervaltr.update({training.abstract["fname"]: x})
                    # except TypeError:
                    # print("Probabily no speed data ")
                    # time.sleep(1)
                    # pass
        return intervaltr

    def set_interval(self):
        trainingen = self._return_interval()
        for fname in trainingen:
            result = self.mongo.simplequery("fname", fname)
            for res in result:
                objid = res["_id"]
                self.mongo.updateOne(
                    objid, {"trainingtype.interval": trainingen[fname]}
                )

    def _return_roadrace(self):
        traingen = self._generator_training()
        race_alaps = []
        race_laps = []
        for training in traingen:
            if training.laps != None:
                lapses = pj.RManualLapAnalyzer(training.laps)
                if (len(lapses.laps) != 0) & (lapses.laps["speed"] != None):
                    su_laps = lapses.return_startuprunoutlaps()
                    ignorelaps = su_laps[0] + su_laps[1]
                    x = lapses.identify_roadrace(ignorelaps)
                    if x == True:
                        # print(lapses["fname"])
                        print(training.abstract["fname"])
                        race_laps.append(training.abstract["fname"])

            alapses = pj.RAutoLapAnalyzer(training.alaps)
            if len(alapses.laps) != 0:
                try:
                    x = alapses.identify_roadrace()
                except:
                    continue  # print("not good!")
                if x == True:
                    print(training.abstract["fname"])
                    race_alaps.append(training.abstract["fname"])

        set1 = set(race_laps)
        set2 = set(race_alaps)
        return set1.union(set2)

    def _return_easyrun(self):
        traingen = self._generator_training()
        easyrun = []

        for training in traingen:
            lapses = pj.RAutoLapAnalyzer(training.alaps)
            if len(lapses.laps) != 0:
                if lapses.identify_easyrun():
                    easyrun.append(training.abstract["fname"])
        return easyrun

    def set_easyrun(self):
        fnamerr = self._return_easyrun()
        for fname in fnamerr:
            result = self.mongo.simplequery("fname", fname)
            for res in result:
                objid = res["_id"]
                self.mongo.updateOne(objid, {"trainingtype.easyrun": True})

    def _return_sprint(self):
        traingen = self._generator_training()
        sprint = []
        for training in traingen:
            if training.laps != None:
                lapses = pj.RManualLapAnalyzer(training.laps)
                if (len(lapses.laps) != 0) & (lapses.laps["speed"] != None):
                    if lapses.identify_sprints():
                        sprint.append(training.abstract["fname"])
        return sprint

    def set_sprint(self):
        fnamerr = self._return_sprint()
        for fname in fnamerr:
            result = self.mongo.simplequery("fname", fname)
            for res in result:
                objid = res["_id"]
                self.mongo.updateOne(objid, {"trainingtype.sprint": True})


if __name__ == "__main__":
    classif = MongoRunningClassifier("polartest4", "polar2018")

    classif.set_interval()
    road_races = classif.mongo.simplequery("trainingtype.interval", "interval, check1")
    for rr in road_races:
        print(rr)
    print("___________________________________________________")

    classif.set_roadrace()
    road_races = classif.mongo.simplequery("trainingtype.roadrace", True)
    for rr in road_races:
        print(rr)
    print("___________________________________________________")
    classif.set_easyrun()
    road_races = classif.mongo.simplequery("trainingtype.easyrun", True)
    for rr in road_races:
        print(rr)
    print("___________________________________________________")
    classif.set_sprint()
    road_races = classif.mongo.simplequery("trainingtype.sprint", True)
    for rr in road_races:
        print(rr)
