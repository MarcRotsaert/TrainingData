import os
import tomli
import xml.etree.ElementTree as ET


class Forerunner_parser:
    def __init__(self, filename: str):
        config = tomli.load(open("config.toml", "rb"))
        self.path = config["forerunner_xml"]["datapath"]
        self.Namespace = "{http://www.garmin.com/xmlschemas/ForerunnerLogbook}"
        self.filename = filename

    def _xml_parser(self) -> tuple[ET.Element, ET.Element, ET.Element]:
        xml = ET.parse(os.path.join(self.path, self.filename))
        session = xml.find(f"{self.Namespace}Run")
        laps = session.findall(f"{self.Namespace}Lap")
        track = session.findall(f"{self.Namespace}Track")
        return session, laps, track


class Lapparser(Forerunner_parser):
    def __init__(self, filename: str):
        super().__init__(filename)
        _, self.laps, _ = self._xml_parser()

    def _return_starttime(self, lap: ET.Element) -> str:
        return lap.find(f"{self.Namespace}StartTime").text

    def _return_latitude(self, lap: ET.Element) -> float:
        temp = lap.find(f"{self.Namespace}BeginPosition")
        try:
            lat = float(temp.find(f"{self.Namespace}Latitude").text)
        except AttributeError:
            return None
        return lat

    def _return_longitude(self, lap: ET.Element) -> float:
        temp = lap.find(f"{self.Namespace}BeginPosition")
        try:
            lon = float(temp.find(f"{self.Namespace}Longitude").text)
        except AttributeError:
            return None
        return lon

    def _return_distance(self, lap: ET.Element) -> float:
        length = lap.find(f"{self.Namespace}Length").text
        return float(length)

    def _return_duration(self, lap: ET.Element) -> str:
        temp = lap.find(f"{self.Namespace}Duration").text
        durfloat = self._timestr2float(temp)
        return durfloat

    def _return_speed(self, lap: ET.Element) -> float:
        duration = self._return_duration(lap)
        # s_duration = float(duration[2:-1])
        distance = self._return_distance(lap)
        speed = 3600 * (distance / duration) / 1000
        return round(speed, 1)

    @staticmethod
    def _timestr2float(val: str) -> float:
        return float(val.strip("PT").strip("S"))

    def xml2laps(self) -> list:
        if len(self.laps) > 1:
            json = self._xml2laps_multiplelap()
        else:
            json = self._xml2laps_onelap()
        return json

    def _xml2laps_onelap(self) -> list:
        result = [
            {
                "startTime": self._return_starttime(self.laps[0]),
                "latitude": self._return_latitude(self.laps[0]),
                "longitude": self._return_longitude(self.laps[0]),
                "duration": self._return_duration(self.laps[0]),
                "speed": {"avg": self._return_speed(self.laps[0])},
                "distance": self._return_distance(self.laps[0]),
            }
        ]
        return result

    def _xml2laps_multiplelap(self) -> list:
        laps = [
            {
                "startTime": self._return_starttime(self.laps[0]),
                "latitude": self._return_latitude(self.laps[0]),
                "longitude": self._return_longitude(self.laps[0]),
            }
        ]
        for i, lap in enumerate(self.laps):
            duration = self._return_duration(lap)
            distance = self._return_distance(lap)
            speed = self._return_speed(lap)
            laps.append(
                {
                    "lapNumber": i,
                    "duration": duration,
                    "speed": {"avg": speed},
                    "distance": distance,
                }
            )
        return laps


class Sampleparser(Forerunner_parser):
    def __init__(self, filename: str):
        super().__init__(filename)
        _, _, track = self._xml_parser()
        self.samples = track[0].findall(f"{self.Namespace}Trackpoint")

    def xml2samples(self) -> list[dict]:
        recordedRoute = []
        for sample in self.samples:
            # dateTime
            alt = self._return_altitude(sample)
            lat, lon = self._return_latlon(sample)
            time = self._return_time(sample)
            recordedRoute.append(
                {"latitude": lat, "longitude": lon, "altitude": alt, "dateTime": time}
            )
        return recordedRoute

    def _return_altitude(self, sample: ET.Element):
        sample2 = sample.find(f"{self.Namespace}Position")
        return sample2.find(f"{self.Namespace}Altitude").text

    def _return_latlon(self, sample: ET.Element):
        sample2 = sample.find(f"{self.Namespace}Position")
        lat = sample2.find(f"{self.Namespace}Latitude").text
        lon = sample2.find(f"{self.Namespace}Longitude").text
        return lat, lon

    def _return_time(self, sample: ET.Element):
        return sample.find(f"{self.Namespace}Time").text


class Parser(Forerunner_parser):
    def __init__(self, filename: str):
        super().__init__(filename)
        _, self.laps, self.samples = self._xml_parser()

    def xml2json(self):
        laps = Lapparser(self.filename).xml2laps()
        recordedroute = Sampleparser(self.filename).xml2samples()

        abstract = laps.pop(0)
        exercise = {"samples": {"recordedRoute": recordedroute}}

        if len(laps) > 1:
            distance = sum(la["distance"] for la in laps)
            duration = sum(la["duration"] for la in laps)
            abstract["duration"] = duration
            abstract["distance"] = distance
            abstract.update({"speed": {"avg": 3600 * distance / (duration * 1000)}})
            exercise.update({"laps": laps})

        json = abstract
        json.update({"exercises": [exercise]})
        return json
