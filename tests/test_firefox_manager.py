import os

import pytest
from selenium import webdriver

from tests.test_cache import cache, delete_cache
from webdriver_manager.driver import GeckoDriver
from webdriver_manager.firefox import GeckoDriverManager

PATH = '.'


def delete_old_install(path=None):
    if not path is None:
        path = os.path.abspath(path)
        try:
            os.remove(os.path.join(path, 'geckodriver.exe'))
            os.remove(os.path.join(path, 'geckodriver.zip'))
        except:
            pass


def test_gecko_manager_with_correct_version():
    driver_path = GeckoDriverManager("v0.11.0").install()
    assert os.path.exists(driver_path)


def test_gecko_manager_with_selenium():
    driver_path = GeckoDriverManager().install()
    ff = webdriver.Firefox(executable_path=driver_path,
                           log_path=os.path.join(os.path.dirname(__file__), "log.log"))
    ff.get("http://automation-remarks.com")
    ff.quit()


def test_gecko_manager_with_wrong_version():
    with pytest.raises(ValueError) as ex:
        delete_old_install()
        driver_path = GeckoDriverManager("0.2").install()
        ff = webdriver.Firefox(executable_path=driver_path)
        ff.quit()
    assert ex.value.args[0] == "There is no such driver geckodriver with version 0.2"


def test_can_download_ff_x64():
    delete_cache()
    driver_path = GeckoDriverManager(os_type="win64").install()
    print(driver_path)


@pytest.mark.parametrize('os_type', ['win32',
                                     'win64',
                                     'linux32',
                                     'linux64',
                                     'mac64'])
def test_can_get_driver_from_cache(os_type):
    delete_cache()
    GeckoDriverManager(os_type=os_type).install()
    driver_path = GeckoDriverManager(os_type=os_type).install()
    assert os.path.exists(driver_path)
