import os
import glob
import random
import pprint
import tomli
from matplotlib import pyplot as pp

from analyzer.polar_analyzer import Trainses_json

from analyzer.garmin_analyzer import Trainses_fit
from analyzer.forerunner_analyzer import Trainses_xml

config = tomli.load(open("config.toml", "rb"))
path = config["polar_json"]["datapath"]


def ex_polar_lapanalyzer():
    file = "training-session-2015-01-25-263888810-887b73d8-5599-4534-833c-521322b8c28b.json"
    session = Trainses_json(file)
    res = session.RManualLapAnalyzer.determine_intervals()
    print(res)

    file = "training-session-2015-02-17-263886464-81c22d89-24ce-41b2-b130-98f85cec4dbe.json"
    session = Trainses_json(file)
    res = session.RManualLapAnalyzer.determine_intervals()
    print(res)


    file = "training-session-2015-03-11-263884640-0e71a9a2-88f6-4a50-a478-4401c7e9128c.json"
    session = Trainses_json(file)
    res = session.RManualLapAnalyzer.determine_intervals()
    print(res)

    files = glob.glob(os.path.join(path, "training-session-2015-*.json"))
    k = 0
    while k < 10:
        file = random.choice(files)
        session = Trainses_json(file)
        if session.return_laps() is not None:
            if session.RManualLapAnalyzer.identify_interval() in [
                "interval",
                "interval, check1",
                "interval, check2",
            ]:
                print(session.abstract["fname"])
                res = session.RManualLapAnalyzer.determine_intervals()
                print(res)
                k += 1
    #
    # training-session-2015-01-25-263888810-887b73d8-5599-4534-833c-521322b8c28b.json
    # training-session-2015-03-11-263884640-0e71a9a2-88f6-4a50-a478-4401c7e9128c.json

    file = "training-session-2015-01-07-263888486-2d791dc2-1ee2-4964-bb44-558579c19c6f.json"
    session = Trainses_json(file)
    res = session.RManualLapAnalyzer.determine_intervals()
    print(res)

    file = "training-session-2014-03-16-263911274-403459ca-e3b5-447d-b45b-e622e723e967.json"
    session = Trainses_json(file)
    res = session.RManualLapAnalyzer.determine_intervals()
    print(res)

    "training-session-2015-10-02-263860694-a0cc566f-63e0-4a22-ae42-e2b50b649e81.json"
    file = "training-session-2014-03-16-263911274-403459ca-e3b5-447d-b45b-e622e723e967.json"

    file = "training-session-2015-04-18-263883440-3be46e75-6a93-4746-a320-96c9660f809c.json"
    session = Trainses_json(file)

    laps = session.return_laps()
    lapses = session.RAutoLapAnalyzer
    x = lapses.return_paraslist("speed")

    file = "training-session-2015-01-14-263888618-3d72bde3-4957-4db4-8fa6-662a180a2d23.json"
    session = Trainses_json(file)
    lapses = session.RAutoLapAnalyzer
    result = lapses.identify_roadrace()
    print(result)


def ex_lapanalyzer_identify():

    file = "training-session-2017-03-15-1202520256-b65156be-3420-4164-a6c9-6e34d0caafbd.json"
    session = Trainses_json(file)
    lapses = session.RManualLapAnalyzer
    lapses.identify_interval()
    


    files = glob.glob(os.path.join(path, "training-session-2021-*.json"))
    for fi in random.choices(files, k=5):
        filename = fi.split("\\")[-1]
        pprint.pprint(filename)
        session = Trainses_json(filename)

        if session.laps is not None:
            lapses = session.RManualLapAnalyzer

            print(lapses.compare_hr_sp())
            result = lapses.identify_interval()
            pprint.pprint(result)

            result = lapses.identify_sprints()
            pprint.pprint("sprints? " + str(result))

        if session.alaps is not None:
            try:
                lapses = session.RAutoLapAnalyzer
                result = lapses.identify_easyrun()
                pprint.pprint("easyrun?" + str(result))
            except KeyError:
                print("not passed:", session.file)

        print("_______________________________")


