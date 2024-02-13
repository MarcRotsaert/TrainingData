import os
import tomli
import numpy as np
import fitdecode
from fitdecode.records import FitDataMessage
from typing import Union

# The yielded frame object is of one of the following types:
# * fitdecode.FitHeader (FIT_FRAME_HEADER)
# * fitdecode.FitDefinitionMessage (FIT_FRAME_DEFINITION)
# * fitdecode.FitDataMessage (FIT_FRAME_DATA)
# * fitdecode.FitCRC (FIT_FRAME_CRC)


class Garminfit_parser:
    def __init__(self, filename: str):
        config = tomli.load(open("config.toml", "rb"))
        self.path = config["garmin_fit"]["datapath"]
        self.filename = filename
        self.config = config

    @staticmethod
    def _fit_parser_alllaps(alllaps: list) -> (list, list):
        triggers, frames = zip(*alllaps)
        if triggers.count("manual") < 3:
            laps = []
            alaps = frames
        else:
            alaps = []
            laps = frames

        return laps, alaps

    def _fit_parser(self) -> [list, list, list, list]:
        extractor = self._data_extractor()
        samples = []
        session = []
        # alaps = []
        all_laps = []
        for kind, frame in extractor:
            if kind == "sample":
                samples.append(frame)
            elif kind == "lap":
                field_lap_trigger = self._find_onefield(frame, "lap_trigger")
                if field_lap_trigger.value in ["manual"]:
                    all_laps.append(["manual", frame])
                    # laps.append(frame)
                elif field_lap_trigger.value in [
                    "distance",
                    "time",
                    "session_end",
                ]:
                    all_laps.append(["automatic", frame])
                else:
                    print(field_lap_trigger.value)
                    xx
            elif kind == "session":
                session.append(frame)
        if len(all_laps) > 0:
            laps, alaps = self._fit_parser_alllaps(all_laps)
        else:
            laps, alaps = [[], []]
        return session, laps, alaps, samples

    def _data_extractor(self) -> [str, fitdecode.FIT_FRAME_DATA]:
        with fitdecode.FitReader(os.path.join(self.path, self.filename)) as fitreader:
            for frame in fitreader:
                if frame.frame_type == fitdecode.FIT_FRAME_DATA:
                    if frame.name == "record":  # samples
                        yield "sample", frame
                    elif frame.name == "session" or frame.name == "activity":  # session
                        yield "session", frame
                    elif frame.name == "lap":  # lap
                        yield "lap", frame

    def _extract_fitheader(self) -> fitdecode.FIT_FRAME_HEADER:
        with fitdecode.FitReader(os.path.join(self.path, self.filename)) as fitreader:
            for frame in fitreader:
                if frame.frame_type == fitdecode.FIT_FRAME_HEADER:
                    return frame

    def _extract_fitdefinitionmessage(self) -> list[fitdecode.FIT_FRAME_DEFINITION]:
        framedef = []
        with fitdecode.FitReader(os.path.join(self.path, self.filename)) as fitreader:
            for frame in fitreader:
                if frame.frame_type == fitdecode.FIT_FRAME_DEFINITION:
                    framedef.append(frame)
        return framedef

    def _extract_samples(self) -> list:
        _, _, _, samples = self._data_extractor()
        return samples

    def _extract_session(self) -> list:
        session, _, _, _ = self._data_extractor()
        return session

    def _extract_alaps(self) -> list:
        _, alaps, _, _ = self._data_extractor()
        return alaps

    def _extract_laps(self) -> list:
        _, _, laps, _ = self._data_extractor()
        return laps

    def _find_onefield(self, frame, fieldname):
        for i, field in enumerate(frame.fields):
            if field.name == fieldname:
                return field

    def _values_from_frame(
        self, frame: FitDataMessage, fieldnames: Union[list, str]
    ) -> list:
        if isinstance(fieldnames, str):
            fieldnames = [fieldnames]

        values = []
        for fi in fieldnames:
            field = self._find_onefield(frame, fi)
            if hasattr(field, "value"):
                if field.value == None:
                    field.value = None
                values.append(field.value)
            else:
                values.append(None)
        return values

    def _get_fitframedata_fieldnames(self):
        fieldnames = set()
        with fitdecode.FitReader(os.path.join(self.path, self.filename)) as fitreader:
            for frame in fitreader:
                if frame.frame_type == fitdecode.FIT_FRAME_DATA:
                    fieldnames.add(frame.name)
        return fieldnames

    def _semicircles2deg(self, value_in):
        degree = value_in * (180 / 2**31)
        return degree

    def _get_dataframes(self) -> list:
        with fitdecode.FitReader(os.path.join(self.path, self.filename)) as fitreader:
            dframe = []
            for frame in fitreader:
                if frame.frame_type == fitdecode.FIT_FRAME_DATA:
                    dframe.append(frame)
            return dframe

    def extract_abstract(self) -> dict:
        framename = "session"
        paramnames = [
            "speed",
            "sport",
            "startTime",
            "duration",
            "distance",
            "descent",
            "ascent",
            "maximumHeartRate",
            "averageHeartRate",
        ]

        session, _, _, _ = self._fit_parser()
        if len(session) > 0:
            frame = session[0]

            abstract = {}
            paramconv = self.config["garmin_fit"]["paramnameconversion"]
            for pn in paramnames:
                if pn == "speed":
                    avgvalue = frame.get_value("avg_speed")
                    maxvalue = frame.get_value("max_speed")
                    if avgvalue:
                        avgvalue = avgvalue * 3600 / 1000
                    else:
                        avgvalue = None
                    if maxvalue:
                        maxvalue = avgvalue * 3600 / 1000
                    else:
                        maxvalue = None
                    abstract.update(
                        {
                            "speed": {"avg": avgvalue, "max": maxvalue},
                        }
                    )
                else:
                    value = frame.get_value(paramconv[pn])
                    if pn == "sport":
                        value = value.upper()
                    elif pn == "startTime":
                        value = str(value)

                    abstract.update({pn: value})
            return abstract
        # framename = 'device'
        # fnames = ['serial_number']


