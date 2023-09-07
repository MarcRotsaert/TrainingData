import os
import tomli 
import pprint
import xml.etree.ElementTree as ET

import forerunner_parser as fparser
from lap_analyzer import RManualLapAnalyzer, RAutoLapAnalyzer
from sample_analyzer import SampleAnalyzerBasic, SamAnalExtra


class Trainses:
     def add_data(self, data: dict):
        def _set_data_nonexercise(data):
            # self.samples = data.pop("samples")
            self.laps = data.pop("laps")
            return data

        def _set_data_exercise(data):
            config = tomli.load(open("config.toml", "rb"))
            for dtype in config["forerunner_xml"]["datatypes"]:
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

         # self.data = data
        if "exercises" in data:
            data = _set_data_exercise(data)
        else:
            data = _set_data_nonexercise(data)
        self.abstract = data
        self.data = True       


class Trainses_xml(Trainses):
    def __init__(self, path: str, file: str):
        self.path = path
        self.file = file
        self.laps = []
        self.alaps = []
        self.abstract = {}
        data = self._read_xml()

        self.add_data(data)
        self.data = True

    def _read_xml(self) -> None:
        data = fparser.Parser(self.file).xml2json()
        
        # with open(os.path.join(self.path, self.file)) as g:
        #     temp = g.read()
        # data = json.loads(temp)
        data.update({"fname": self.file})
        return data


if __name__ == "__main__":
    config = tomli.load(open("config.toml", "rb"))
    path = config["forerunner_xml"]["datapath"]

    if True:
        file = '20050725-190632.xml'
        session = Trainses_xml(path, file)
        lapses = RManualLapAnalyzer(session.laps)
        SamAnalExtra(session.samples).determine_s_location()

        file = '20041008-170457.xml'
        session = Trainses_xml(path, file)
        # lapses = RManualLapAnalyzer(session.laps)
        # result = lapses.identify_roadrace()

