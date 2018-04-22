import os
import subprocess

from .exceptions import (ApplicationsException, CharactersException,
                         DeviceConnectionException, InvalidPATHException,
                         PackageException, ParametersException,
                         RootPermissionsException, WLANConnectException)


class AndroidDriver(object):
    '''
    Allows you to drive the android device.
    You will need to download the ADB executable from https://github.com/fjwCode/cerium.
    '''

    def __init__(self, executable_path='default', device_sn=None, debug=False, via_wlan=False, host=None, port=None):
        '''
        Cerium requires a driver to with the chosen android device.
        Make sure it's in your PATH, e. g., place it in C:/Anaconda3.
        Or specify the path to the executable.
        Of course, you also can choose the default option.
        '''
        if executable_path in ['adb', 'adb.exe']:
            self.__path = executable_path
            PATH = os.environ['PATH']
            if not ('adb' in PATH or 'android' in PATH):
                raise InvalidPATHException(
                    'PATH does not exist. You will need to download the ADB executable from https://github.com/fjwCode/cerium. Then add to PATH.')
        elif executable_path.endswith('adb.exe'):
            self.__path = executable_path
            if not os.path.isfile(executable_path):
                raise InvalidPATHException(
                    '{!r} does not exist. You will need to download the ADB executable from https://github.com/fjwCode/cerium.'.format(self.__path))
        elif executable_path == 'default':
            self.__path = os.path.join(
                os.path.split(os.path.dirname(__file__))[0],
                'adb', 'adb.exe')
            if not os.path.isfile(self.__path):
                raise InvalidPATHException(
                    '{!r} does not exist. You will need to download the ADB executable from https://github.com/fjwCode/cerium.'.format(self.__path))
        else:
            raise InvalidPATHException(
                'You will need to download the ADB executable from https://github.com/fjwCode/cerium.')
        self.__debug = debug
        self.__start_server()
        self.__target_sn = device_sn
        if via_wlan:
            if host and port:
                self.direct_connect(host, port)
            else:
                raise WLANConnectException('You need input the HOST and PORT.')
        self.__devices = self.devices()
        self.__target()

    def __target(self):
        devices_num = len(self.__devices)
        if devices_num == 0:
            raise DeviceConnectionException(
                'No devices are connected. Please connect the device with USB or via WLAN and turn on the USB debugging option.')
        elif not self.__target_sn and devices_num > 1:
            raise DeviceConnectionException(
                'Multiple devices detected: {}, please specify device serial number or host.'.format(' | '.join(self.__devices)))
        else:
            self.__target_sn = self.__devices[0]

    def __build_command(self, args):
        '''
        build command
        '''
        cmd = [self.__path]
        cmd.extend(args)
        return cmd

    def __run_command(self, *args):
        '''
        execute command
        '''
        process = subprocess.Popen(
            self.__build_command(args),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            encoding='utf-8')
        command = ' '.join(process.args)
        if self.__debug:
            output, error = process.communicate()
            print(
                "Debug Information",
                "Command: {!r}".format(command),
                "Output: {!r}".format(output.encode('utf-8')),
                "Error: {!r}".format(error.encode('utf-8')),
                sep='\n', end='\n{}\n'.format('=' * 80)
            )
        return process.communicate()

    def devices(self):
        '''
        list connected devices
        '''
        output, error = self.__run_command('devices')
        _devices = output.split()[4::2]
        return _devices

    def devices_l(self):
        '''
        list connected devices (-l for long output)
        '''
        output, error = self.__run_command('devices', '-l')
        devices = output.split()[4::6]
        models = output.split()[7::6]
        return dict(zip(devices, models))

    def __start_server(self):
        '''
        ensure that there is a server running
        '''
        self.__run_command('start-server')

    def kill_server(self):
        '''
        kill the server if it is running
        '''
        self.__run_command('kill-server')

    def restart_server(self):
        '''
        restart the server if it is running
        '''
        self.kill_server()
        self.__start_server()

    def version(self):
        '''
        show version num
        '''
        output, error = self.__run_command('version')
        return output.splitlines()[0].split()[-1]

    def model(self):
        '''
        show model
        '''
        output, error = self.__run_command('-s', self.__target_sn, 'shell',
                                           'getprop', 'ro.product.model')
        return output.strip()

    def battery(self):
        '''
        show model
        '''
        output, error = self.__run_command('-s', self.__target_sn, 'shell',
                                           'dumpsys', 'battery')
        return output

    def physical_size(self):
        '''
        show physical size
        '''
        output, error = self.__run_command('-s', self.__target_sn, 'shell',
                                           'wm', 'size')
        return output.split()[2]

    def density(self):
        '''
        show density
        '''
        output, error = self.__run_command('-s', self.__target_sn, 'shell',
                                           'wm', 'density')
        return output.split()[2]

    def displays(self):
        '''
        show displays parameters
        '''
        output, error = self.__run_command(
            '-s', self.__target_sn, 'shell', 'dumpsys', 'window', 'displays')
        return output

    def android_id(self):
        '''
        show android id
        '''
        output, error = self.__run_command(
            '-s', self.__target_sn, 'shell', 'settings', 'get', 'secure', 'android_id')
        return output.strip()

    def android_version(self):
        '''
        show android version
        '''
        output, error = self.__run_command(
            '-s', self.__target_sn, 'shell', 'getprop', 'ro.build.version.release')
        return output.strip()

    def device_mac(self):
        '''
        show device mac
        '''
        output, error = self.__run_command(
            '-s', self.__target_sn, 'shell', 'cat', '/sys/class/net/wlan0/address')
        return output.strip()

    def device_cpu(self):
        '''
        show device CPU info
        '''
        output, error = self.__run_command(
            '-s', self.__target_sn, 'shell', 'cat', '/proc/cpuinfo')
        return output

    def device_memory(self):
        '''
        show device memory
        '''
        output, error = self.__run_command(
            '-s', self.__target_sn, 'shell', 'cat', '/proc/meminfo')
        return output

    def root(self):
        '''
        restart adbd with root permissions
        '''
        output, error = self.__run_command('root')
        if not output:
            raise RootPermissionsException(
                '{!r} does not have root permission.'.format(self.__target_sn))

    def unroot(self):
        '''
        restart adbd without root permissions
        '''
        self.__run_command('unroot')

    def connect(self, port=5555):
        '''
        connect to a device via TCP/IP
        '''
        host = self.__wlan_address()
        self.__target_sn = '{}:{}'.format(host, port)
        # restart adb server listening on TCP on PORT
        self.__run_command('tcpip', str(port))
        self.__run_command('connect', self.__target_sn)
        print('Now you can unplug the USB cable, and control your device via WLAN.')

    def direct_connect(self, host='192.168.0.3', port=5555):
        '''
        connect to a device via TCP/IP directly
        '''
        self.__target_sn = '{}:{}'.format(host, port)
        self.__run_command('connect', self.__target_sn)

    def disconnect(self, host='192.168.0.3', port=5555):
        '''
        disconnect from given TCP/IP device [default port=5555], or all
        '''
        pass

    def __wlan_address(self) -> str:
        '''
        show WLAN IP Address
        '''
        output, error = self.__run_command('-s', self.__target_sn,
                                           'shell', 'ip', '-f', 'inet', 'addr', 'show', 'wlan0')
        import re
        wlan_address = re.findall(
            r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b", output)
        if not wlan_address:
            raise WLANConnectException('The device is not connected to WLAN.')
        return wlan_address[0]

    def push(self, local='LICENSE', remote='/sdcard/LICENSE'):
        '''
        copy local files/directories to device
        '''
        if not os.path.exists(local):
            raise InvalidPATHException(
                'Local path {!r} does not exist.'.format(local))
        self.__run_command('-s', self.__target_sn,
                           'push', local, remote)

    def push_sync(self, local='LICENSE', remote='/sdcard/LICENSE'):
        '''
        only push files that are newer on the host than the device
        '''
        if not os.path.exists(local):
            raise InvalidPATHException(
                'Local path {!r} does not exist.'.format(local))
        self.__run_command('-s', self.__target_sn,
                           'push', '--sync', local, remote)

    def pull(self, remote, local):
        '''
        copy files/directories from device
        '''
        output, error = self.__run_command('-s', self.__target_sn,
                                           'pull', remote, local)
        if 'error' in output:
            raise InvalidPATHException(
                'Remote path {!r} does not exist.'.format(remote))

    def pull_a(self, remote, local):
        '''
        copy files/directories from device, and preserve file timestamp and mode
        '''
        output, error = self.__run_command('-s', self.__target_sn,
                                           'pull', '-a', remote, local)
        if 'error' in output:
            raise InvalidPATHException(
                'Remote path {!r} does not exist.'.format(remote))

    def sync(self, option='all'):
        '''
        sync a local build from $ANDROID_PRODUCT_OUT to the device (default all)
        '''
        if option in ['system', 'vendor', 'oem', 'data', 'all']:
            self.__run_command('-s', self.__target_sn,
                               'sync', option)
        else:
            raise ParametersException(
                'There is no option named: {!r}.'.format(option))

    def sync_l(self, option='all'):
        '''
        list but don't copy
        '''
        if option in ['system', 'vendor', 'oem', 'data', 'all']:
            self.__run_command('-s', self.__target_sn,
                               'sync', '-l', option)
        else:
            raise ParametersException(
                'There is no option named: {!r}.'.format(option))

    # Application Management
    def install(self, package: str, option='-r'):
        '''
        push package to the device and install it
        -l: forward lock application
        -r: replace existing application
        -t: allow test packages
        -s: install application on sdcard
        -d: allow version code downgrade (debuggable packages only)
        -g: grant all runtime permissions
        '''
        if not os.path.isfile(package):
            raise InvalidPATHException(
                '{!r} does not exist.'.format(self.__path))
        for i in option:
            if i not in '-lrtsdg':
                raise ParametersException(
                    'There is no option named: {!r}.'.format(option))
        self.__run_command('-s', self.__target_sn,
                           'install', option, package)

    def install_multiple(self, *packages, option='-r'):
        '''
        push packages to the device and install them
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
                raise InvalidPATHException(
                    '{!r} does not exist.'.format(self.__path))
        for i in option:
            if i not in '-lrtsdpg':
                raise ParametersException(
                    'There is no option called {!r}.'.format(option))
        self.__run_command('-s', self.__target_sn,
                           'install-multiple', option, *packages)

    def uninstall(self, package):
        '''
        remove this app package from the device
        '''
        if package not in self.shell_pm_list_packages():
            raise PackageException(
                'There is no package called {!r}.'.format(package))
        self.__run_command('-s', self.__target_sn, 'uninstall', package)

    def uninstall_k(self, package):
        '''
        remove this app package from the device, and keep the data and cache directories
        '''
        if package not in self.shell_pm_list_packages():
            raise PackageException(
                'There is no package called {!r}.'.format(package))
        self.__run_command('-s', self.__target_sn, 'uninstall', '-k', package)

    def shell_pm_list_packages(self, option='-e'):
        '''
        show all packages
        -f see their associated file
        -d filter to only show disabled packages
        -e filter to only show enabled packages
        -s filter to only show system packages
        -3 filter to only show third party packages
        -i see the installer for the packages
        -u also include uninstalled packages

        '''
        if option not in ['-f', '-d', '-e', '-s', '-3', '-i', '-u']:
            raise ParametersException(
                'There is no option called {!r}.'.format(option))
        output, error = self.__run_command('-s', self.__target_sn,
                                           'shell', 'pm', 'list', 'packages', option)
        return list(map(lambda x: x[8:], output.splitlines()))

    def shell_pm_path(self, package):
        '''
        print the path to the APK of the given
        '''
        if package not in self.shell_pm_list_packages():
            raise PackageException(
                'There is no package called {!r}.'.format(package))
        output, error = self.__run_command('-s', self.__target_sn,
                                           'shell', 'pm', 'path', package)
        return output[8:-1]

    def shell_pm_clear(self, package):
        '''
        deletes all data associated with a package
        '''
        if package not in self.shell_pm_list_packages():
            raise PackageException(
                'There is no package called {!r}.'.format(package))
        self.__run_command('-s', self.__target_sn,
                           'shell', 'pm', 'clear', package)

    def shell_dumpsys_activity_focused_activity(self):
        '''
        view reception activity
        '''
        output, error = self.__run_command('-s', self.__target_sn,
                                           'shell', 'dumpsys', 'activity', 'activities', '|', 'grep', 'mFocusedActivity')
        return output.strip()

    def shell_dumpsys_activity_services(self, package=''):
        '''
        view running services
        '''
        output, error = self.__run_command('-s', self.__target_sn,
                                           'shell', 'dumpsys', 'activity', 'services', package)
        return output

    def shell_dumpsys_package(self, package=''):
        '''
        query package detail information
        '''
        output, error = self.__run_command('-s', self.__target_sn,
                                           'shell', 'dumpsys', 'package', package)
        return output

    def shell_dumpsys_windows_current(self):
        '''
        get current application behavior
        '''
        output, error = self.__run_command('-s', self.__target_sn,
                                           'shell', 'dumpsys', 'window', 'windows', '|', 'findstr', '"Current"')
        return output

    # Interact with Applications
    def shell_am_start(self, *args):
        '''
        -a <ACTION>
        -c <CATEGORY>
        -n <COMPONENT>
        for example:
            from cerium import AndroidDriver
            driver = AndroidDriver()
            driver.shell_am_start('-n', 'com.tencent.android.qqdownloader/com.tencent.assistantv2.activity.MainActivity')
        '''
        output, error = self.__run_command('-s', self.__target_sn, 'shell',
                                           'am', 'start', *args)
        if error and error.startswith('Error'):
            raise ApplicationsException(error.split(':', 1)[-1].strip())

    def shell_am_startservice(self, *args):
        '''
        start a service
        '''
        output, error = self.__run_command('-s', self.__target_sn, 'shell',
                                           'am', 'startservice', *args)
        if error and error.startswith('Error'):
            raise ApplicationsException(error.split(':', 1)[-1].strip())

    def shell_am_stopservice(self, *args):
        '''
        start a service
        '''
        output, error = self.__run_command('-s', self.__target_sn, 'shell',
                                           'am', 'stopservice', *args)
        if error and error.startswith('Error'):
            raise ApplicationsException(error.split(':', 1)[-1].strip())

    def shell_am_broadcast(self, *args):
        '''
        send a broadcast
        '''
        output, error = self.__run_command('-s', self.__target_sn, 'shell',
                                           'am', 'broadcast', *args)
        if error:
            raise ApplicationsException(error.split(':', 1)[-1].strip())

    def shell_am_force_stop(self, package):
        '''
        force stop an application
        '''
        self.__run_command('-s', self.__target_sn, 'shell',
                           'am', 'force-stop', package)

    def shell_am_send_trim_memory(self, pid: int, level='RUNNING_LOW'):
        '''
        trim memory
        -level: HIDDEN、RUNNING_MODERATE、BACKGROUND、 RUNNING_LOW、MODERATE、RUNNING_CRITICAL、COMPLETE
        '''
        output, error = self.__run_command('-s', self.__target_sn, 'shell',
                                           'am', 'send-trim-memory', str(pid), level)
        if error and error.startswith('Error'):
            raise ApplicationsException(error.split(':', 1)[-1].strip())

    def screencap(self, filename='/sdcard/screencap.png'):
        '''
        taking a screenshot of a device display
        '''
        self.__run_command('-s', self.__target_sn, 'shell',
                           'screencap', '-p', filename)

    def pull_screencap(self, remote='/sdcard/screencap.png', local='screencap.png'):
        '''
        taking a screenshot of a device display, then copy it to your computer
        '''
        self.screencap(remote)
        self.pull(remote, local)

    def screencap_exec(self, save_as='screencap.png'):
        '''
        taking a screenshot of a device display, then copy it to your computer
        '''
        self.__run_command('-s', self.__target_sn, 'exec-out',
                           'screencap', '-p', '>', save_as)

    def screenrecord(self, bit_rate: int = 5000000, time_limit: int = 180, filename='/sdcard/demo.mp4'):
        '''
        recording the display of devices running Android 4.4 (API level 19) and higher
        bit_rate: you can increase the bit rate to improve video quality, but doing so results in larger movie files
        time_limit: sets the maximum recording time, in seconds, and the maximum value is 180 (3 minutes)
        '''
        self.__run_command('-s', self.__target_sn, 'shell',
                           'screenrecord', '--bit-rate', str(bit_rate), '--time-limit', str(time_limit), filename)

    def pull_screenrecord(self, bit_rate: int = 5000000, time_limit: int = 180, remote='/sdcard/demo.mp4', local='demo.mp4'):
        '''
        recording the display of devices running Android 4.4 (API level 19) and higher
        bit_rate: you can increase the bit rate to improve video quality, but doing so results in larger movie files
        time_limit: sets the maximum recording time, in seconds, and the maximum value is 180 (3 minutes)
        '''
        self.screenrecord(bit_rate, time_limit, filename=remote)
        self.pull(remote, local)

    def input_tap(self, x, y):
        '''
        simulate finger click
        '''
        self.__run_command('-s', self.__target_sn, 'shell',
                           'input', 'tap', str(x), str(y))

    def input_swipe(self, x1, y1, x2, y2, duration=100):
        '''
        simulate finger slide
        '''
        self.__run_command('-s', self.__target_sn, 'shell',
                           'input', 'swipe', str(x1), str(y1), str(x2), str(y2), str(duration))

    def input_text(self, text: str = 'cerium'):
        '''
        input text
        '''
        for char in text:
            if '\u4e00' <= char <= '\u9fff':
                raise CharactersException(
                    'Text cannot contain non-English characters, such as {!r}.'.format(char))
        text = text.replace(' ', '\ ')
        self.__run_command('-s', self.__target_sn, 'shell',
                           'input', 'text', text)

    def input_keyevent(self, keyevent: int or str):
        '''
        input keyevent
        '''
        self.__run_command('-s', self.__target_sn, 'shell',
                           'input', 'keyevent', str(keyevent))

    def monkey(self, package, v=500):
        pass

    def reboot(self, mode=''):
        '''
        reboot the device;
        defaults to booting system image but supports bootloader and recovery too.
        '''
        ['recovery', 'bootloader']
        self.__run_command('-s', self.__target_sn, 'reboot', mode)

    def __enter__(self, *arg):
        return self

    def __exit__(self, *arg):
        self.kill_server()
