# Determine training type and set traing info in Mongo DB.
import abc
from typing import Generator, Union

import nosql_adapter as mongodb
from trainsession import Trainsession_mongo


class MongoClassifier(metaclass=abc.ABCMeta):
    def __init__(self, dbase: str, collection: str):
        self.mongo = mongodb.MongoPolar(dbase, collection)
        self.sport = "RUNNING"

    @abc.abstractmethod
    def _return_session(self, mongorecord: dict) -> Trainsession_mongo:
        pass

    @abc.abstractmethod
    def _generator_training(self) -> Generator:
        pass


class MongoRunningClassifier(MongoClassifier):
    def _return_session(self, mongorecord) -> Trainsession_mongo:
        return Trainsession_mongo(mongorecord)

    def _generator_training(self) -> Generator:
        # yield all trainingen, from self.sport
        trainingen = self.mongo.simplequery("sport", self.sport)
        for training in trainingen:
            yield self._return_session(training)

    def set_roadrace(self) -> None:
        fnamerr = self.return_roadrace()
        for fname in fnamerr:
            result = self.mongo.simplequery("fname", fname)
            for res in result:
                objid = res["_id"]
                self.mongo.updateOne(objid, {"trainingtype.roadrace": True})

    def return_roadrace(self) -> set:
        traingen = self._generator_training()
        race_laps = []
        race_alaps = []

        for training in traingen:
            if training.laps is not None:
                result1 = self._return_roadrace_laps(training)
                if result1 is not False:
                    race_laps.append(result1)

            result2 = self._return_roadrace_alaps(training)
            if result2 is not False:
                race_alaps.append(result2)

        set1 = set(race_laps)
        set2 = set(race_alaps)
        return set1.union(set2)

    def _return_roadrace_laps(self, training: Trainsession_mongo) -> Union[bool, str]:
        su, ro = training.RManualLapAnalyzer.determine_startuprunoutlaps()
        if su is None and ro is None:
            return False
        # if len(training.laps) != 0:
        #     return False
        # if training.laps[0]["speed"] is None:
        #     return False

        ignorelaps = []
        if su != [-1]:
            ignorelaps.extend(su)
        if ro != [99999]:
            ignorelaps.extend(ro)

        isroadrace = training.RManualLapAnalyzer.identify_roadrace(ignorelaps)
        if isroadrace:
            print(training.abstract["fname"])
            return training.abstract["fname"]
        else:
            return False

    def _return_roadrace_alaps(self, training: Trainsession_mongo) -> str or False:
        if training.alaps is None:
            return False

        if len(training.alaps) == 0:
            return False
        ri, ru = training.RAutoLapAnalyzer.determine_startuprunoutlaps()

        isroadrace = training.RAutoLapAnalyzer.identify_roadrace(ri + ru)
        if isroadrace:
            print(training.abstract["fname"])
            return training.abstract["fname"]
        else:
            return False

    def set_interval(self) -> None:
        trainingen = self.return_interval()
        for fname, descr in trainingen.items():
            cursor = self.mongo.simplequery("fname", fname)
            for res in cursor:
                objid = res["_id"]
                self.mongo.updateOne(
                    objid,
                    {"trainingtype.interval": descr},
                )

    def return_interval(self) -> dict:
        traingen = self._generator_training()
        intervaltr = {}
        for training in traingen:
            if training.laps is not None:
                # lapses = training.RManualLapAnalyzer
                if len(training.laps) != 0:
                    result = training.RManualLapAnalyzer.identify_interval()
                    intervaltr.update({training.abstract["fname"]: result})
        return intervaltr

    def set_easyrun(self) -> None:
        easyruns, no_easyruns = self.return_easyrun()

        for fname in easyruns:
            res = self.mongo.simplequery("fname", fname)
            for training in res:
                objid = training["_id"]
                self.mongo.updateOne(objid, {"trainingtype.easyrun": True})

        for fname in no_easyruns:
            res = self.mongo.simplequery("fname", fname)
            for training in res:
                objid = training["_id"]
                self.mongo.updateOne(objid, {"trainingtype.easyrun": False})

    def return_easyrun(self) -> list[str]:
        trainingen = self._generator_training()
        easyrun = []
        no_easyrun = []

        for training in trainingen:
            if training.laps is not None and len(training.laps) > 2:
                if training.RManualLapAnalyzer.identify_easyrun():
                    easyrun.append(training.abstract["fname"])
                else:
                    no_easyrun.append(training.abstract["fname"])

            else:
                if training.alaps is None:
                    continue
                if len(training.alaps) == 0:
                    continue
                if training.RAutoLapAnalyzer.identify_easyrun():
                    easyrun.append(training.abstract["fname"])
                else:
                    no_easyrun.append(training.abstract["fname"])

        return easyrun, no_easyrun

    def set_sprint(self) -> list[str]:
        fnamerr = self.return_sprint()
        for fname in fnamerr:
            result = self.mongo.simplequery("fname", fname)
            for res in result:
                objid = res["_id"]
                self.mongo.updateOne(objid, {"trainingtype.sprint": True})

    def return_sprint(self) -> list[str]:
        traingen = self._generator_training()
        sprint = []
        for training in traingen:
            if training.laps is not None:
                lapses = training.RManualLapAnalyzer
                if (len(training.laps) != 0) & (lapses.laps_an["speed"] is not None):
                    if lapses.identify_sprints():
                        sprint.append(training.abstract["fname"])
        return sprint

    def set_traindescription(self):
        traingen = self._generator_training()
        for training in traingen:
            # print(training.abstract["fname"])
            if training.laps is None:
                continue
            if "trainingtype" not in training.abstract:
                continue
            if training.abstract["trainingtype"]["interval"] in [
                "interval",
                "interval, check1",
                "interval, check2",
            ]:
                description = training.RManualLapAnalyzer.return_intervalstring()
                # print(description)
                result = self.mongo.simplequery("fname", training.abstract["fname"])
                for res in result:
                    objid = res["_id"]
                    self.mongo.updateOne(objid, {"trainingdescription": description})


