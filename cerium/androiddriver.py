# Licensed to the Software Freedom Conservancy (SFC) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The SFC licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

'''The AndroidDriver implementation.'''


import os
import re
import tempfile

from lxml import html

from .by import By
from .elements import Elements
from .exceptions import (ApplicationsException, CharactersException,
                         DeviceConnectionException, NoSuchElementException,
                         NoSuchPackageException)
from .intent import Actions, Category
from .keys import Keys
from .service import Service


class BaseAndroidDriver(Service):
    '''Controls Android Debug Bridge and allows you to drive the android device.'''

    _element_cls = Elements
    _temp = os.path.join(tempfile.gettempdir(), 'uidump.xml')
    _nodes = None

    def __init__(self, executable_path='default', device_sn=None, wireless=False, host='192.168.0.3', port=5555, service_port=5037, env=None, service_args=None, dev=False):
        '''Creates a new instance of the android driver.

        Starts the service and then creates new instance of android driver.

        Args:
            executable_path: Path to the executable. The default uses its own executable.
            device_sn: Device serial number.
            wireless/host/port: If wireless is True, will connect your device via WLAN driectly. \
                                         The premise is that your device has opened the port and \
                                         you know the device's IP address.
            service_port: Service port you would like the service to run, \
                                if left as 0, a free port will be found.
            env: Environment variables.
            service_args: List of args to pass to the androiddriver service.
        '''

        self._dev = dev
        super(BaseAndroidDriver, self).__init__(executable_path=executable_path,
                                            port=service_port, env=env, service_args=service_args)
        self.start()
        self.device_sn = device_sn

        if wireless:
            if host and port:
                self.connect(host, port)
            else:
                raise ValueError('You need to specify the HOST and PORT.')

        self.devices_list = self.devices()
        self._detect_devices()

    def _detect_devices(self):
        '''Detect whether devices connected.'''
        devices_num = len(self.devices_list)
        if devices_num == 0:
            raise DeviceConnectionException(
                'No devices are connected. Please connect the device with USB or \
                via WLAN and turn on the USB debugging option.')
        elif not self.device_sn and devices_num > 1:
            raise DeviceConnectionException(
                'Multiple devices detected: {}, please specify device \
                serial number or host.'.format(' | '.join(self.devices_list)))
        else:
            self.device_sn = self.devices_list[0]

    def start_server(self):
        '''Start server.'''
        self.start()

    def kill_server(self):
        '''Kill the server if it is running.'''
        self.stop()

    def restart_server(self):
        '''Restart the server if it is running.'''
        self.restart()

    def _execute(self, *args):
        '''Execute command.'''
        process = self.execute(*args)
        command = ' '.join(process.args)
        if self._dev:
            output, error = process.communicate()
            print(
                "Debug Information",
                "Command: {!r}".format(command),
                "Output: {!r}".format(output.encode('utf-8')),
                "Error: {!r}".format(error.encode('utf-8')),
                sep='\n', end='\n{}\n'.format('=' * 80)
            )
        return process.communicate()

    # Android Device Information
    def get_device_model(self) -> str:
        '''Show device model.'''
        output, _ = self._execute(
            '-s', self.device_sn, 'shell', 'getprop', 'ro.product.model')
        return output.strip()

    def get_battery_info(self) -> dict:
        '''Show device battery information.

        Returns:
            A dict. For example:

                {'AC powered': 'false',
                'Charge counter': '0',
                'Max charging current': '0',
                'Max charging voltage': '0',
                'USB powered': 'false',
                'Wireless powered': 'false',
                'health': '2',
                'level': '67',
                'present': 'true',
                'scale': '100',
                'status': '3',
                'technology': 'Li-poly',
                'temperature': '310',
                'voltage': '3965'}
        '''
        output, _ = self._execute(
            '-s', self.device_sn, 'shell', 'dumpsys', 'battery')
        battery_status = re.split('\n  |: ', output[33:].strip())
        return dict(zip(battery_status[::2], battery_status[1::2]))

    def get_resolution(self) -> list:
        '''Show device resolution.'''
        output, _ = self._execute('-s', self.device_sn, 'shell', 'wm', 'size')
        return output.split()[2].split('x')

    def get_screen_density(self) -> str:
        '''Show device screen density (PPI).'''
        output, _ = self._execute(
            '-s', self.device_sn, 'shell', 'wm', 'density')
        return output.split()[2]

    def get_displays_params(self) -> str:
        '''Show displays parameters.'''
        output, error = self._execute(
            '-s', self.device_sn, 'shell', 'dumpsys', 'window', 'displays')
        return output

    def get_android_id(self) -> str:
        '''Show Android ID.'''
        output, _ = self._execute(
            '-s', self.device_sn, 'shell', 'settings', 'get', 'secure', 'android_id')
        return output.strip()

    def get_android_version(self) -> str:
        '''Show Android version.'''
        output, _ = self._execute(
            '-s', self.device_sn, 'shell', 'getprop', 'ro.build.version.release')
        return output.strip()

    def get_device_mac(self) -> str:
        '''Show device MAC.'''
        output, _ = self._execute(
            '-s', self.device_sn, 'shell', 'cat', '/sys/class/net/wlan0/address')
        return output.strip()

    def get_cpu_info(self) -> str:
        '''Show device CPU information.'''
        output, _ = self._execute(
            '-s', self.device_sn, 'shell', 'cat', '/proc/cpuinfo')
        return output

    def get_memory_info(self) -> str:
        '''Show device memory information.'''
        output, _ = self._execute(
            '-s', self.device_sn, 'shell', 'cat', '/proc/meminfo')
        return output

    def get_sdk_version(self) -> str:
        '''Show Android SDK version.'''
        output, _ = self._execute(
            '-s', self.device_sn, 'shell', 'getprop', 'ro.build.version.sdk')
        return output.strip()

    def root(self):
        '''Restart adbd with root permissions.'''
        output, _ = self._execute('-s', self.device_sn, 'root')
        if not output:
            raise PermissionError(
                '{!r} does not have root permission.'.format(self.device_sn))

    def unroot(self):
        '''Restart adbd without root permissions.'''
        self._execute('-s', self.device_sn, 'unroot')

    def tcpip(self, port=5555):
        '''Restart adb server listening on TCP on PORT.'''
        self._execute('-s', self.device_sn, 'tcpip', str(port))

    def get_ip_addr(self) -> str:
        '''Show IP Address.'''
        output, _ = self._execute(
            '-s', self.device_sn, 'shell', 'ip', '-f', 'inet', 'addr', 'show', 'wlan0')
        ip_addr = re.findall(
            r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b", output)
        if not ip_addr:
            raise ConnectionError('The device is not connected to WLAN.')
        return ip_addr[0]

    def auto_connect(self, port=5555):
        '''Connect to a device via TCP/IP automatically.'''
        host = self.get_ip_addr()
        self.tcpip(port)
        self.connect(host, port)
        print('Now you can unplug the USB cable, and control your device via WLAN.')

    def push(self, local='LICENSE', remote='/sdcard/LICENSE'):
        '''Copy local files/directories to device.'''
        if not os.path.exists(local):
            raise FileNotFoundError('Local {!r} does not exist.'.format(local))
        self._execute('-s', self.device_sn, 'push', local, remote)

    def push_sync(self, local='LICENSE', remote='/sdcard/LICENSE'):
        '''Only push files that are newer on the host than the device.'''
        if not os.path.exists(local):
            raise FileNotFoundError('Local {!r} does not exist.'.format(local))
        self._execute('-s', self.device_sn, 'push', '--sync', local, remote)

    def pull(self, remote, local):
        '''Copy files/directories from device.'''
        output, _ = self._execute('-s', self.device_sn, 'pull', remote, local)
        if 'error' in output:
            raise FileNotFoundError(
                'Remote {!r} does not exist.'.format(remote))

    def pull_a(self, remote, local):
        '''Copy files/directories from device, and preserve file timestamp and mode.'''
        output, _ = self._execute(
            '-s', self.device_sn, 'pull', '-a', remote, local)
        if 'error' in output:
            raise FileNotFoundError(
                'Remote {!r} does not exist.'.format(remote))

    def sync(self, option='all'):
        '''Sync a local build from $ANDROID_PRODUCT_OUT to the device (default all).'''
        if option in ['system', 'vendor', 'oem', 'data', 'all']:
            self._execute('-s', self.device_sn, 'sync', option)
        else:
            raise ValueError('There is no option named: {!r}.'.format(option))

    def sync_l(self, option='all'):
        '''List but don't copy.'''
        if option in ['system', 'vendor', 'oem', 'data', 'all']:
            self._execute('-s', self.device_sn, 'sync', '-l', option)
        else:
            raise ValueError('There is no option named: {!r}.'.format(option))

    # Application Management
    def install(self, package: str, option='-r'):
        '''Push package to the device and install it.

        Args:
            option: 
                -l: forward lock application
                -r: replace existing application
                -t: allow test packages
                -s: install application on sdcard
                -d: allow version code downgrade (debuggable packages only)
                -g: grant all runtime permissions
        '''
        if not os.path.isfile(package):
            raise FileNotFoundError('{!r} does not exist.'.format(package))
        for i in option:
            if i not in '-lrtsdg':
                raise ValueError(
                    'There is no option named: {!r}.'.format(option))
        self._execute('-s', self.device_sn, 'install', option, package)

    def install_multiple(self, *packages, option='-r'):
        '''
        Push packages to the device and install them.

        Args:
            option: 
                -l: forward lock application
                -r: replace existing application
                -t: allow test packages
                -s: install application on sdcard
                -d: allow version code downgrade (debuggable packages only)
                -p: partial application install (install-multiple only)
                -g: grant all runtime permissions
        '''
        for package in packages:
            if not os.path.isfile(package):
                raise FileNotFoundError('{!r} does not exist.'.format(package))
        for i in option:
            if i not in '-lrtsdpg':
                raise ValueError(
                    'There is no option named: {!r}.'.format(option))
        self._execute('-s', self.device_sn,
                      'install-multiple', option, *packages)

    def uninstall(self, package):
        '''Remove this app package from the device.'''
        if package not in self.view_packgets_list():
            raise NoSuchPackageException(
                'There is no such package {!r}.'.format(package))
        self._execute('-s', self.device_sn, 'uninstall', package)

    def uninstall_k(self, package):
        '''Remove this app package from the device, and keep the data and cache directories.'''
        if package not in self.view_packgets_list():
            raise NoSuchPackageException(
                'There is no such package {!r}.'.format(package))
        self._execute('-s', self.device_sn, 'uninstall', '-k', package)

    def view_packgets_list(self, option='-e', keyword=''):
        '''Show all packages.

        Args:
            option: 
                -f see their associated file
                -d filter to only show disabled packages
                -e filter to only show enabled packages
                -s filter to only show system packages
                -3 filter to only show third party packages
                -i see the installer for the packages
                -u also include uninstalled packages
                -keyword: optionally only those whose name contains the text in keyword
        '''
        if option not in ['-f', '-d', '-e', '-s', '-3', '-i', '-u']:
            raise ValueError('There is no option called {!r}.'.format(option))
        output, _ = self._execute(
            '-s', self.device_sn, 'shell', 'pm', 'list', 'packages', option, keyword)
        return list(map(lambda x: x[8:], output.splitlines()))

    def view_package_path(self, package):
        '''Print the path to the APK of the given.'''
        if package not in self.view_packgets_list():
            raise NoSuchPackageException(
                'There is no such package {!r}.'.format(package))
        output, _ = self._execute(
            '-s', self.device_sn, 'shell', 'pm', 'path', package)
        return output[8:-1]

    def clear_app_data(self, package):
        '''Deletes all data associated with a package.'''
        if package not in self.view_packgets_list():
            raise NoSuchPackageException(
                'There is no such package {!r}.'.format(package))
        self._execute('-s', self.device_sn, 'shell', 'pm', 'clear', package)

    def view_focused_activity(self):
        '''View focused activity.'''
        output, _ = self._execute(
            '-s', self.device_sn, 'shell', 'dumpsys', 'activity', 'activities')
        return re.findall(r'mFocusedActivity: .+(com[a-zA-Z0-9\.]+/.[a-zA-Z0-9\.]+)', output)[0]

    def view_running_services(self, package=''):
        '''View running services.'''
        output, _ = self._execute(
            '-s', self.device_sn, 'shell', 'dumpsys', 'activity', 'services', package)
        return output

    def view_package_info(self, package=''):
        '''View package detail information.'''
        output, _ = self._execute(
            '-s', self.device_sn, 'shell', 'dumpsys', 'package', package)
        return output

    def view_current_app_behavior(self):
        '''View application behavior in the current window.'''
        output, _ = self._execute(
            '-s', self.device_sn, 'shell', 'dumpsys', 'window', 'windows')
        return re.findall(r'mCurrentFocus=.+(com[a-zA-Z0-9\.]+/.[a-zA-Z0-9\.]+)', output)[0]

    def view_surface_app_activity(self):
        '''Get package with activity of applications that are running in the foreground.'''
        output, error = self._execute(
            '-s', self.device_sn, 'shell', 'dumpsys', 'window', 'w')
        return re.findall(r"name=([a-zA-Z0-9\.]+/.[a-zA-Z0-9\.]+)", output)

    # Interact with Applications
    def _app_base_start(self, option, args):
        '''
        Args:
            option: 
                -a <ACTION>
                -c <CATEGORY>
                -n <COMPONENT>
        '''
        _, error = self._execute('-s', self.device_sn,
                                 'shell', 'am', 'start', option, *args)
        if error and error.startswith('Error'):
            raise ApplicationsException(error.split(':', 1)[-1].strip())

    def app_start_action(self, *args):
        '''Start action.'''
        self._app_base_start('-a', args)

    def app_start_category(self, *args):
        '''Start category.'''
        self._app_base_start('-c', args)

    def app_start_activity(self, *args):
        '''Start activity.'''
        self._app_base_start('-n', args)

    def app_start_service(self, *args):
        '''Start a service.'''
        _, error = self._execute('-s', self.device_sn,
                                 'shell', 'am', 'startservice', *args)
        if error and error.startswith('Error'):
            raise ApplicationsException(error.split(':', 1)[-1].strip())

    def app_stop_service(self, *args):
        '''Stop a service'''
        _, error = self._execute('-s', self.device_sn, 'shell',
                                 'am', 'stopservice', *args)
        if error and error.startswith('Error'):
            raise ApplicationsException(error.split(':', 1)[-1].strip())

    def app_broadcast(self, *args):
        '''Send a broadcast.'''
        _, error = self._execute('-s', self.device_sn, 'shell',
                                 'am', 'broadcast', *args)
        if error:
            raise ApplicationsException(error.split(':', 1)[-1].strip())

    def close_app(self, package):
        '''Close an application.'''
        self._execute('-s', self.device_sn, 'shell',
                      'am', 'force-stop', package)

    def app_trim_memory(self, pid: int, level='RUNNING_LOW'):
        '''Trim memory.

        Args:
            level: HIDDEN | RUNNING_MODERATE | BACKGROUNDRUNNING_LOW | \
                     MODERATE | RUNNING_CRITICAL | COMPLETE
        '''
        _, error = self._execute('-s', self.device_sn, 'shell',
                                 'am', 'send-trim-memory', str(pid), level)
        if error and error.startswith('Error'):
            raise ApplicationsException(error.split(':', 1)[-1].strip())

    def app_start_up_time(self, package):
        '''Get the time it took to launch your application.'''
        output, _ = self._execute(
            '-s', self.device_sn, 'shell', 'am', 'start', '-W', package)
        return re.findall('TotalTime: \d+', output)[0]

    def screencap(self, filename='/sdcard/screencap.png'):
        '''Taking a screenshot of a device display.'''
        self._execute('-s', self.device_sn, 'shell',
                      'screencap', '-p', filename)

    def pull_screencap(self, remote='/sdcard/screencap.png', local='screencap.png'):
        '''Taking a screenshot of a device display, then copy it to your computer.'''
        self.screencap(remote)
        self.pull(remote, local)

    def screencap_exec(self, filename='screencap.png'):
        '''Taking a screenshot of a device display, then copy it to your computer.'''
        # self.execute('-s', self.device_sn, 'exec-out',
        #               'screencap', '-p', '>', filename)
        self.pull_screencap(local=filename)

    def screenrecord(self, bit_rate: int = 5000000, time_limit: int = 180, filename='/sdcard/demo.mp4'):
        '''Recording the display of devices running Android 4.4 (API level 19) and higher.

        Args:
            bit_rate:You can increase the bit rate to improve video quality, but doing so results in larger movie files.
            time_limit: Sets the maximum recording time, in seconds, and the maximum value is 180 (3 minutes).

        '''
        self._execute('-s', self.device_sn, 'shell',
                      'screenrecord', '--bit-rate', str(bit_rate), '--time-limit', str(time_limit), filename)

    def pull_screenrecord(self, bit_rate: int = 5000000, time_limit: int = 180, remote='/sdcard/demo.mp4', local='demo.mp4'):
        '''Recording the display of devices running Android 4.4 (API level 19) and higher. Then copy it to your computer.

        Args:
            bit_rate:You can increase the bit rate to improve video quality, but doing so results in larger movie files.
            time_limit: Sets the maximum recording time, in seconds, and the maximum value is 180 (3 minutes).

        '''
        self.screenrecord(bit_rate, time_limit, filename=remote)
        self.pull(remote, local)

    def click(self, x, y):
        '''Simulate finger click.'''
        self._execute('-s', self.device_sn, 'shell',
                      'input', 'tap', str(x), str(y))

    def swipe(self, x1, y1, x2, y2, duration=100):
        '''Simulate finger swipe.'''
        self._execute('-s', self.device_sn, 'shell',
                      'input', 'swipe', str(x1), str(y1), str(x2), str(y2), str(duration))

    def send_keys(self, text: str = 'cerium'):
        '''Simulates typing keys.'''
        for char in text:
            if '\u4e00' <= char <= '\u9fff':
                raise CharactersException(
                    'Text cannot contain non-English characters, such as {!r}.'.format(char))
        text = text.replace(' ', '\ ')
        self._execute('-s', self.device_sn, 'shell',
                      'input', 'text', text)

    def send_keyevents(self, keyevent: int):
        '''Simulates typing keyevents.'''
        self._execute('-s', self.device_sn, 'shell',
                      'input', 'keyevent', str(keyevent))

    def send_keyevents_long_press(self, keyevent: int):
        '''Simulates typing keyevents long press.'''
        self._execute('-s', self.device_sn, 'shell',
                      'input', 'keyevent', '--longpress', str(keyevent))

    def send_monkey(self, *args):
        '''Generate pseudo-random user events to simulate clicks, touches, gestures, etc.'''
        self._execute('-s', self.device_sn, 'shell', 'monkey', *args)

    def reboot(self):
        '''Reboot the device.'''
        self._execute('-s', self.device_sn, 'reboot')

    def recovery(self):
        '''Reboot to recovery mode.'''
        self._execute('-s', self.device_sn, 'reboot', 'recovery')

    def fastboot(self):
        '''Reboot to bootloader mode.'''
        self._execute('-s', self.device_sn, 'reboot', 'bootloader')

    def uidump(self, local=None):
        '''Get the current interface layout file.'''
        local = local if local else self._temp
        self._execute('-s', self.device_sn, 'shell', 'uiautomator',
                      'dump', '--compressed', '/data/local/tmp/uidump.xml')
        self.pull('/data/local/tmp/uidump.xml', local)
        ui = html.fromstring(open(local, 'rb').read())
        self._nodes = ui.iter(tag="node")

    def find_element(self, value, by=By.ID, renew=False):
        '''Find a element or the first element.'''
        if renew or not self._nodes:
            self.uidump()
        for node in self._nodes:
            if node.attrib[by] == value:
                bounds = node.attrib['bounds']
                coord = list(map(int, re.findall(r'\d+', bounds)))
                click_point = (coord[0] + coord[2]) / \
                    2, (coord[1] + coord[3]) / 2
                return self._element_cls(self, node.attrib, by, value, coord, click_point)
        raise NoSuchElementException(
            'No such element: {}={!r}.'.format(by, value))

    def find_elements(self, value, by=By.ID, renew=False):
        '''Find all elements.'''
        elements = []
        if renew or not self._nodes:
            self.uidump()
        for node in nodes:
            if node.attrib[by] == value:
                bounds = node.attrib['bounds']
                coord = list(map(int, re.findall(r'\d+', bounds)))
                click_point = (coord[0] + coord[2]) / \
                    2, (coord[1] + coord[3]) / 2
                elements.append(self._element_cls(
                    self, node.attrib, by, value, coord, click_point))
        if elements:
            return elements
        raise NoSuchElementException(
            'No such element: {}: {!r}.'.format(by, value))

    def find_element_by_id(self, id_, renew=False):
        '''Finds an element by id.

        Args:
            id_: The id of the element to be found.

        Returns:
            The element if it was found.

        Raises:
            NoSuchElementException - If the element wasn't found.

        Usage:
            element = driver.find_element_by_id('foo')
        '''
        return self.find_element(by=By.ID, value=id_, renew=renew)

    def find_elements_by_id(self, id_, renew=False):
        '''Finds multiple elements by id.

        Args:
            id_: The id of the elements to be found.

        Returns:
            A list with elements if any was found. An empty list if not.

        Raises:
            NoSuchElementException - If the element wasn't found.

        Usage:
            elements = driver.find_elements_by_id('foo')
        '''
        return self.find_elements(by=By.ID, value=id_, renew=renew)

    def find_element_by_name(self, name, renew=False):
        '''Finds an element by name.

        Args:
            name: The name of the element to be found.

        Returns:
            The element if it was found.

        Raises:
            NoSuchElementException - If the element wasn't found.

        Usage:
            element = driver.find_element_by_name('foo')
        '''
        return self.find_element(by=By.NAME, value=name, renew=renew)

    def find_elements_by_name(self, name, renew=False):
        '''Finds multiple elements by name.

        Args:
            name: The name of the elements to be found.

        Returns:
            A list with elements if any was found. An empty list if not.

        Raises:
            NoSuchElementException - If the element wasn't found.

        Usage:
            elements = driver.find_elements_by_name('foo')
        '''
        return self.find_elements(by=By.NAME, value=name, renew=renew)

    def find_element_by_class(self, class_, renew=False):
        '''Finds an element by class.

        Args:
            class_: The class of the element to be found.

        Returns:
            The element if it was found.

        Raises:
            NoSuchElementException - If the element wasn't found.

        Usage:
            element = driver.find_element_by_class('foo')
        '''
        return self.find_element(by=By.CLASS, value=class_, renew=renew)

    def find_elements_by_class(self, class_, renew=False):
        '''Finds multiple elements by class.

        Args:
            class_: The class of the elements to be found.

        Returns:
            A list with elements if any was found. An empty list if not.

        Raises:
            NoSuchElementException - If the element wasn't found.

        Usage:
            elements = driver.find_elements_by_class('foo')
        '''
        return self.find_elements(by=By.CLASS, value=class_, renew=renew)

    def __repr__(self):
        return '<{0.__module__}.{0.__name__} (device="{1}")>'.format(type(self), self.device_sn)


class AndroidDriver(BaseAndroidDriver):
    '''More utility functions are implemented.

    Controls Android Debug Bridge and allows you to drive the android device.
    '''

    def home(self):
        '''Home button. Go back to Home screen.'''
        self.send_keyevents(Keys.HOME)

    def back(self):
        '''Back button.'''
        self.send_keyevents(Keys.BACK)

    def menu(self):
        '''Menu button. Open the menu or show recent apps tray.'''
        self.send_keyevents(Keys.MENU)

    def switch(self):
        '''Show recent apps tray.'''
        self.send_keyevents(Keys.SWITCH)

    def wake(self):
        '''Wake up screen.'''
        self.send_keyevents(Keys.WAKE)
    
    def lock(self):
        '''Lock screen.'''
        self.send_keyevents(Keys.LOCK)

    def unlock(self, password, width=1080, length=1920):
        '''Unlock screen.'''
        self.wake()
        self.swipe_up(width, length)
        self.send_keys(str(password))

    def power(self):
        '''Power button.'''
        self.send_keyevents(Keys.POWER)

    def brightness_down(self):
        '''Brightness down.'''
        self.send_keyevents(Keys.BRIGHTNESS_DOWN)

    def brightness_up(self):
        '''Brightness up'''
        self.send_keyevents(Keys.BRIGHTNESS_UP)

    def volume_mute(self):
        '''Volume mute.'''
        self.send_keyevents(Keys.VOLUME_MUTE)

    def volume_up(self):
        '''Volume up.'''
        self.send_keyevents(Keys.VOLUME_UP)

    def volume_down(self):
        '''Volume down.'''
        self.send_keyevents(Keys.VOLUME_DOWN)

    def open_browser(self):
        '''Open the system browser.'''
        self.send_keyevents(Keys.BROWSER)

    def open_contacts(self):
        '''Open the system contacts.'''
        self.send_keyevents(Keys.CONTACTS)

    def open_calendar(self):
        '''Open the system calendar.'''
        self.send_keyevents(Keys.CALENDAR)

    def open_calculator(self):
        '''Open the system calculator'''
        self.send_keyevents(Keys.CALCULATOR)
        
    def open_url(self, url='https://www.baidu.com'):
        '''Open a web page with the default browser.'''
        self.app_start_action(Actions.VIEW, '-d', url)

    def launch_app(self, package):
        '''Launch an application.'''
        self.app_start_action(package)

    def make_a_call(self, number=18268237856):
        '''Make a call.'''
        self.app_start_action(Actions.CALL, '-d', 'tel:{}'.format(str(number)))

    def swipe_left(self, width=1080, length=1920):
        '''Swipe left.'''
        self.swipe(0.8*width, 0.5*length, 0.2*width, 0.5*length)

    def swipe_right(self, width=1080, length=1920):
        '''Swipe right.'''
        self.swipe(0.2*width, 0.5*length, 0.8*width, 0.5*length)

    def swipe_up(self, width=1080, length=1920):
        '''Swipe up.'''
        self.swipe(0.5*width, 0.8*length, 0.5*width, 0.2*length)

    def swipe_down(self, width=1080, length=1920):
        '''Swipe down.'''
        self.swipe(0.5*width, 0.2*length, 0.5*width, 0.8*length)
