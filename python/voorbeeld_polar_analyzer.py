import os
import glob
import random
import pprint
import tomli
from matplotlib import pyplot as pp

from analyzer.polar_analyzer import Trainses_json

config = tomli.load(open("config.toml", "rb"))
path = config["polar_json"]["datapath"]

if True:
    file = "training-session-2015-04-18-263883440-3be46e75-6a93-4746-a320-96c9660f809c.json"
    session = Trainses_json(file)
    laps = session.return_laps()
    lapses = session.RAutoLapAnalyzer
    x = lapses.return_paraslist("speed")

if True:
    files = [
        "training-session-2019-10-30-4009640085-5105bf47-b37c-47c3-a96c-d74653ae0d5a.json",
        "training-session-2015-06-26-263879702-2d485ab0-ef26-4100-b2ae-1ca9c5f144d6.json",
    ]
    for file in files:
        session = Trainses_json(file)
        samses = session.SamAnalRunning
        dtroute = samses.return_s_timeroute()
        dt = samses.return_s_timesamples()

        idx1 = samses.return_idx_bytime(dtroute[0], "samples")
        try:
            idx2 = samses.return_idx_bytime(dtroute[-1], "samples", "last")
        except IndexError:
            continue

        try:
            samses.export_geojson()
        except TypeError:
            print(traceback.format_exc())
    files = glob.glob(os.path.join(path, "training-session-2022-*.json"))

if True:
    file = "training-session-2015-06-26-263879702-2d485ab0-ef26-4100-b2ae-1ca9c5f144d6.json"
    # file = "training-session-2019-10-30-4009640085-5105bf47-b37c-47c3-a96c-d74653ae0d5a.json"
    # training-session-2015-07-03-263876996-e9c14b6c-bc80-4c10-b335-91081c2552e7.json
    # training-session-2015-09-20-263873564-7f116bac-8756-4f54-a5a0-9272ec0f44ee.json
    # training-session-2015-09-29-263860670-b456e24e-4325-411f-b2c6-3e3a3bc29de6.json
    # training-session-2015-10-24-263861018-3690058d-71c0-47c3-8539-e7b67e8099fe.json
    # training-session-2015-10-17-263860916-1b563b91-c4f4-4991-878c-5c1225f84b2c.json
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
    samses.export_geojson()
    samses.plot("speed")


if True:
    file = "training-session-2015-01-14-263888618-3d72bde3-4957-4db4-8fa6-662a180a2d23.json"
    session = Trainses_json(file)
    lapses = session.RAutoLapAnalyzer
    result = lapses.identify_roadrace()
    samses = session.SamAnalRunning
    samples = samses.return_samples()
    X = samses.return_idxlowmovement()
    print(X)

if True:
    files = glob.glob(os.path.join(path, "training-session-2021-*.json"))
    pointcoll = []
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
        samses = session.SamAnalRunning
        samses.plot("speed")
        pprint.pprint(samses.determine_s_location())
