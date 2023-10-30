# Processing data export polar data json files

import tomli

from trainsession import Trainsession_file
import parsing.polar_parser as pparser


class Trainses_json(Trainsession_file):
    def __init__(self, file):
        super().__init__(file)

    def _return_path(self):
        config = tomli.load(open("config.toml", "rb"))
        return config["polar_json"]["datapath"]

    def _read_file(self) -> dict:
        data = pparser.Parser(self.file).json2json()
        data.update({"fname": self.file})
        return data

    def add_data(self, data: dict) -> None:
        def _set_data_nonexercise(data):
            self.laps = data.pop("laps")
            self.alaps = data.pop("alaps")
            return data

        def _set_data_exercise(data: dict):
            config = tomli.load(open("config.toml", "rb"))
            for dtype in config["polar_json"]["datatypes"]:
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


