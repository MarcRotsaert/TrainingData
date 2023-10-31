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
        return data


class Parser(Polar_parser):
    def json2json(self):
        return self._read_json()

