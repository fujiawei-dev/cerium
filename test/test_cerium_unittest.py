import unittest
from time import sleep

from cerium import AndroidDriver


class TestCerium(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = AndroidDriver()
        cls.driver.unlock(1997)   # unlock by password

    def test_a_launch_app(self):
        self.driver.launch_app('com.tencent.mm/com.tencent.mm.ui.LauncherUI')
        sleep(5)

    def test_b_click(self):
        self.driver.click(500, 250)
        sleep(1)

    def test_c_send_keys(self):
        element = self.driver.find_element_by_class('android.widget.EditText')
        element.send_keys("I'm White Turing.")
        sleep(1)

    def test_d_close_app(self):
        self.driver.close_app('com.tencent.mm')
        sleep(1)

    def test_e_call(self):
        self.driver.make_a_call()
        sleep(3)
    
    def test_f_endcall(self):
        self.driver.end_the_call()
        sleep(1)

    def test_g_open_url(self):
        self.driver.open_url('https://www.baidu.com')
        sleep(3)

    def test_h_screencap_exec(self):
        self.driver.screencap_exec('test/screencap.png')
        sleep(1)
    
    def test_i_home(self):
        self.driver.home()
        sleep(3)

    @classmethod
    def tearDownClass(cls):
        cls.driver.lock()


if __name__ == '__main__':
    unittest.main()
