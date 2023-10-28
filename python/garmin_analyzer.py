import tomli

from  trainsession import Trainsession_file
import garminfit_parser as gparser

class Trainses_fit(Trainsession_file):
    def __init__(self, file: str):
        super().__init__(file)
        # self.path = path
        # self.file = file
        # self.laps = []
        # self.alaps = []
        # self.abstract = {}
        # data = self._read_fit()

        # self.add_data(data)
        # self.data = True
    def _return_path(self):
        config = tomli.load(open("config.toml", "rb"))
        return config["garmin_fit"]["datapath"]    

    def _read_file(self) -> None:
        data = gparser.Parser(self.file).fit2json()
        data.update({"fname": self.file})
        return data

    def add_data(self, data: dict):
        def _set_data_nonexercise(data):
            self.laps = data.pop("laps")
            self.alaps = data.pop("alaps")
            return data

        def _set_data_exercise(data):
            config = tomli.load(open("config.toml", "rb"))
            for dtype in config["garmin_fit"]["datatypes"]:
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

if __name__ == "__main__":
    config = tomli.load(open("config.toml", "rb"))
    # path = config["garmin_fit"]["datapath"]

    if True:
        file = "marcrotsaert_175152248.fit"
        session = Trainses_fit(file)

        file = "marcrotsaert_220466005.fit"
        session = Trainses_fit(file)
