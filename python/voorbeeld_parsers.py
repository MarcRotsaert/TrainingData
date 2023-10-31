import os
import pprint
import glob
import tomli
import parsing.forerunner_parser as for_pas
import parsing.garminfit_parser as gar_pas
import parsing.polar_parser as pol_pas

config = tomli.load(open("config.toml", "rb"))

def forerunner_parser():
    z = for_pas.Parser("20041008-170457.xml").xml2json()
    z = for_pas.Parser("20050725-190632.xml").xml2json()
    x = for_pas.Lapparser("20050725-190632.xml").xml2laps()

    x = for_pas.Lapparser("20041008-170457.xml").xml2laps()
    x = for_pas.Lapparser("20050725-190632.xml").xml2laps()
    y = for_pas.Sampleparser("20050725-190632.xml").xml2samples()
    pprint.pprint(y)

def garminfit_parser():
    path = config["garmin_fit"]["datapath"]
    for file in glob.glob(os.path.join(path, '*.fit'))[0:3]:
        x = gar_pas.Garminfit_parser(file.split('\\')[-1])
        abst = x.extract_abstract()
        print(abst)

    x = gar_pas.Garminfit_parser('marcrotsaert_220466005.fit')
    dframe = x._get_dataframes()

    for frame in dframe:
        if frame.name == 'session':
            print(frame)
            #if x._find_onefield(frame,'lap') is not None:

    g = gar_pas.Sampleparser('marcrotsaert_220466005.fit')
    print(g._return_latlon(g.samples[100]))
    print(g._return_altitude(g.samples[100]))
    print(g._return_speed(g.samples[100]))
    print(g._return_heartrate(g.samples[100]))
    print(g.fit2samples())
    g = gar_pas.Sampleparser('marcrotsaert_711735968.fit')
    print(g.fit2samples())

    x = gar_pas.Lapparser('marcrotsaert_711735968.fit')
    alaps = x.fit2laps('alaps')
    laps = x.fit2laps('laps')

def polar_parser():
    filename = "training-session-2014-01-03-263915750-ce8ea79c-8a35-43ed-8bc4-65733b407692.json"
    popa = pol_pas.Parser(filename).json2json()
    print(popa["exercises"][0])


if __name__ == '__main__':
    forerunner_parser()
    polar_parser()
    garminfit_parser()
