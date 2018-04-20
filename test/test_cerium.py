import unittest

from cerium import AndroidDriver, Keys


class AndroidDriverDemo(unittest.TestCase):

    def setUp(self):
        self.driver = AndroidDriver()

    def test_devices():
        print(self.driver.devices())

    def test_devices_l():
        print(self.driver.devices_l())

    def test_version():
        print(self.driver.version())

    def test_push():
        self.driver.push(local='test.txt', remote='/sdcard/test.txt')
        
    def test_pull():
        self.driver.pull(remote='/sdcard/test.txt', local='test.txt')

    def test_pull_screencap():
        self.driver.pull_screencap(local='screencap.png')

    def test_input_tap():
        self.driver.input_tap(100, 500)

    def test_input_swipe():
        self.driver.input_swipe(50, 100, 50, 200, duration=100)

    def test_input_text():
        self.driver.input_text("I'm White Turing.")

    def test_input_keyevent():
        self.driver.input_keyevent(Keys.HOME)

    def tearDown(self):
        self.driver.kill_server()


if __name__ == '__main__':
    unittest.main()