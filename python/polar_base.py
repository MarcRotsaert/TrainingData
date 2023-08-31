# Basic class attributes


class Basic_Collections:
    TRAININGTYPES = ["easy", "interval", "roadrace", "sprint"]
    DATATYPES = ["laps", "autoLaps", "samples"]
    SPORT = ["RUNNING", "CYCLING", "OTHER"]


class Base_polar(Basic_Collections):
    run_classattr = {
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
        "sample_param": ["altitude", "heartRate", "speed", "distance", "recordedRoute"],
        "sample_paces": {"low_movement": 7},
    }

    actions = ["read", "add", "identify", "determine", "read", "compare", "plot"]


class Base_training_classifier(Basic_Collections):
    actions = ["set"]


class Base_nosql:
    DATATYPES = {
        "database": "person",
        "collection": "year",
        "session": "training",
        "field": "",
        "docs": "",
    }

    RESUME = {
        "abstract": "session.abstract",
        "laps": "session.laps",
        "autolaps": "session:autolaps",
        "location": "function",
    }
