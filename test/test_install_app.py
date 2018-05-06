import unittest
from time import sleep

from cerium import AndroidDriver


class TestCerium(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = AndroidDriver()
        cls.driver.unlock(9325)   # unlock by password

    def test_a_install_app(self):
        self.driver.install('test/yyb.apk')
        sleep(1)

    def test_b_view_packgets_list(self):
        apps = self.driver.view_packgets_list(keyword='tencent')
        self.assertIn('com.tencent.android.qqdownloader', apps)

    def test_c_uninstall_app(self):
        self.driver.uninstall('com.tencent.android.qqdownloader')

    def test_d_view_packgets_list(self):
        apps = self.driver.view_packgets_list(keyword='tencent')
        self.assertNotIn('com.tencent.android.qqdownloader', apps)

    @classmethod
    def tearDownClass(cls):
        cls.driver.lock()


if __name__ == '__main__':
    unittest.main()
