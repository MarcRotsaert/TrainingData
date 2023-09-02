# Processing data export polar data json files

import os
import glob
import json

import tomli

from lap_analyzer import RManualLapAnalyzer, RAutoLapAnalyzer
from sample_analyzer import SampleAnalyzerBasic, SamAnalExtra


class Trainses:
    def add_data(self, data: dict):
        def _set_data_nonexercise(data):
            # self.samples = data.pop("samples")
            self.laps = data.pop("laps")
            self.alaps = data.pop("autolaps")
            return data

        def _set_data_exercise(data):
            config = tomli.load(open("config.toml", "rb"))
            for dtype in config["polar_json"]["datatypes"]:
                if dtype == "autolaps":
                    dtype_attr = "alaps"
                else:
                    dtype_attr = dtype

                if dtype in data["exercises"][0]:
                    setattr(self, dtype_attr, data["exercises"][0].pop(dtype))
                else:
                    setattr(self, dtype_attr, None)

            param = config["running"]["overall_param"]
            for par in param:
                if par in data["exercises"][0]:
                    data.update({par: data["exercises"][0][par]})
            data.pop("exercises")
            return data

        # self.data = data
        if "exercises" in data:
            data = _set_data_exercise(data)
        else:
            data = _set_data_nonexercise(data)
        self.abstract = data
        self.data = True

    def return_laps(self) -> list[dict]:
        return self.laps

    def return_autolaps(self) -> list[dict]:
        return self.alaps

    def return_sport(self) -> str:
        return self.abstract["sport"]


class Trainses_json(Trainses):
    def __init__(self, path: str, file: str):
        self.path = path
        self.file = file
        self.laps = []
        self.alaps = []
        self.abstract = {}
        data = self._read_json()

        self.add_data(data)
        self.data = True

    def _read_json(self) -> None:
        with open(os.path.join(self.path, self.file)) as g:
            temp = g.read()
        data = json.loads(temp)
        data.update({"fname": self.file})
        return data


class Trainses_mongo(Trainses):
    def __init__(self, mongorecord):
        self.add_data(mongorecord)


if __name__ == "__main__":
    config = tomli.load(open("config.toml", "rb"))
    path = config["polar_json"]["datapath"]

    if False:
        file = "training-session-2015-06-26-263879702-2d485ab0-ef26-4100-b2ae-1ca9c5f144d6.json"
        # file = "training-session-2019-10-30-4009640085-5105bf47-b37c-47c3-a96c-d74653ae0d5a.json"
        # training-session-2015-07-03-263876996-e9c14b6c-bc80-4c10-b335-91081c2552e7.json
        # training-session-2015-09-20-263873564-7f116bac-8756-4f54-a5a0-9272ec0f44ee.json
        # training-session-2015-09-29-263860670-b456e24e-4325-411f-b2c6-3e3a3bc29de6.json
        # training-session-2015-10-24-263861018-3690058d-71c0-47c3-8539-e7b67e8099fe.json
        # training-session-2015-10-17-263860916-1b563b91-c4f4-4991-878c-5c1225f84b2c.json
        session = Trainses_json(path, file)
        laps = session.return_laps()
        lapses = RManualLapAnalyzer(laps)

        x = lapses.return_paraslist("speed")
        result = lapses.determine_startuprunoutlaps()
        print(lapses.identify_interval())
        samses = SamAnalExtra(session.samples)
        samses.plot("speed")
        # xx

    if True:
        file = "training-session-2015-01-14-263888618-3d72bde3-4957-4db4-8fa6-662a180a2d23.json"
        session = Trainses_json(path, file)
        lapses = RAutoLapAnalyzer(session.alaps)
        result = lapses.identify_roadrace()
        # xx
    if True:
        file = "training-session-2015-04-18-263883440-3be46e75-6a93-4746-a320-96c9660f809c.json"
        session = Trainses_json(path, file)
        laps = session.return_laps()
        lapses = RManualLapAnalyzer(session.laps)

    if True:
        samses = SampleAnalyzerBasic(session.samples)
        samses = SamAnalExtra(session.samples)
        X = samses.return_idxlowmovement()

    files = glob.glob(os.path.join(path, "training-session-2022-*.json"))
    pointcoll = []
    for fi in files[0:5]:
        filename = fi.split("\\")[-1]
        print(filename)
        session = Trainses_json(path, filename)

        if True:
            if session.laps is not None:
                lapses = RManualLapAnalyzer(session.laps)
                lapses.compare_hr_sp()
        if True:
            if session.laps is not None:
                lapses = RManualLapAnalyzer(session.laps)
                result = lapses.identify_interval()
                print(result)

                result = lapses.identify_sprints()
                print("sprints? " + str(result))

            if session.alaps is not None:
                # try:
                lapses = RManualLapAnalyzer(session.alaps)
                result = lapses.identify_easyrun()
                print("easyrun?" + str(result))
                # except:
                #    pass

            print("_______________________________")
        if True:
            samses = SamAnalExtra(session.samples)
            samses.plot("speed")
        if True:
            samples = samses.return_samples()

            print(samses.determine_s_location())
            print(samses.samples)
