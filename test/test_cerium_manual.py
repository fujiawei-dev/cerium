from cerium import AndroidDriver
from cerium import Keys


driver = AndroidDriver(dev=True)   # show debug information
driver = AndroidDriver(wireless=True)
driver = AndroidDriver()

driver.unlock((29281-0.5)/3.14)   # unlock by password

driver.launch_app('com.tencent.mm/com.tencent.mm.ui.LauncherUI')   # launch WeChat

element = driver.find_element_by_class('android.widget.EditText')
element.send_keys("I'm White Turing.")

driver.close_app('com.tencent.mm')

driver.make_a_call()
driver.end_the_call()   # end call

driver.open_url('https://www.baidu.com')
driver.home()

driver.screencap_exec('test/screencap.png')

driver.install('test/yyb.apk')
driver.view_packgets_list(keyword='tencent')
driver.uninstall('com.tencent.android.qqdownloader')