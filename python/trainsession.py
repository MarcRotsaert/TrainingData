import abc

from lap_analyzer import RManualLapAnalyzer, RAutoLapAnalyzer
from sample_analyzer import SampleAnalyzerBasic, SamAnalExtra


class Trainsession_file(metaclass=abc.ABCMeta):
    def __init__(self, file: str):
        self.path = self._return_path()
        self.file = file
        self.laps = []
        self.alaps = []
        self.abstract = {}
        data = self._read_file()

        self.add_data(data)
        self.data = True

        self.RManualLapAnalyzer = RManualLapAnalyzer
        self.RAutoLapAnalyzer = RAutoLapAnalyzer
        self.SampleAnalyzerBasic = SampleAnalyzerBasic
        self.SamAnalExtra = SamAnalExtra

    @classmethod
    def _read_file(self) -> dict:
        pass

    @classmethod
    def add_data(self, data: dict) -> None:
        pass

    @classmethod
    def _return_path(self):
        pass


class Trainsession_mongo(metaclass=abc.ABCMeta):
    def __init__(self, mongorecord):
        try:
            self.laps = mongorecord.pop("laps")
        except AttributeError:
            self.laps = []
        try:
            self.alaps = mongorecord.pop("alaps")
        except AttributeError:
            self.alaps = []

        # self.file = mongorecord.pop('fname')
        self.abstract = mongorecord
        self.RManualLapAnalyzer = RManualLapAnalyzer
        self.RAutoLapAnalyzer = RAutoLapAnalyzer
        self.SampleAnalyzerBasic = SampleAnalyzerBasic
        self.SamAnalExtra = SamAnalExtra
