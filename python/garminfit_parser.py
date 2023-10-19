import os, glob
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

    def _fit_parser(self) -> [FitDataMessage, ]:
        alaps_raw = self._extract_alaps()
        laps_raw = self._extract_laps()
        samples_raw = self._extract_samples()
        session_raw = self._extract_session()
        return session_raw, alaps_raw, laps_raw, samples_raw

    def _extract_fitheader(self):
        with fitdecode.FitReader(os.path.join(self.path, self.filename)) as fitreader:
            for frame in fitreader:
                if frame.frame_type == fitdecode.FIT_FRAME_HEADER:
                    return frame

    def _extract_fitdefinitionmessage(self):
        framedef = []
        with fitdecode.FitReader(os.path.join(self.path, self.filename)) as fitreader:
            for frame in fitreader:
                if frame.frame_type == fitdecode.FIT_FRAME_DEFINITION:
                    framedef.append(frame)
        return framedef

    def _extract_samples(self):
        samples = []
        with fitdecode.FitReader(os.path.join(self.path, self.filename)) as fitreader:
            for frame in fitreader:
                if frame.frame_type == fitdecode.FIT_FRAME_DATA:
                    # Here, frame is a FitDataMessage object.
                    # A FitDataMessage object contains decoded values that
                    # are directly usable in your script logic.
                    if frame.name == "record":
                        samples.append(frame)
        return samples

    def _extract_session(self):
        session = []
        with fitdecode.FitReader(os.path.join(self.path, self.filename)) as fitreader:
            for frame in fitreader:
                if frame.frame_type == fitdecode.FIT_FRAME_DATA:
                    # Here, frame is a FitDataMessage object.
                    # A FitDataMessage object contains decoded values that
                    # are directly usable in your script logic.
                    if frame.name == "session" or frame.name == "activity":
                        session.append(frame)
                        # print(frame.name)
        return session

    def _extract_alaps(self):
        alaps = []
        with fitdecode.FitReader(os.path.join(self.path, self.filename)) as fitreader:
            for frame in fitreader:
                if frame.frame_type == fitdecode.FIT_FRAME_DATA:
                    if frame.name == "lap":
                        field_lap_trigger = self._find_onefield(frame, 'lap_trigger')
                        # print(field_lap_trigger.value)
                        if field_lap_trigger.value in ["distance", "time", "session_end"]:
                            alaps.append(frame)
        return alaps

    def _extract_laps(self):
        laps = []
        with fitdecode.FitReader(os.path.join(self.path, self.filename)) as fitreader:
            for frame in fitreader:
                if frame.frame_type == fitdecode.FIT_FRAME_DATA:
                    if frame.name == "lap":
                        field_lap_trigger = self._find_onefield(frame, 'lap_trigger')
                        if field_lap_trigger.value in ["manual"]:
                            laps.append(frame)
        return laps

    def _find_onefield(self, frame, fieldname):
        for i, field in enumerate(frame.fields):
            if field.name == fieldname:
                return field

    def _values_from_frame(self, frame: FitDataMessage, fieldnames: Union[list, str]) -> list:
        if isinstance(fieldnames, str):
            fieldnames = [fieldnames]

        values = []
        for fi in fieldnames:
            field = self._find_onefield(frame, fi)
            if hasattr(field, 'value'):
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

    def _get_dataframes(self):
         
         with fitdecode.FitReader(os.path.join(self.path, self.filename)) as fitreader:
            dframe =[]
            for frame in fitreader:
                if frame.frame_type == fitdecode.FIT_FRAME_DATA:
                    dframe.append(frame)
            return dframe


    def _extract_abstract_exercises(self):
        framename = 'session'
        fnames = ['start_time', 'total_elapsed_time', 'total_distance', 'sport', 
                  'avg_cadence', 'max_cadence',
                  'total_descent', 'total_ascent'
                  # 'total_calories'
        ]

    def extract_abstract(self):
        framename = 'session'
        paramnames = ["startTime", "duration", "distance", "descent", "ascent", "maximumHeartRate", "averageHeartRate"]
        dframe = self._get_dataframes()
        i = 0
        while dframe[i].name != 'session':
            i += 1
            if i == len(dframe):
                return None
        
        abstract ={}
        
        paramconv = self.config['garmin_fit']['paramnameconversion']
        frame = dframe[i]
        for pn in paramnames:
            abstract.update({pn: frame.get_value(paramconv[pn])})
        return abstract
        # framename = 'device'
        # fnames = ['serial_number'] 


