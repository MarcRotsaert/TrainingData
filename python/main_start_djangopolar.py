import os
import subprocess
import webbrowser
import asyncio
from pathlib import Path


async def runserver():
    rootpath = Path(__file__).parent.parent.parent.resolve()
    polarpath = Path(__file__).parent.parent.resolve()

    # os.chdir(polarpath)
    # print(os.path.exists(os.path.join(rootpath, "env_polar\Scripts")))

    settingfile = "test_project2.settings"

    # os.system(
    #     "python django/test_project2/manage.py runserver "
    #     + "--settings="
    #     + settingfile
    #     + " "
    #     + "8001"
    # )
    process = subprocess.Popen(
        [
            # os.path.join(rootpath, "polar_env/Scripts/activate"),
            "python",
            "django/test_project2/manage.py",
            "runserver",
            "--settings=" + settingfile,
            "8001",
        ],
        shell=True,
        stdout=open("C:/temp/stdout", "w"),
        stderr=open("C:/temp/stdout", "w"),
    )
    print(process.poll())


def openproject():
    webbrowser.open_new_tab("http://127.0.0.1:8001/home")


async def main():
    task1 = asyncio.create_task(runserver())
    openproject()
    await task1


# asyncio.run(main())
