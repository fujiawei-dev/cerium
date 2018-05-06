import unittest
from time import sleep

from cerium import AndroidDriver


class TestCerium(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = AndroidDriver()
        cls.driver.unlock(1997)   # unlock by password

    def test_brightness_down(self):
        self.driver.brightness_down()
        sleep(1)
    
    def test_brightness_up(self):
        self.driver.brightness_up()
        sleep(1)

    def test_volume_mute(self):
        self.driver.volume_mute()
        sleep(1)
    
    def test_volume_up(self):
        self.driver.volume_up()
        sleep(1)

    def test_volume_down(self):
        self.driver.volume_down()
        sleep(1)

    def test_open_contacts(self):
        self.driver.open_contacts()
        sleep(1)
        self.driver.home()

    def test_open_calendar(self):
        self.driver.open_calendar()
        sleep(1)
        self.driver.home()

    def test_open_calculator(self):
        self.driver.open_calculator()
        sleep(1)
        self.driver.home()

    @classmethod
    def tearDownClass(cls):
        cls.driver.lock()


def suite():
    suite = unittest.TestSuite()
    tests = (TestCerium(i) for i in ['test_brightness_down', 'test_brightness_up', 'test_volume_mute', 'test_volume_up', 'test_volume_down', 'test_open_contacts', 'test_open_calendar', 'test_open_calculator'])
    suite.addTests(tests)
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())