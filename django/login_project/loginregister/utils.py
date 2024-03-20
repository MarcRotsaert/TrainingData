import os
import re
from pathlib import Path

from django.conf import settings
from .models import UserProfile


basedir = settings.BASE_DIR
homedir = Path(basedir).parent.parent.resolve()
polardir = r"django\test_project2\test_project2"


def create_settings(userprofile: UserProfile):
    dummyfile = os.path.join(homedir, polardir, "settings_dummy.py")
    outputfile = os.path.join(homedir, polardir, "settings.py")
    with open(dummyfile, "r", encoding="utf-8") as g:
        text = g.read()
    textout = replace_input(text, userprofile)
    with open(outputfile, "w", encoding="utf-8") as f:
        f.write(textout)


def create_toml(userprofile: UserProfile):
    dummyfile = os.path.join(homedir, "config_dummy.toml")
    outputfile = os.path.join(homedir, "config.toml")
    with open(dummyfile, "r", encoding="utf-8") as g:
        text = g.read()
        g.close()
    textout = replace_input(text, userprofile)
    with open(outputfile, "w", encoding="utf-8") as f:
        f.write(textout)


def replace_input(text: str, userprofile: UserProfile) -> str:
    regex = re.findall("\{\{(\w+)\}\}", text)
    print(regex)

    for pattern in regex:
        try:
            repl = getattr(userprofile, pattern)
        except AttributeError:
            # print(repl)
            continue
        text = re.sub("\{\{" + pattern + "\}\}", str(repl), text)
    return text
