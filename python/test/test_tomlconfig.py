import unittest
import tomli

import os


class TomliRead(unittest.TestCase):
    @classmethod
    def setUp(cls) -> None:
        cls.dummy_file = "config_dummy.toml"
        cls.test_file = "config_test.toml"
        path_onedrive = os.environ["OneDrive"].encode()
        path_onedrive = path_onedrive.replace(b'\\',b'/')

        datapath_tracks = path_onedrive + b"/Documenten/logboek_looptracks"
        cls.cf = {
            b"datapath_polar": datapath_tracks+  b"/polar-user-data-export",
            b"datapath_fit": datapath_tracks + b"/looptracks_garmin",
            b"datapath_forerunner": datapath_tracks + b"looptracks_forerunner/Looptracks/XMLfiles",
        }

    def test_make_config(self):
        # this needs to be in a 
        with open(self.dummy_file, "rb") as g:
            text = g.read()
            for key in self.cf:
                text = text.replace(key, self.cf[key])
            text = text.replace('{{'.encode(), ''.encode())
            text = text.replace('}}'.encode(), ''.encode())

        with open(self.test_file, 'wb') as h:
            h.write(text)

        
        config = tomli.load(open(self.test_file, "rb"))


    def test_header_config(self):
        headers = ("polar_json",
                   "forerunner_xml",
                   "garmin_fit",
                   "mongodb",
                   "running",
        )

        config = tomli.load(open(self.dummy_file, "rb"))
        with self.subTest(config):
            self.assertEqual(len(config), len(headers))
        
        for item in config: 
            with self.subTest(item):
                self.assertIn(item, config)

    @classmethod
    def tearDown(cls) -> None:
        try:
            os.remove(cls.test_file)
        except:
            pass