class MongoIntervalTraining(MongoRunningClassifier):
    def _return_session(self, mongorecord) -> Trainsession_mongo:
        return Trainsession_mongo(mongorecord)

    def _generator_training(self) -> Generator:
        # yield all trainingen, from self.sport
        query = {
            "$and": [
                {"sport": "RUNNING"},
                {
                    "$or": [
                        {"trainingtype.interval": "interval"},
                        {"trainingtype.interval": "interval, check1"},
                        {"trainingtype.interval": "interval, check2"},
                    ]
                },
            ]
        }
        trainingen = self.mongo.morecomplexquery(query)
        for training in trainingen:
            yield self._return_session(training)

    def set_intervaldescription(self):
        train_gen = self._generator_training()

        # print(len(list(train_gen)))
        for training in train_gen:
            print(training)
            descr = training.RManualLapAnalyzer.return_intervalstring()
            objid = training.abstract["_id"]
            self.mongo.updateOne(
                objid,
                {"trainingdescription": {"type": "interval", "description": descr}},
            )

    def set_corrected_speed(self):
        train_gen = self._generator_training()
        for training in train_gen:
            int_strtype, _, _, _ = training.RManualLapAnalyzer.determine_intervals()
            if int_strtype == "distance":
                objid = training.abstract["_id"]
                idx_int, _ = training.RManualLapAnalyzer.return_idx_intrec()
                corr_speed = training.RManualLapAnalyzer.determine_corrspeed_int()

                for nr, ind in enumerate(idx_int):
                    self.mongo.updateOne(
                        objid,
                        {"laps." + str(ind) + ".speed.avg_corr": corr_speed[nr]},
                    )
