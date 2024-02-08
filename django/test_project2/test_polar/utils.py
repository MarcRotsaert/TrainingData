import tomli

from django.http import HttpRequest


def _return_configttype() -> list[str]:
    # config = tomli.load(open("../../config.toml", "rb"))
    config = tomli.load(open("config.toml", "rb"))
    return config["running"]["trainingtypes"]


def _create_ttype_dict(request: HttpRequest) -> dict:
    # terribly hacky, but for now it's alright
    ttype_db = {}
    ttypes = {"interval", "sprint", "roadrace", "easyrun"}
    for tt in ttypes:
        new_val = request.POST["trainingtype-" + tt]
        if tt != "interval":
            if new_val == "unknown" or "":
                new_val = None
            elif new_val == "false":
                new_val = False
            else:
                new_val = True
        ttype_db.update({tt: new_val})
    return ttype_db
