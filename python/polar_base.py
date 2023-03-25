class Trainses:
    trainingtypes = {"easy": 0, "interval": 1, "roadrace": 2, "sprint": 3}
    datatypes=['laps','autolaps','samples']

    sports = {
        "RUNNING": 0,
        "CYCLING": 1,
        "OTHER": 2,
    }


class Base_polar_json(Trainses):
    actions = ['read','add','identify','read']


class Base_training_classifier(Trainses):
    actions =['set',]

class  Base_nosql:
    resume = {"abstract":"session.abstract",
                "laps":"session.laps", 
                "autolaps":"session:autolaps"],
                "location":'location', 
    }
