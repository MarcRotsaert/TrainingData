import unittest
import tomli

import os


class TomliRead(unittest.TestCase):
    @classmethod
    def setUp(cls) -> None:
        cls.dummy_file = "config_dummy.toml"

        path_onedrive = os.environ("OneDrive")
        datapath_tracks = os.path.join(path_onedrive, "Documenten/logboek_looptracks")
        cls.cf = {
            "datapath_polar": os.path.join(datapath_tracks, "polar-user-data-export"),
            "datapath_fit": os.path.join(datapath_tracks, "looptracks_garmin"),
            "datapath_forerunner": os.path.join(
                datapath_tracks, "looptracks_forerunner/Looptracks/XMLfiles"
            ),
        }

    @unittest.TestCase
    def test_make_config(self):
        g = open((self.dummy_file, "rb"))
        text = g.read()
        for key, val in self.cf:
            text.replace(key, val)

        config = tomli.load(open("config_dummy.toml", "rb"))
        self.asserTrue(config)

    def test_loadtomli(self):
        config = tomli.load(open("config.toml", "rb"))


if __name__ == "__main__":
    TomliRead.setUp()
