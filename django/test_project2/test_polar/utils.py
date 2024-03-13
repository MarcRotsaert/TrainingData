import tomli
from django.core.cache import cache
from django.conf import settings

from test_polar.models import PolarModel

from nosql_adapter import MongoPolar


# class Config()
def _return_configttype() -> list[str]:
    # config = tomli.load(open("../../config.toml", "rb"))
    config = tomli.load(open("config.toml", "rb"))
    return config["running"]["trainingtypes"]


def _set_cache_trainingdata(trainingen: list, cachetime: float) -> None:
    cache_key = "training_data"
    cache.clear()
    cache.set(cache_key, trainingen, cachetime)


def get_collections_name() -> list[str]:
    # config = tomli.load(open("config.toml", "rb"))
    # database = config["mongodb"]["database"]
    database = settings.DATABASES["default"]["NAME"]
    db_table = PolarModel._meta.db_table

    mongpol = MongoPolar(database, db_table)
    collections = mongpol.getAvailableCollections()
    collections.sort()
    print(collections)
    try:
        collections.remove("__schema__")
    except ValueError: 
        print("not present")
    try:
        collections.remove("django_migrations")
    except ValueError: 
        print("not present")

    return collections