class Lapparser(Garminfit_parser):
    def __init__(self, filename: str):
        super().__init__(filename)
        _, self.laps, self.alaps, _ = self._fit_parser()

    def _return_starttime(self, lap: FitDataMessage) -> str:
        par_name = "start_time"
        return self._values_from_frame(lap, par_name)[0]

    def _return_latitude(self, lap: FitDataMessage) -> float:
        par_name = "start_position_lat"
        value_semicirc = self._values_from_frame(lap, par_name)[0]
        if value_semicirc is not None:
            degree = self._semicircles2deg(value_semicirc)
        else:
            degree = None
        return degree

    def _return_longitude(self, lap: FitDataMessage) -> float:
        par_name = "start_position_lon"
        value_semicirc = self._values_from_frame(lap, par_name)[0]
        degree = self._semicircles2deg(value_semicirc)
        return degree

    def _return_distance(self, lap: FitDataMessage) -> float:
        par_name = "total_distance"
        return self._values_from_frame(lap, par_name)[0]

    def _return_duration(self, lap: FitDataMessage) -> str:
        par_name = "total_timer_time"
        return self._values_from_frame(lap, par_name)[0]

    def _return_speed(self, lap: FitDataMessage) -> np.array:
        par_names = [
            "enhanced_avg_speed",
            "avg_speed",
            "enhanced_max_speed",
            "max_speed",
        ]
        speed_list = self._values_from_frame(lap, par_names)
        # try:
        speed_arr = np.array(speed_list)
        speed_arr[speed_arr == np.nan] = 0
        # speed_arr[speed_arr is None] = 0
        speed_arr[speed_arr == None] = 0
        try:
            speed_kmu = speed_arr * 3600 / 1000  # m/s -> km/u
        except TypeError:
            print(speed_arr)
            xx
        # speed_kmu[speed_kmu == 0] = None
        # except TypeError:
        # speed_kmu = len(speed_list) * [None]
        return speed_kmu

    def _return_heartrate(self, lap: FitDataMessage) -> list[float]:
        par_names = ["avg_heart_rate", "max_heart_rate"]
        return self._values_from_frame(lap, par_names)

    def _return_cadence(self, lap: FitDataMessage) -> list[float]:
        par_names = ["avg_running_cadence", "max_running_cadence"]
        return self._values_from_frame(lap, par_names)

    def fit2laps(self, laps_alaps) -> dict or list:
        json = self._fit2laps_multiplelap(laps_alaps)
        return json

    def _fit2laps_multiplelap(self, laps_alaps: str) -> list:
        if laps_alaps == "alaps":
            laps_in = self.alaps
        elif laps_alaps == "laps":
            laps_in = self.laps

        laps_out = []
        for i, lap in enumerate(laps_in):
            duration = self._return_duration(lap)
            distance = self._return_distance(lap)
            speed = self._return_speed(lap)
            heartrate = self._return_heartrate(lap)
            cadence = self._return_cadence(lap)
            laps_out.append(
                {
                    "lapNumber": i,
                    "duration": duration,
                    "speed": {"avg": speed[0], "max": speed[2]},
                    "heartRate": {"avg": heartrate[0], "max": heartrate[1]},
                    "cadence": {"avg": cadence[0], "max": cadence[1]},
                    "distance": distance,
                }
            )
        return laps_out


