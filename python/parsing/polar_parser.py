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
        data['duration'] = float( data['duration'].lstrip("PT").rstrip("S"))
        if 'laps' in data['exercises'][0]:
            for lap in data['exercises'][0]['laps']:
                lap['duration'] = float(lap['duration'].lstrip("PT").rstrip("S"))
        if 'autoLaps' in data['exercises'][0]:
            for alap in data['exercises'][0]['autoLaps']:
                alap['duration'] = float(alap['duration'].lstrip("PT").rstrip("S"))

        return data

class Parser(Polar_parser):
    def json2json(self):
        return self._read_json()

