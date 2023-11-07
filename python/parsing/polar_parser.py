import os
import tomli
import json


class Polar_parser:
    def __init__(self, filename: str):
        config = tomli.load(open("config.toml", "rb"))
        self.path = config["polar_json"]["datapath"]
        self.filename = filename

    def _read_json(self) -> dict:
        with open(os.path.join(self.path, self.filename)) as g:
            temp = g.read()
        data = json.loads(temp)
        sport = data["exercises"][0]["sport"]
        data.update({"sport": sport})
        data = self._tconv_duration(data)
        return data

    def _tconv_duration(self, data):
        data["duration"] = float(data["duration"].lstrip("PT").rstrip("S"))
        dur = data["exercises"][0]["duration"]
        dur = float(dur.lstrip("PT").rstrip("S"))
        data["exercises"][0]["duration"] = dur

        if "laps" in data["exercises"][0]:
            for i, lap in enumerate(data["exercises"][0]["laps"]):
                dur2 = float(lap["duration"].lstrip("PT").rstrip("S"))
                data["exercises"][0]["laps"][i]["duration"] = dur2

        if "autoLaps" in data["exercises"][0]:
            for i, alap in enumerate(data["exercises"][0]["autoLaps"]):
                dur3 = float(alap["duration"].lstrip("PT").rstrip("S"))
                data["exercises"][0]["autoLaps"][i]["duration"] = dur3
        return data


class Parser(Polar_parser):
    def json2json(self):
        return self._read_json()