class Sampleparser(Garminfit_parser):
    def __init__(self, filename: str):
        super().__init__(filename)
        _, _, _, self.samples = self._fit_parser()

    def fit2samples(self) -> list[dict]:
        speed_arr = []
        heartrate_arr = []
        recordedRoute = []
        distance_arr = []
        for sample in self.samples:
            # dateTime
            hr = self._return_heartrate(sample)
            alt = self._return_altitude(sample)
            lat, lon = self._return_latlon(sample)
            time = self._return_time(sample)
            speed = self._return_speed(sample)
            distance = self._return_distance(sample)

            speed_arr.append({"dateTime": time, "value": speed[0]})
            heartrate_arr.append({"dateTime": time, "value": hr[0]})
            distance_arr.append({"dateTime": time, "value": distance[0]})

            recordedRoute.append(
                {
                    "latitude": lat,
                    "longitude": lon,
                    "altitude": alt[0],
                    "dateTime": time,
                }
            )
            # samples = {'speed': speed_arr, 'heartRate': heartrate_arr, 'recordedRoute':recordedRoute}
        samples = {
            "distance": distance_arr,
            "speed": speed_arr,
            "heartRate": heartrate_arr,
            "recordedRoute": recordedRoute,
        }
        return samples  # , recordedRoute

    def _return_heartrate(self, lap: FitDataMessage) -> list[float]:
        par_names = "heart_rate"
        return self._values_from_frame(lap, par_names)

    def _return_altitude(self, sample: FitDataMessage) -> list:
        par_names = ["enhanced_altitude", "altitude"]
        altitude_list = self._values_from_frame(sample, par_names)
        return altitude_list

    def _return_latlon(self, sample: FitDataMessage) -> [float, float]:
        par_names = ["position_lat", "position_long"]
        latlon_list = self._values_from_frame(sample, par_names)
        if latlon_list[0] is not None:
            lat_deg = self._semicircles2deg(latlon_list[0])
            lon_deg = self._semicircles2deg(latlon_list[1])
        else:
            lat_deg = lon_deg = None
        return lat_deg, lon_deg

    def _return_time(self, sample: FitDataMessage) -> str:
        par_names = "timestamp"
        timestamp = self._values_from_frame(sample, par_names)[0]
        isotime = timestamp.isoformat()
        return isotime

    def _return_speed(self, sample: FitDataMessage):
        par_names = ["enhanced_speed", "speed"]
        speed_list = self._values_from_frame(sample, par_names)
        if speed_list[0] is not None and speed_list[1]:
            speed_kmu = np.array(speed_list) * 3600 / 1000  # m/s -> km/u
        else:
            speed_kmu = np.array([None, None])

        return speed_kmu

    def _return_distance(self, sample: FitDataMessage):
        par_names = ["distance"]
        distance_list = self._values_from_frame(sample, par_names)
        return distance_list


class Parser(Garminfit_parser):
    def __init__(self, filename: str):
        super().__init__(filename)
        self.session, self.laps, self.alaps, self.samples = self._fit_parser()

    def fit2json(self):
        json = self.extract_abstract()

        laps = Lapparser(self.filename).fit2laps("laps")
        alaps = Lapparser(self.filename).fit2laps("alaps")
        samples = Sampleparser(self.filename).fit2samples()

        json.update(
            {
                "exercises": [
                    {
                        "alaps": alaps,
                        "laps": laps,
                        "samples": {
                            "recordedRoute": samples["recordedRoute"],
                            "speed": samples["speed"],
                            "heartRate": samples["heartRate"],
                            "distance": samples["distance"],
                        },
                    }
                ]
            }
        )

        return json
