import os
import tomli
import pprint
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
                    if frame.name=="record":
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
                        print(frame.name)
        return session

    def _extract_alaps(self):
        alaps = []
        with fitdecode.FitReader(os.path.join(self.path, self.filename)) as fitreader:
            for frame in fitreader:
                if frame.frame_type == fitdecode.FIT_FRAME_DATA:
                    if frame.name == "lap":
                        field_lap_trigger = self._find_onefield(frame,'lap_trigger')
                        print(field_lap_trigger.value)
                        try: 
                            if field_lap_trigger.value == "distance":
                                alaps.append(frame)
                        except:
                            pass
        return alaps

    def _extract_laps(self):
        laps = [] 
        with fitdecode.FitReader(os.path.join(self.path, self.filename)) as fitreader:
            for frame in fitreader:
                if frame.frame_type == fitdecode.FIT_FRAME_DATA:
                    if frame.name == "lap":
                        field_lap_trigger = self._find_onefield(frame,'lap_trigger')
                        try: 
                             if field_lap_trigger.value in ["manual", "session_end", "time"]:
                                laps.append(frame)
                        except:
                            pass
        return laps

    def _find_onefield(self,frame, fieldname):
        for i,field in enumerate(frame.fields):
            if field.name == fieldname:
                return field

    def _values_from_frame(self, frame: FitDataMessage, fieldnames: Union[list, str]) -> list:
        if isinstance(fieldnames, str):
            fieldnames = [fieldnames]
        values = []
        for fi in fieldnames:
            field = self._find_onefield(frame, fi)
            values.append(field.value)
        return values

    def _get_fitframedata_fieldnames(self):
        fieldnames = set()
        with fitdecode.FitReader(os.path.join(self.path, self.filename)) as fitreader:
            for frame in fitreader:
                if frame.frame_type == fitdecode.FIT_FRAME_DATA:
                    fieldnames.add(frame.name)
                    #print(frame.fields)
        return(fieldnames)


    def _semicircles2deg(self, value_in):
        degree = value_in * ( 180 / 2**31 )
        return degree
    
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
        degree = self._semicircles2deg(value_semicirc)
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
        par_names = ['enhanced_avg_speed', 'avg_speed', 'enhanced_max_speed', 'max_speed']
        speed_list =  self._values_from_frame(lap, par_names)
        speed_kmu = np.array(speed_list)*3600/1000 # 
        return speed_kmu

    def _return_heartrate(self, lap: FitDataMessage) -> list[float]:
        par_names = ['avg_heart_rate', 'max_heart_rate']
        return self._values_from_frame(lap, par_names)

    def _return_cadence(self, lap: FitDataMessage) -> list[float]:
        par_names = ['avg_running_cadence', 'max_running_cadence']
        # fieldnames = self._get_fitframedata_fieldnames(lap)
        return self._values_from_frame(lap, par_names)

    def fit2laps(self, laps_alaps) -> dict or list:
        json = self._fit2laps_multiplelap(laps_alaps)
        return json

    def _fit2laps_multiplelap(self, laps_alaps: str) -> list:
        if laps_alaps =='alaps':
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
                    "speed": {"avg": speed[0], "max":speed[2]},
                    "heartRate": {"avg": heartrate[0], "max": heartrate[1]},
                    "cadence": {"avg": cadence[0], "max": cadence[1]},
                    "distance": distance,
                }
            )
        return laps_out

# class Sessionparser:
#     name = "session"
#     def _return_sport(self):
#         session.sport.value

class Sampleparser(Garminfit_parser):
    def __init__(self, filename: str):
        super().__init__(filename)
        _, _ , _, self.samples = self._fit_parser()

    def fit2samples(self) ->list[dict]:
        recordedRoute = []
        for sample in self.samples:
            # dateTime
            alt = self._return_altitude(sample)
            lat, lon = self._return_latlon(sample)
            time = self._return_time(sample)
            speed = self._return_speed(sample)

            recordedRoute.append(
                {"latitude": lat, "longitude": lon, "altitude": alt, "dateTime": time, "speed": speed[0]}
            )
        return recordedRoute

    def _return_altitude(self, sample: FitDataMessage) -> list:
        par_names = ['enhanced_altitude', 'altitude' ]
        altitude_list =  self._values_from_frame(sample, par_names)
        altitude = altitude_list[0]
        return altitude_list

    def _return_latlon(self, sample: FitDataMessage) -> [float, float]:
        par_names = ['position_lat', 'position_long']
        latlon_list =  self._values_from_frame(sample, par_names)
        lat_deg = self._semicircles2deg(latlon_list[0])
        lon_deg = self._semicircles2deg(latlon_list[1])
        return lat_deg,lon_deg

    def _return_time(self, sample: FitDataMessage):
        par_names = 'timestamp'
        timestamp =  self._values_from_frame(sample, par_names)[0]
        isotime = timestamp.isoformat()
        return isotime

    def _return_speed(self, sample: FitDataMessage):
        par_names = ['enhanced_speed', 'speed']
        speed_list =  self._values_from_frame(sample, par_names)
        speed_kmu = np.array(speed_list)*3600/1000 # m/s -> km/u
        return speed_kmu


if __name__=='__main__':
    # f = Garminfit_parser('marcrotsaert_711735968.fit')
    # frames = f._extract_fitdefinitionmessage()
    g = Sampleparser('marcrotsaert_220466005.fit')
    g.fit2samples()
    print(g._return_latlon(g.samples[100]))
    g._return_altitude(g.samples[100])
    g._return_speed(g.samples[100])

    alaps_raw = f._extract_alaps()
    x = Lapparser('marcrotsaert_711735968.fit')
    alaps = x.fit2laps('alaps')
    laps = x.fit2laps('laps')
    _, alaps ,laps  ,_ = Garminfit_parser('marcrotsaert_711735968.fit')._fit_parser()
    
    for lap in laps:
        y = Lapparser('marcrotsaert_712321869.fit')._return_heartrate(lap)
        print(y)
        y = Lapparser('marcrotsaert_712321869.fit')._return_cadence(lap)
        print(y)
