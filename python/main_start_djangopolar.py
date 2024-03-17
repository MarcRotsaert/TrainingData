import os
import webbrowser
import asyncio
from pathlib import Path


async def runserver():
    path = Path(__file__).parent.parent.resolve()
    print(path)
    settingfile = " 'django/test_project2/settings.py' "
    # settingfile = " settings.py "

    os.chdir(path)
    # os.system(
    #     "python django/test_project2/manage.py runserver --setting"
    #     + settingfile
    #     + "8001"
    # )
    os.system("python django/test_project2/manage.py runserver " + settingfile + "8001")


def openproject():
    webbrowser.open_new_tab("http://127.0.0.1:8001/home")


async def main():
    task1 = asyncio.create_task(runserver())
    openproject()
    await task1


# asyncio.run(main())