def ex_polar_sampleanalyzer():
    files = [
        "training-session-2015-06-26-263879702-2d485ab0-ef26-4100-b2ae-1ca9c5f144d6.json",
        "training-session-2019-10-30-4009640085-5105bf47-b37c-47c3-a96c-d74653ae0d5a.json",
        "training-session-2015-07-03-263876996-e9c14b6c-bc80-4c10-b335-91081c2552e7.json",
        "training-session-2015-09-20-263873564-7f116bac-8756-4f54-a5a0-9272ec0f44ee.json",
        "training-session-2015-09-29-263860670-b456e24e-4325-411f-b2c6-3e3a3bc29de6.json",
        "training-session-2015-10-24-263861018-3690058d-71c0-47c3-8539-e7b67e8099fe.json",
        "training-session-2015-10-17-263860916-1b563b91-c4f4-4991-878c-5c1225f84b2c.json",
    ]
    for file in files:
        session = Trainses_json(file)

        samses = session.SamAnalRunning

        dtroute = samses.return_s_timeroute()
        dt = samses.return_s_timesamples()

        samses.plot("speed")
        samses.plot("heartRate")

        idx1 = samses.return_idx_bytime(dtroute[0], "samples")
        try:
            idx2 = samses.return_idx_bytime(dtroute[-1], "samples", "last")
        except IndexError:
            continue

        try:
            samses.export_geojson()
        except IndexError:
            print("Lineup problem:" + file)
        except TypeError:
            print(traceback.format_exc())

        print(samses.determine_s_location())

    file = "training-session-2015-01-14-263888618-3d72bde3-4957-4db4-8fa6-662a180a2d23.json"
    samses = session.SamAnalRunning
    samples = samses.return_samples()
    X = samses.return_idxlowmovement()
    print(X)


def ex_sampleanalyzer_wind():
    files = [
        "training-session-2015-06-26-263879702-2d485ab0-ef26-4100-b2ae-1ca9c5f144d6.json",
        "training-session-2019-10-30-4009640085-5105bf47-b37c-47c3-a96c-d74653ae0d5a.json",
        "training-session-2015-07-03-263876996-e9c14b6c-bc80-4c10-b335-91081c2552e7.json",
        "training-session-2015-09-20-263873564-7f116bac-8756-4f54-a5a0-9272ec0f44ee.json",
        "training-session-2015-09-29-263860670-b456e24e-4325-411f-b2c6-3e3a3bc29de6.json",
        "training-session-2015-10-24-263861018-3690058d-71c0-47c3-8539-e7b67e8099fe.json",
        "training-session-2015-10-17-263860916-1b563b91-c4f4-4991-878c-5c1225f84b2c.json",
    ]

    for file in files:
        session = Trainses_json(file)
        samses = session.SamAnalRunning
        # normroute = samses.return_normalizedroute()
        normheading = samses.return_normalizedheading()
        head2wind = samses.return_normalizedrelwind(360)
        pp.figure()
        ax1 = pp.subplot(2, 1, 1)
        pp.plot(normheading)
        pp.subplot(2, 1, 2, sharex=ax1)
        pp.plot(head2wind)
        pp.show()


def ex_forerunner_analyzer():
    file = "20050725-190632.xml"
    session = Trainses_xml(file)
    print(session)

    file = "20041008-170457.xml"
    session = Trainses_xml(file)
    print(session)


def ex_garminfit_analyzer():
    file = "marcrotsaert_175152248.fit"
    session = Trainses_fit(file)
    print(session)

    file = "marcrotsaert_220466005.fit"
    session = Trainses_fit(file)
    print(session)


if __name__ == "__main__":
    ex_polar_lapanalyzer()
    ex_lapanalyzer_identify()
    ex_polar_sampleanalyzer()
    ex_sampleanalyzer_wind()
    ex_garminfit_analyzer()
    ex_forerunner_analyzer()
