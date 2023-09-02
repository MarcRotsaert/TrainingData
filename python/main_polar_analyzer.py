import polar_analyzer as pol_an
import tomli


config = tomli.load(open("config.toml",'rb'))
path = config['polar_json']['datapath']
fnames = (
    "training-session-2014-01-27-263915162-07e7d91b-d3aa-4f89-b2f5-036d8a023f3e.json",
    "training-session-2014-01-28-263915222-2eae615f-9203-4444-a264-5bb5cfdef6e4.json",
    "training-session-2014-04-27-263909516-fe9cf303-39e2-4a0c-bd99-1045e7f5e3b3.json",
    "training-session-2014-06-13-263906738-f1c9ddc3-b859-4833-976c-f312d0a99076.json",
    "training-session-2014-06-26-263907098-511aa8c0-1ef7-4143-85c1-547a6829689c.json",
    "training-session-2014-09-20-263902910-e959734b-043e-4c79-9acf-c2de11aa748f.json",
    "training-session-2014-10-18-263901506-732b5d52-e5e4-4f20-b080-9068f5e6c96f.json",
    "training-session-2014-10-27-263901686-6054478b-7fa7-4a4c-99c1-0249e3f9be96.json",
    "training-session-2014-11-06-263898308-933bffed-d636-44e8-83d5-65dd0a5c2595.json",
)

for fname in fnames:
    training = pol_an.Trainses_json(path, fname)

    lap_an = pol_an.RManualLapAnalyzer(training.laps)
    print(lap_an.identify_easyrun())
