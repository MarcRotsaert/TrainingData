import abc

from lap_analyzer import RManualLapAnalyzer, RAutoLapAnalyzer
from sample_analyzer import SampleAnalyzerBasic, SamAnalExtra


class Trainsession(metaclass=abc.ABCMeta):
    def return_laps(self) -> list[dict]:
        return self.laps

    def return_autolaps(self) -> list[dict]:
        return self.alaps

    def return_sport(self) -> str:
        return self.abstract["sport"]


class Trainsession_file(Trainsession, metaclass=abc.ABCMeta):
    def __init__(self, file: str):
        self.path = self._return_path()
        self.file = file
        self.laps = []
        self.alaps = []
        self.samples = {}
        self.abstract = {}
        data = self._read_file()

        self.add_data(data)
        self.data = True

        self.RManualLapAnalyzer = RManualLapAnalyzer(self.laps)
        self.RAutoLapAnalyzer = RAutoLapAnalyzer(self.alaps)
        self.SamAnalExtra = SamAnalExtra(self.samples)

    @abc.abstractmethod
    def _read_file(self) -> dict:
        pass

    @abc.abstractmethod
    def add_data(self, data: dict) -> None:
        pass

    @abc.abstractmethod
    def _return_path(self):
        pass

    def return_samples(self):
        return self.samples


class Trainsession_mongo(Trainsession):
    def __init__(self, mongorecord):
        try:
            self.laps = mongorecord.pop("laps")
        except AttributeError:
            self.laps = []
        try:
            self.alaps = mongorecord.pop("alaps")
        except AttributeError:
            self.alaps = []

        self.abstract = mongorecord
        self.RManualLapAnalyzer = RManualLapAnalyzer(self.laps)
        self.RAutoLapAnalyzer = RAutoLapAnalyzer(self.alaps)
