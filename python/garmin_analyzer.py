import tomli
import xml.etree.ElementTree as ET

import garminfit_parser as gparser
from lap_analyzer import RManualLapAnalyzer, RAutoLapAnalyzer
from sample_analyzer import SampleAnalyzerBasic, SamAnalExtra


class Trainses:
    def add_data(self, data: dict):
        def _set_data_nonexercise(data):
            self.laps = data.pop("laps")
            return data

        def _set_data_exercise(data):
            config = tomli.load(open("config.toml", "rb"))
            for dtype in config["garmin_fit"]["datatypes"]:
                if dtype == "autoLaps":
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

        if "exercises" in data:
            data = _set_data_exercise(data)
        else:
            data = _set_data_nonexercise(data)
        self.abstract = data
        self.data = True


class Trainses_fit(Trainses):
    def __init__(self, path: str, file: str):
        self.path = path
        self.file = file
        self.laps = []
        self.alaps = []
        self.abstract = {}
        data = self._read_fit()

        self.add_data(data)
        self.data = True

    def _read_fit(self) -> None:
        data = gparser.Parser(self.file).fit2json()
        data.update({"fname": self.file})
        return data


if __name__ == "__main__":
    config = tomli.load(open("config.toml", "rb"))
    path = config["garmin_fit"]["datapath"]

    if True:
        file = "marcrotsaert_366197484.fit"
        session = Trainses_fit(path, file)
        lapses = RManualLapAnalyzer(session.laps)
        print(SamAnalExtra(session.samples).determine_s_location())
