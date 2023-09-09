import os
import tomli
import pprint
import fitdecode
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

    def _fit_parser(self):
        alaps_raw = self._extract_alaps()
        laps_raw = self._extract_laps()
        samples_raw = self._extract_samples()        
        session_raw = self._extract_session()        
        return session_raw, alaps_raw, laps_raw, samples_raw

    def _extract_samples(self): 

        samples = []
        with fitdecode.FitReader(os.path.join(self.path, self.filename)) as fitreader:
            for frame in fitreader:
                if frame.frame_type == fitdecode.FIT_FRAME_DATA:
                    if frame.name=='record':
                        samples.append(frame)
        return samples

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

    def _find_onefield(self,frame, fieldname): 
        for i,field in enumerate(frame.fields): 
            if field.name == fieldname:
                return field

    def _extract_alaps(self):
        alaps = []
        with fitdecode.FitReader(os.path.join(self.path, self.filename)) as fitreader:
            for frame in fitreader:
                if frame.frame_type == fitdecode.FIT_FRAME_DATA:
                    if frame.name == "lap":
                        field_lap_trigger = self._find_onefield(frame,'lap_trigger')
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
                             if field_lap_trigger.name in ["manual", "session_end"]:
                                laps.append(frame)
                        except:
                            pass
        return laps
        # lap_trigger="manual"
        # lap_trigger="time???"
        # lap_trigger = "session_end"

"""
class Lapparser():
    if frame.name=="lap":
        xx


class Sampleparser():
    name = "record"
    timestamp
    config[parameters]



class Sessionparser:
    name = "session"

    def _return_sport(self):
        session.sport.value

"""


if __name__=='__main__':

    Garminfit_parser('marcrotsaert_712321869.fit')._fit_parser()