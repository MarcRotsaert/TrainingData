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
    files = [
# "training-session-2014-03-04-263911052-aa284d51-d372-4939-b83f-b9c732d3eb3a.json",
# "training-session-2014-08-12-263904236-745120a4-29ce-4447-9405-db67f292622d.json",
# "training-session-2014-11-04-263898290-253ad8c7-76cd-45b6-bc86-c49074870ecd.json",
# "training-session-2014-11-18-263898758-b1261b4c-6f72-4469-9b0c-68aa92e3df24.json",

# "training-session-2015-02-17-263886464-81c22d89-24ce-41b2-b130-98f85cec4dbe.json",

# "training-session-2015-05-26-263881424-622c9ae7-136e-4eb9-a901-87dd3a0728ee.json",


# "training-session-2017-05-03-1347831169-a6b9ff50-2ba7-456a-a1a3-21474ab51ef5.json",
# "training-session-2017-10-18-1852531570-f6d37baf-2b3d-4514-852c-d4eef4b025c3.json",
# "training-session-2017-11-08-1921335148-ffcf00ed-05cf-454a-a665-bf553ff9bdcd.json",
# "training-session-2017-12-06-1990656442-fffa734d-af95-44af-b180-e6714ae7e29a.json",
# "training-session-2017-12-27-2038992394-59b467c5-4fa5-4e7a-be9e-d7b4fa023035.json",
    ] 
    files =     [ 
# "training-session-2015-02-04-263886074-f1452aa8-9734-47c9-bb3c-61ed2c457084.json",
# "training-session-2015-02-17-263886464-81c22d89-24ce-41b2-b130-98f85cec4dbe.json",
# "training-session-2015-06-03-263879174-463f62f9-4e7f-455a-9d42-fda0b0f237cc.json",
# "training-session-2015-06-09-263879396-b9438e81-065a-43c5-8c36-2b4853abffda.json",
"training-session-2015-07-12-263877212-0d71763a-94dc-44d6-8848-cd2b0a2e92d0.json",
# "training-session-2015-10-06-263860766-8f9f123e-a2b9-4497-b9fa-36d5df196706.json",
# "training-session-2015-10-14-263860874-8761fac4-2fb2-4d97-9081-2214bcc9208e.json",
# "training-session-2015-11-04-272100918-99d6f253-e2ea-4e37-a483-ba1971a8f462.json",
]
    for file in files:  
    # file = "training-session-2014-03-04-263911052-aa284d51-d372-4939-b83f-b9c732d3eb3a.json"
        print(file)
        session = Trainses_json(file)
    
        res = session.RManualLapAnalyzer.return_intervalstring()
        print(res)
        # print(session.RManualLapAnalyzer.determine_corrspeed_int())
        # print(session.RManualLapAnalyzer.return_paraslist("speed", "avg"))

    file = "training-session-2015-06-10-263879420-179087dd-448d-4a57-9d5f-caaa193b05f8.json"
    session = Trainses_json(file)
    res = session.RManualLapAnalyzer.return_intervalstring()
    print(res)
    print(session.RManualLapAnalyzer.determine_corrspeed_int())
    print(session.RManualLapAnalyzer.return_paraslist("speed", "avg"))

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
                res = session.RManualLapAnalyzer.return_intervalstring()
                print(res)
                k += 1
    #
    # training-session-2015-01-25-263888810-887b73d8-5599-4534-833c-521322b8c28b.json
    # training-session-2015-03-11-263884640-0e71a9a2-88f6-4a50-a478-4401c7e9128c.json

    file = "training-session-2015-01-07-263888486-2d791dc2-1ee2-4964-bb44-558579c19c6f.json"
    session = Trainses_json(file)
    res = session.RManualLapAnalyzer.return_intervalstring()
    print(res)

    file = "training-session-2014-03-16-263911274-403459ca-e3b5-447d-b45b-e622e723e967.json"
    session = Trainses_json(file)
    res = session.RManualLapAnalyzer.return_intervalstring()
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
    # crit 3, but location baanbras.
    files = [
        # "training-session-2014-09-23-263902976-9b0479b8-d510-4ad0-9qf26-906666161153.json",
        # "training-session-2014-09-30-263903114-b27ef81e-c085-4b88-9d35-61091d7de3dc.json",
        # "training-session-2017-03-08-1181389126-47ee7d62-fddd-4428-8642-69a1818591f9.json",
        "training-session-2017-03-15-1202520256-b65156be-3420-4164-a6c9-6e34d0caafbd.json",
        "training-session-2017-03-29-1249402670-1d7264df-df18-4076-a426-970db7a7b94e.json",
    ]
    files = [
        "training-session-2017-02-22-1144054899-ad01617e-6217-4aa9-9d24-501af712b65b.json"
    ]
    for file in files:
        session = Trainses_json(file)
        lapses = session.RManualLapAnalyzer
        lapses.identify_interval()

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
    ex_lapanalyzer_identify()
    ex_polar_lapanalyzer()
    ex_garminfit_analyzer()
    ex_forerunner_analyzer()
    ex_polar_sampleanalyzer()
    ex_sampleanalyzer_wind()
