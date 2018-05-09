# Licensed to the White Turing under one or more
# contributor license agreements.  See the NOTICE file
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
from .service import _PATH, Service
from .utils import merge_dict


class BaseAndroidDriver(Service):
    '''Controls Android Debug Bridge and allows you to drive the android device.'''

    _element_cls = Elements
    _temp = os.path.join(tempfile.gettempdir(), 'uidump.xml')
    _nodes = None

    def __init__(self, executable_path: _PATH = 'default', device_sn: str = None, wireless: bool = False, host: str = '192.168.0.3', port: str or int = 5555, service_port: str or int =5037, env: dict = None, service_args: list or tuple = None, dev: bool = False) -> None:
        '''Creates a new instance of the android driver.

        Starts the service and then creates new instance of android driver.

        Args:
            executable_path: Path to the executable. The default uses its own executable.
            device_sn: Device serial number.
            wireless/host/port: If wireless is True, will connect your device via WLAN driectly.
                                         The premise is that your device has opened the port and
                                         you know the device's IP address.
            service_port: Service port you would like the service to run,
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

    def _detect_devices(self) -> None:
        '''Detect whether devices connected.'''
        devices_num = len(self.devices_list)
        if devices_num == 0:
            raise DeviceConnectionException(
                'No devices are connected. Please connect the device with USB or via WLAN and turn on the USB debugging option.')
        elif not self.device_sn and devices_num > 1:
            raise DeviceConnectionException(
                f"Multiple devices detected: {' | '.join(self.devices_list)}, please specify device serial number or host.")
        else:
            self.device_sn = self.devices_list[0]
        if self.get_state() == 'offline':
            raise DeviceConnectionException(
                'The device is offline. Please reconnect.')

    def start_server(self) -> None:
        '''Start server.'''
        self.start()

    def kill_server(self) -> None:
        '''Kill the server if it is running.'''
        self.stop()

    def restart_server(self) -> None:
        '''Restart the server if it is running.'''
        self.restart()

    def _execute(self, *args: str, **kwargs) -> tuple:
        '''Execute command.'''
        process = self.execute(
            args=args, options=merge_dict(self.options, kwargs))
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
    @property
    def serial_number(self) -> str:
        '''Show device serial number.'''
        return self.device_sn

    @classmethod
    def serial_matcher(cls, serial) -> bool:
        """Returns a device matcher for the given serial."""
        return lambda device: device.serial_number == serial

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

    def root(self) -> None:
        '''Restart adbd with root permissions.'''
        output, _ = self._execute('-s', self.device_sn, 'root')
        if not output:
            raise PermissionError(
                f'{self.device_sn!r} does not have root permission.')

    def unroot(self) -> None:
        '''Restart adbd without root permissions.'''
        self._execute('-s', self.device_sn, 'unroot')

    def tcpip(self, port: int or str = 5555) -> None:
        '''Restart adb server listening on TCP on PORT.'''
        self._execute('-s', self.device_sn, 'tcpip', str(port))

    def get_ip_addr(self) -> str:
        '''Show IP Address.'''
        output, _ = self._execute(
            '-s', self.device_sn, 'shell', 'ip', '-f', 'inet', 'addr', 'show', 'wlan0')
        ip_addr = re.findall(
            r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b", output)
        if not ip_addr:
            raise ConnectionError(
                'The device is not connected to WLAN or not connected via USB.')
        return ip_addr[0]

    def auto_connect(self, port: int or str =5555) -> None:
        '''Connect to a device via TCP/IP automatically.'''
        host = self.get_ip_addr()
        self.tcpip(port)
        self.connect(host, port)
        print('Now you can unplug the USB cable, and control your device via WLAN.')

    def push(self, local: _PATH = 'LICENSE', remote: _PATH = '/sdcard/LICENSE') -> None:
        '''Copy local files/directories to device.'''
        if not os.path.exists(local):
            raise FileNotFoundError(f'Local {local!r} does not exist.')
        self._execute('-s', self.device_sn, 'push', local, remote)

    def push_sync(self, local: _PATH = 'LICENSE', remote: _PATH = '/sdcard/LICENSE') -> None:
        '''Only push files that are newer on the host than the device.'''
        if not os.path.exists(local):
            raise FileNotFoundError(f'Local {local!r} does not exist.')
        self._execute('-s', self.device_sn, 'push', '--sync', local, remote)

    def pull(self, remote: _PATH, local: _PATH) -> None:
        '''Copy files/directories from device.'''
        output, _ = self._execute('-s', self.device_sn, 'pull', remote, local)
        if 'error' in output:
            raise FileNotFoundError(f'Remote {remote!r} does not exist.')

    def pull_a(self, remote: _PATH, local: _PATH) -> None:
        '''Copy files/directories from device, and preserve file timestamp and mode.'''
        output, _ = self._execute(
            '-s', self.device_sn, 'pull', '-a', remote, local)
        if 'error' in output:
            raise FileNotFoundError(f'Remote {remote!r} does not exist.')

    def sync(self, option: str = 'all') -> None:
        '''Sync a local build from $ANDROID_PRODUCT_OUT to the device (default all).

        Args:
            option: 'system', 'vendor', 'oem', 'data', 'all'
        '''
        if option in ['system', 'vendor', 'oem', 'data', 'all']:
            self._execute('-s', self.device_sn, 'sync', option)
        else:
            raise ValueError(f'There is no option named: {option!r}.')

    def sync_l(self, option: str = 'all') -> None:
        '''List but don't copy.

        Args:
            option: 'system', 'vendor', 'oem', 'data', 'all'
        '''
        if option in ['system', 'vendor', 'oem', 'data', 'all']:
            self._execute('-s', self.device_sn, 'sync', '-l', option)
        else:
            raise ValueError('There is no option named: {!r}.'.format(option))

    # Application Management
    def install(self, package: str, option: str = '-r') -> None:
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
            raise FileNotFoundError(f'{package!r} does not exist.')
        for i in option:
            if i not in '-lrtsdg':
                raise ValueError(f'There is no option named: {option!r}.')
        self._execute('-s', self.device_sn, 'install', option, package)

    def install_multiple(self, *packages, option: str = '-r') -> None:
        '''Push packages to the device and install them.

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
                raise FileNotFoundError(f'{package!r} does not exist.')
        for i in option:
            if i not in '-lrtsdpg':
                raise ValueError(f'There is no option named: {option!r}.')
        self._execute('-s', self.device_sn,
                      'install-multiple', option, *packages)

    def uninstall(self, package: str) -> None:
        '''Remove this app package from the device.'''
        if package not in self.view_packgets_list():
            raise NoSuchPackageException(
                f'There is no such package {package!r}.')
        self._execute('-s', self.device_sn, 'uninstall', package)

    def uninstall_k(self, package: str) -> None:
        '''Remove this app package from the device, and keep the data and cache directories.'''
        if package not in self.view_packgets_list():
            raise NoSuchPackageException(
                f'There is no such package {package!r}.')
        self._execute('-s', self.device_sn, 'uninstall', '-k', package)

    def view_packgets_list(self, option: str = '-e', keyword: str = '') -> list:
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
            raise ValueError(f'There is no option called {option!r}.')
        output, _ = self._execute(
            '-s', self.device_sn, 'shell', 'pm', 'list', 'packages', option, keyword)
        return list(map(lambda x: x[8:], output.splitlines()))

    def view_package_path(self, package: str) -> _PATH:
        '''Print the path to the APK of the given.'''
        if package not in self.view_packgets_list():
            raise NoSuchPackageException(
                f'There is no such package {package!r}.')
        output, _ = self._execute(
            '-s', self.device_sn, 'shell', 'pm', 'path', package)
        return output[8:-1]

    def clear_app_data(self, package: str) -> None:
        '''Deletes all data associated with a package.'''
        if package not in self.view_packgets_list():
            raise NoSuchPackageException(
                f'There is no such package {package!r}.')
        self._execute('-s', self.device_sn, 'shell', 'pm', 'clear', package)

    def view_focused_activity(self) -> str:
        '''View focused activity.'''
        output, _ = self._execute(
            '-s', self.device_sn, 'shell', 'dumpsys', 'activity', 'activities')
        return re.findall(r'mFocusedActivity: .+(com[a-zA-Z0-9\.]+/.[a-zA-Z0-9\.]+)', output)[0]

    def view_running_services(self, package: str='') -> str:
        '''View running services.'''
        output, _ = self._execute(
            '-s', self.device_sn, 'shell', 'dumpsys', 'activity', 'services', package)
        return output

    def view_package_info(self, package: str='') -> str:
        '''View package detail information.'''
        output, _ = self._execute(
            '-s', self.device_sn, 'shell', 'dumpsys', 'package', package)
        return output

    def view_current_app_behavior(self) -> str:
        '''View application behavior in the current window.'''
        output, _ = self._execute(
            '-s', self.device_sn, 'shell', 'dumpsys', 'window', 'windows')
        return re.findall(r'mCurrentFocus=.+(com[a-zA-Z0-9\.]+/.[a-zA-Z0-9\.]+)', output)[0]

    def view_surface_app_activity(self) -> str:
        '''Get package with activity of applications that are running in the foreground.'''
        output, error = self._execute(
            '-s', self.device_sn, 'shell', 'dumpsys', 'window', 'w')
        return re.findall(r"name=([a-zA-Z0-9\.]+/.[a-zA-Z0-9\.]+)", output)

    # Interact with Applications
    def _app_base_start(self, option: str, args: list or tuple) -> None:
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

    def app_start_action(self, *args) -> None:
        '''Start action.'''
        self._app_base_start('-a', args)

    def app_start_category(self, *args) -> None:
        '''Start category.'''
        self._app_base_start('-c', args)

    def app_start_activity(self, *args) -> None:
        '''Start activity.'''
        self._app_base_start('-n', args)

    def app_start_service(self, *args) -> None:
        '''Start a service.'''
        _, error = self._execute('-s', self.device_sn,
                                 'shell', 'am', 'startservice', *args)
        if error and error.startswith('Error'):
            raise ApplicationsException(error.split(':', 1)[-1].strip())

    def app_stop_service(self, *args) -> None:
        '''Stop a service'''
        _, error = self._execute('-s', self.device_sn, 'shell',
                                 'am', 'stopservice', *args)
        if error and error.startswith('Error'):
            raise ApplicationsException(error.split(':', 1)[-1].strip())

    def app_broadcast(self, *args) -> None:
        '''Send a broadcast.'''
        _, error = self._execute('-s', self.device_sn, 'shell',
                                 'am', 'broadcast', *args)
        if error:
            raise ApplicationsException(error.split(':', 1)[-1].strip())

    def close_app(self, package: str) -> None:
        '''Close an application.'''
        self._execute('-s', self.device_sn, 'shell',
                      'am', 'force-stop', package)

    def app_trim_memory(self, pid: int or str, level: str = 'RUNNING_LOW') -> None:
        '''Trim memory.

        Args:
            level: HIDDEN | RUNNING_MODERATE | BACKGROUNDRUNNING_LOW | \
                     MODERATE | RUNNING_CRITICAL | COMPLETE
        '''
        _, error = self._execute('-s', self.device_sn, 'shell',
                                 'am', 'send-trim-memory', str(pid), level)
        if error and error.startswith('Error'):
            raise ApplicationsException(error.split(':', 1)[-1].strip())

    def app_start_up_time(self, package: str) -> str:
        '''Get the time it took to launch your application.'''
        output, _ = self._execute(
            '-s', self.device_sn, 'shell', 'am', 'start', '-W', package)
        return re.findall('TotalTime: \d+', output)[0]

    def screencap(self, filename: _PATH='/sdcard/screencap.png') -> None:
        '''Taking a screenshot of a device display.'''
        self._execute('-s', self.device_sn, 'shell',
                      'screencap', '-p', filename)

    def pull_screencap(self, remote: _PATH = '/sdcard/screencap.png', local: _PATH = 'screencap.png') -> None:
        '''Taking a screenshot of a device display, then copy it to your computer.'''
        self.screencap(remote)
        self.pull(remote, local)

    def screencap_exec(self, filename: _PATH = 'screencap.png') -> None:
        '''Taking a screenshot of a device display, then copy it to your computer.'''
        self._execute('-s', self.device_sn, 'exec-out',
                      'screencap', '-p', '>', filename, shell=True)

    def screenrecord(self, bit_rate: int = 5000000, time_limit: int = 180, filename: _PATH = '/sdcard/demo.mp4') -> None:
        '''Recording the display of devices running Android 4.4 (API level 19) and higher.

        Args:
            bit_rate:You can increase the bit rate to improve video quality, but doing so results in larger movie files.
            time_limit: Sets the maximum recording time, in seconds, and the maximum value is 180 (3 minutes).
        '''
        self._execute('-s', self.device_sn, 'shell',
                      'screenrecord', '--bit-rate', str(bit_rate), '--time-limit', str(time_limit), filename)

    def pull_screenrecord(self, bit_rate: int = 5000000, time_limit: int = 180, remote: _PATH = '/sdcard/demo.mp4', local: _PATH = 'demo.mp4') -> None:
        '''Recording the display of devices running Android 4.4 (API level 19) and higher. Then copy it to your computer.

        Args:
            bit_rate:You can increase the bit rate to improve video quality, but doing so results in larger movie files.
            time_limit: Sets the maximum recording time, in seconds, and the maximum value is 180 (3 minutes).
        '''
        self.screenrecord(bit_rate, time_limit, filename=remote)
        self.pull(remote, local)

    def click(self, x: int, y: int) -> None:
        '''Simulate finger click.'''
        self._execute('-s', self.device_sn, 'shell',
                      'input', 'tap', str(x), str(y))

    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration: int = 100) -> None:
        '''Simulate finger swipe.'''
        self._execute('-s', self.device_sn, 'shell',
                      'input', 'swipe', str(x1), str(y1), str(x2), str(y2), str(duration))

    def send_keys(self, text: str = 'cerium') -> None:
        '''Simulates typing keys.'''
        for char in text:
            if '\u4e00' <= char <= '\u9fff':
                raise CharactersException(
                    f'Text cannot contain non-English characters, such as {char!r}.')
        text = re.escape(text)
        self._execute('-s', self.device_sn, 'shell',
                      'input', 'text', text)

    def send_keyevents(self, keyevent: int) -> None:
        '''Simulates typing keyevents.'''
        self._execute('-s', self.device_sn, 'shell',
                      'input', 'keyevent', str(keyevent))

    def send_keyevents_long_press(self, keyevent: int) -> None:
        '''Simulates typing keyevents long press.'''
        self._execute('-s', self.device_sn, 'shell',
                      'input', 'keyevent', '--longpress', str(keyevent))

    def send_monkey(self, *args) -> None:
        '''Generate pseudo-random user events to simulate clicks, touches, gestures, etc.'''
        self._execute('-s', self.device_sn, 'shell', 'monkey', *args)

    def reboot(self) -> None:
        '''Reboot the device.'''
        self._execute('-s', self.device_sn, 'reboot')

    def recovery(self) -> None:
        '''Reboot to recovery mode.'''
        self._execute('-s', self.device_sn, 'reboot', 'recovery')

    def fastboot(self) -> None:
        '''Reboot to bootloader mode.'''
        self._execute('-s', self.device_sn, 'reboot', 'bootloader')

    def uidump(self, local: _PATH = None) -> None:
        '''Get the current interface layout file.'''
        local = local if local else self._temp
        self._execute('-s', self.device_sn, 'shell', 'uiautomator',
                      'dump', '--compressed', '/data/local/tmp/uidump.xml')
        self.pull('/data/local/tmp/uidump.xml', local)
        ui = html.fromstring(open(local, 'rb').read())
        self._nodes = ui.iter(tag="node")

    def find_element(self, value, by=By.ID, update=False) -> Elements:
        '''Find a element or the first element.'''
        if update or not self._nodes:
            self.uidump()
        for node in self._nodes:
            if node.attrib[by] == value:
                bounds = node.attrib['bounds']
                coord = list(map(int, re.findall(r'\d+', bounds)))
                click_point = (coord[0] + coord[2]) / \
                    2, (coord[1] + coord[3]) / 2
                return self._element_cls(self, node.attrib, by, value, coord, click_point)
        raise NoSuchElementException(f'No such element: {by}={value!r}.')

    def find_elements(self, value, by=By.ID, update=False) -> Elements:
        '''Find all elements.'''
        elements = []
        if update or not self._nodes:
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
        raise NoSuchElementException(f'No such element: {by}={value!r}.')

    def find_element_by_id(self, id_, update=False) -> Elements:
        '''Finds an element by id.

        Args:
            id_: The id of the element to be found.
            update: If the interface has changed, this option should be True.

        Returns:
            The element if it was found.

        Raises:
            NoSuchElementException - If the element wasn't found.

        Usage:
            element = driver.find_element_by_id('foo')
        '''
        return self.find_element(by=By.ID, value=id_, update=update)

    def find_elements_by_id(self, id_, update=False) -> Elements:
        '''Finds multiple elements by id.

        Args:
            id_: The id of the elements to be found.
            update: If the interface has changed, this option should be True.

        Returns:
            A list with elements if any was found. An empty list if not.

        Raises:
            NoSuchElementException - If the element wasn't found.

        Usage:
            elements = driver.find_elements_by_id('foo')
        '''
        return self.find_elements(by=By.ID, value=id_, update=update)

    def find_element_by_name(self, name, update=False) -> Elements:
        '''Finds an element by name.

        Args:
            name: The name of the element to be found.
            update: If the interface has changed, this option should be True.

        Returns:
            The element if it was found.

        Raises:
            NoSuchElementException - If the element wasn't found.

        Usage:
            element = driver.find_element_by_name('foo')
        '''
        return self.find_element(by=By.NAME, value=name, update=update)

    def find_elements_by_name(self, name, update=False) -> Elements:
        '''Finds multiple elements by name.

        Args:
            name: The name of the elements to be found.
            update: If the interface has changed, this option should be True.

        Returns:
            A list with elements if any was found. An empty list if not.

        Raises:
            NoSuchElementException - If the element wasn't found.

        Usage:
            elements = driver.find_elements_by_name('foo')
        '''
        return self.find_elements(by=By.NAME, value=name, update=update)

    def find_element_by_class(self, class_, update=False) -> Elements:
        '''Finds an element by class.

        Args:
            class_: The class of the element to be found.
            update: If the interface has changed, this option should be True.

        Returns:
            The element if it was found.

        Raises:
            NoSuchElementException - If the element wasn't found.

        Usage:
            element = driver.find_element_by_class('foo')
        '''
        return self.find_element(by=By.CLASS, value=class_, update=update)

    def find_elements_by_class(self, class_, update=False) -> Elements:
        '''Finds multiple elements by class.

        Args:
            class_: The class of the elements to be found.
            update: If the interface has changed, this option should be True.

        Returns:
            A list with elements if any was found. An empty list if not.

        Raises:
            NoSuchElementException - If the element wasn't found.

        Usage:
            elements = driver.find_elements_by_class('foo')
        '''
        return self.find_elements(by=By.CLASS, value=class_, update=update)

    def __repr__(self):
        return '<{0.__module__}.{0.__name__} (device="{1}")>'.format(type(self), self.device_sn)