class Lapparser(Garminfit_parser):
    def __init__(self, filename: str):
        super().__init__(filename)
        _, self.alaps, self.laps, _ = self._fit_parser()

    def _return_starttime(self, lap: FitDataMessage) -> str:
        par_name = 'start_time'
        return self._values_from_frame(lap, par_name)[0]

    def _return_latitude(self, lap: FitDataMessage) -> float:
        par_name = 'start_position_lat'
        value_semicirc = self._values_from_frame(lap, par_name)[0]
        if value_semicirc is not None:
            degree = self._semicircles2deg(value_semicirc)
        else:
            degree = None
        return degree

    def _return_longitude(self, lap: FitDataMessage) -> float:
        par_name = 'start_position_lon'
        value_semicirc = self._values_from_frame(lap, par_name)[0]
        degree = self._semicircles2deg(value_semicirc)
        return degree

    def _return_distance(self, lap: FitDataMessage) -> float:
        par_name = 'total_distance'
        return self._values_from_frame(lap, par_name)[0]

    def _return_duration(self, lap: FitDataMessage) -> str:
        par_name = 'total_timer_time'
        return self._values_from_frame(lap, par_name)[0]

    def _return_speed(self, lap: FitDataMessage) -> list[float]:
        par_names = ['enhanced_avg_speed', 'avg_speed',
                     'enhanced_max_speed', 'max_speed']
        speed_list = self._values_from_frame(lap, par_names)
        speed_kmu = np.array(speed_list)*3600/1000  # m/s -> km/u
        return speed_kmu

    def _return_heartrate(self, lap: FitDataMessage) -> list[float]:
        par_names = ['avg_heart_rate', 'max_heart_rate']
        return self._values_from_frame(lap, par_names)

    def _return_cadence(self, lap: FitDataMessage) -> list[float]:
        par_names = ['avg_running_cadence', 'max_running_cadence']
        return self._values_from_frame(lap, par_names)

    def fit2laps(self, laps_alaps) -> dict or list:
        json = self._fit2laps_multiplelap(laps_alaps)
        return json

    def _fit2laps_multiplelap(self, laps_alaps: str) -> list:
        if laps_alaps == 'alaps':
            laps_in = self.alaps
        elif laps_alaps == 'laps':
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
        speed_arr= []
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
            
            speed_arr.append({'dateTime': time,'value': speed[0]}) 
            heartrate_arr.append({'dateTime': time,'value': hr[0]}) 
            distance_arr.append({'dateTime': time,'value': distance[0]}) 
            
            recordedRoute.append(
                {"latitude": lat, "longitude": lon,
                 "altitude": alt[0],
                 "dateTime": time,
                 }
            )
            # samples = {'speed': speed_arr, 'heartRate': heartrate_arr, 'recordedRoute':recordedRoute}
        samples = {'distance':distance_arr, 'speed': speed_arr, 'heartRate': heartrate_arr, 'recordedRoute':recordedRoute}
        return samples #, recordedRoute

    def _return_heartrate(self, lap: FitDataMessage) -> list[float]:
        par_names = 'heart_rate'
        return self._values_from_frame(lap, par_names)

    def _return_altitude(self, sample: FitDataMessage) -> list:
        par_names = ['enhanced_altitude', 'altitude']
        altitude_list = self._values_from_frame(sample, par_names)
        return altitude_list

    def _return_latlon(self, sample: FitDataMessage) -> [float, float]:
        par_names = ['position_lat', 'position_long']
        latlon_list = self._values_from_frame(sample, par_names)
        if latlon_list[0] is not None:
            lat_deg = self._semicircles2deg(latlon_list[0])
            lon_deg = self._semicircles2deg(latlon_list[1])
        else:
            lat_deg = lon_deg = None
        return lat_deg, lon_deg

    def _return_time(self, sample: FitDataMessage) -> str:
        par_names = 'timestamp'
        timestamp = self._values_from_frame(sample, par_names)[0]
        isotime = timestamp.isoformat()
        return isotime

    def _return_speed(self, sample: FitDataMessage):
        par_names = ['enhanced_speed', 'speed']
        speed_list = self._values_from_frame(sample, par_names)
        if speed_list[0] is not None and speed_list[1]:
            speed_kmu = np.array(speed_list)*3600/1000  # m/s -> km/u
        else:
            speed_kmu = np.array([None, None])

        return speed_kmu

    def _return_distance(self, sample: FitDataMessage):
        par_names = ['distance']
        distance_list = self._values_from_frame(sample, par_names)
        return distance_list


class Parser(Garminfit_parser):
    def __init__(self, filename: str):
       super().__init__(filename)
       self.session, self.alaps, self.laps, self.samples = self._fit_parser()

    def fit2json(self):
        laps = Lapparser(self.filename).fit2laps('laps')
        alaps = Lapparser(self.filename).fit2laps('alaps')
        samples = Sampleparser(self.filename).fit2samples()
        # if isinstance(laps, list):
        json = {
            "exercises": [
                {"alaps": alaps, "laps": laps, 
                 "samples": {"recordedRoute": samples['recordedRoute'],
                             "speed": samples['speed'],
                             "heartRate": samples['heartRate'],
                             "distance": samples['distance'],
                             },
        }] }
        #    json = laps
        #    json.update({"exercises": [{"samples": {"recordedRoute": recordedroute}}]})

        return json


if __name__ == '__main__':
    path = r'C:\Users\marcr\OneDrive\Documenten\logboek_looptracks\looptracks_garmin'
    for file in glob.glob(os.path.join(path, '*.fit')):
        x = Garminfit_parser(file.split('\\')[-1])
        abst = x.extract_abstract()
        
        print(abst)

    x = Garminfit_parser('marcrotsaert_220466005.fit')
    dframe = x._get_dataframes()



    for frame in dframe:
        if frame.name == 'session':
            print(frame)
            #if x._find_onefield(frame,'lap') is not None:

    g = Sampleparser('marcrotsaert_220466005.fit')
    print(g._return_latlon(g.samples[100]))
    print(g._return_altitude(g.samples[100]))
    print(g._return_speed(g.samples[100]))
    print(g._return_heartrate(g.samples[100]))
    print(g.fit2samples())
    g = Sampleparser('marcrotsaert_711735968.fit')
    print(g.fit2samples())

    x = Lapparser('marcrotsaert_711735968.fit')
    alaps = x.fit2laps('alaps')
    laps = x.fit2laps('laps')

    for lap in laps:
        y = Lapparser('marcrotsaert_712321869.fit')._return_heartrate(lap)
        print(y)
        y = Lapparser('marcrotsaert_712321869.fit')._return_cadence(lap)
        print(y)
