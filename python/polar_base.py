# Basic class attributes


class Trainses:
    trainingtypes = ["easy", "interval", "roadrace", "sprint"]
    datatypes = ["laps", "autolaps", "samples"]
    sports = ["RUNNING", "CYCLING", "OTHER"]


class Base_polar_json(Trainses):

    classattr = {
        "lap_paces": {
            "maxeasy": 14,
            "minroadrace": 15.3,
            "maxruninout": 13.2,
            "dspeedinterval": 3,
        },
        "lap_param": [
            "distance",
            "duration",
            "cadence",
            "heartRate",
            "speed",
            "ascent",
            "descent",
        ],
        "sample_loc": {
            "de velden": [[85575, 440076], 100],
            "baanbras": [[85085, 449400], 100],
            "kopjesloop": [[85055, 448570], 50],
            "schiehaven": [[90775, 435330], 600],
            "wippolder": [[86255, 446810], 150],
            "bergenopzoom": [[81385, 389191], 400],
            "menmoerhoeve": [[104258, 394390], 200],
            "sola": [[395744, -72146], 15000],
            "meijendel": [[82905, 460500], 300],
        },
    }

    actions = ["read", "add", "identify", "determine", "read", "compare", "plot"]


class Base_training_classifier(Trainses):
    actions = ["set"]


class Base_nosql:
    datatypes = {
        "database": "person",
        "collection": "year",
        "session": "training",
        "field": "",
        "docs": "",
    }

    resume = {
        "abstract": "session.abstract",
        "laps": "session.laps",
        "autolaps": "session:autolaps",
        "location": "function",
    }
