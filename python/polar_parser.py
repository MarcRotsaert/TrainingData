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
        return data


class Parser(Polar_parser):
    def json2json(self):
        return self._read_json()

if __name__=='__main__':
    filename = 'training-session-2014-01-03-263915750-ce8ea79c-8a35-43ed-8bc4-65733b407692.json'
    popa = Parser(filename).json2json()
    print(popa['exercises'][0])
    # popa.Lapparser()