class AndroidDriver(BaseAndroidDriver):
    '''More utility functions are implemented.

    Controls Android Debug Bridge and allows you to drive the android device.
    '''

    def home(self) -> None:
        '''Home button. Go back to Home screen.'''
        self.send_keyevents(Keys.HOME)

    def back(self) -> None:
        '''Back button.'''
        self.send_keyevents(Keys.BACK)

    def menu(self) -> None:
        '''Menu button. Open the menu or show recent apps tray.'''
        self.send_keyevents(Keys.MENU)

    def switch(self) -> None:
        '''Show recent apps tray.'''
        self.send_keyevents(Keys.SWITCH)

    def wake(self) -> None:
        '''Wake up screen.'''
        self.send_keyevents(Keys.WAKE)

    def lock(self) -> None:
        '''Lock screen.'''
        self.send_keyevents(Keys.LOCK)

    def unlock(self, password, width=1080, length=1920) -> None:
        '''Unlock screen.'''
        self.wake()
        self.swipe_up(width, length)
        self.send_keys(str(password))

    def power(self) -> None:
        '''Power button.'''
        self.send_keyevents(Keys.POWER)

    def brightness_down(self) -> None:
        '''Brightness down.'''
        self.send_keyevents(Keys.BRIGHTNESS_DOWN)

    def brightness_up(self) -> None:
        '''Brightness up'''
        self.send_keyevents(Keys.BRIGHTNESS_UP)

    def volume_mute(self) -> None:
        '''Volume mute.'''
        self.send_keyevents(Keys.VOLUME_MUTE)

    def volume_up(self) -> None:
        '''Volume up.'''
        self.send_keyevents(Keys.VOLUME_UP)

    def volume_down(self) -> None:
        '''Volume down.'''
        self.send_keyevents(Keys.VOLUME_DOWN)

    def open_browser(self) -> None:
        '''Open the system browser.'''
        self.send_keyevents(Keys.BROWSER)

    def open_contacts(self) -> None:
        '''Open the system contacts.'''
        self.send_keyevents(Keys.CONTACTS)

    def open_calendar(self) -> None:
        '''Open the system calendar.'''
        self.send_keyevents(Keys.CALENDAR)

    def open_calculator(self) -> None:
        '''Open the system calculator'''
        self.send_keyevents(Keys.CALCULATOR)

    def open_url(self, url: str = 'https://www.baidu.com') -> None:
        '''Open a web page with the default browser.'''
        self.app_start_action(Actions.VIEW, '-d', url)

    def launch_app(self, package) -> None:
        '''Launch an application.'''
        self.app_start_activity(package)

    def make_a_call(self, number: int or str = 18268237856) -> None:
        '''Make a call.'''
        self.app_start_action(Actions.CALL, '-d', 'tel:{}'.format(str(number)))

    def end_the_call(self) -> None:
        '''End the current call.'''
        self.send_keyevents(Keys.ENDCALL)

    def swipe_left(self, width: int = 1080, length: int = 1920) -> None:
        '''Swipe left.'''
        self.swipe(0.8*width, 0.5*length, 0.2*width, 0.5*length)

    def swipe_right(self, width: int = 1080, length: int = 1920) -> None:
        '''Swipe right.'''
        self.swipe(0.2*width, 0.5*length, 0.8*width, 0.5*length)

    def swipe_up(self, width: int = 1080, length: int = 1920) -> None:
        '''Swipe up.'''
        self.swipe(0.5*width, 0.8*length, 0.5*width, 0.2*length)

    def swipe_down(self, width: int = 1080, length: int = 1920) -> None:
        '''Swipe down.'''
        self.swipe(0.5*width, 0.2*length, 0.5*width, 0.8*length)
