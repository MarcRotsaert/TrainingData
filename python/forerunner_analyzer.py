import tomli

import forerunner_parser as fparser


class Trainses:
    def add_data(self, data: dict) -> dict:

        def _set_data_exercise(data: dict) -> dict:
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

        if 'exercises' in data:
            data = _set_data_exercise(data)
        self.abstract = data
        self.data = True


class Trainses_xml(Trainses):
    def __init__(self, file: str):
        config = tomli.load(open("config.toml", "rb"))
        self.path = config["forerunner_xml"]["datapath"]        
        self.file = file
        self.laps = []
        self.alaps = []
        self.abstract = {}
        data = self._read_xml()

        self.add_data(data)
        self.data = True

    def _read_xml(self) -> dict:
        data = fparser.Parser(self.file).xml2json()
        data.update({"fname": self.file})
        return data


if __name__ == "__main__":
    config = tomli.load(open("config.toml", "rb"))
    path = config["forerunner_xml"]["datapath"]

    if True:
        file = "20050725-190632.xml"
        session = Trainses_xml(file)

        file = "20041008-170457.xml"
        session = Trainses_xml(file)
        print(session)
