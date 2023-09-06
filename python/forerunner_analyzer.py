import os
import tomli 
import pprint
import xml.etree.ElementTree as ET

class Forerunner_parser:
    def __init__(self, filename):
        config = tomli.load(open('config.toml',"rb"))
        self.path = config['forerunner_xml']['datapath']
        self.Namespace = '{http://www.garmin.com/xmlschemas/ForerunnerLogbook}'
        self.filename = filename


    def _xml_parser(self):
        xml = ET.parse(os.path.join(self.path, self.filename))
        session = xml.find(f'{self.Namespace}Run')
        laps = session.findall(f'{self.Namespace}Lap')
        samples =session.findall(f'{self.Namespace}Track')
        return session, laps, samples


class Lapparser(Forerunner_parser):
    def __init__(self, filename):
        super().__init__(filename)
        _, self.laps, _= self._xml_parser() 

    def _return_distance(self, lap)-> str:
        length = lap.find(f'{self.Namespace}Length').text       
        return float(length) 

    def _return_duration(self, lap)-> str:
        return lap.find(f'{self.Namespace}Duration').text

    def _return_speed(self, lap) -> str: 
        duration = self._return_duration(lap)
        s_duration = float(duration[2:-1])
        distance = self._return_distance(lap)
        speed =  3600*(distance/s_duration)/1000
        return round(speed,1)


    def xml2json_laps(self):
        laps = []    
        for i, lap in enumerate(self.laps):
            duration = self._return_duration(lap)
            distance = self._return_distance(lap)
            speed = self._return_speed(lap)
            laps.append( {'lapNumber':i,
                      'duration':duration,
                      'speed':{'avg':speed},
                      'distance':distance
                      })
            print(len(laps))
        return laps
    

class Sampleparser(Forerunner_parser):
    def __init__(self, filename ):
        super(Forerunner_parser)
        _, _, self.samples = self._xml_parser() 
    def xml2json_samples(self):

# if __name_ == '__main__':
x = Lapparser('20050725-190632.xml').xml2json_laps()
pprint.pprint(x)
