import os
import subprocess

from .exceptions import DeviceConnectionException, InvalidPATHException


class AndroidDriver(object):
    '''
    Allows you to drive the android device.
    You will need to download the ADB executable from https://github.com/fjwCode/cerium.
    '''
    def __init__(self, executable_path='adb', device_sn=None, debug=False):
        if executable_path in ['adb', 'adb.exe']:
            self.__path = executable_path
            PATH = os.environ['PATH']
            if not ('adb' in PATH or 'android' in PATH):
                raise InvalidPATHException('PATH does not exist. You will need to download the ADB executable from https://github.com/fjwCode/cerium. Then add to PATH.')
        elif executable_path.endswith('adb.exe'):
            self.__path = executable_path
            if not os.path.isfile(executable_path):
                raise InvalidPATHException(
                    '{!r} does not exist. You will need to download the ADB executable from https://github.com/fjwCode/cerium.'.format(self.__path))
        else:
            self.__path = os.path.join(
                os.path.split(os.path.dirname(__file__))[0],
                'adb', 'adb.exe')
            if not os.path.isfile(self.__path):
                raise InvalidPATHException(
                    '{!r} does not exist. You will need to download the ADB executable from https://github.com/fjwCode/cerium.'.format(self.__path))
        self.__debug = debug
        self.__start_server()
        self.__target_sn = device_sn
        self.__devices = self.devices()
        self.__target()

    def __target(self):
        devices_num = len(self.__devices)
        if devices_num == 0:
            raise DeviceConnectionException(
                'No devices are connected. Please connect the device with USB and turn on the USB debugging option.')
        elif not self.__target_sn and devices_num > 1:
            raise DeviceConnectionException(
                'Multiple devices detected, please specify device serial number.')
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

    def push(self, local='LICENSE', remote='/sdcard/LICENSE'):
        '''
        copy local files/directories to device
        '''
        if not os.path.exists(local):
            raise PathException(
                'Local path {!r} does not exist.'.format(local))
        output, error = self.__run_command('-s', self.__target_sn,
                                           'push', local, remote)

    def pull(self, remote, local):
        '''
        copy files/directories from device
        '''
        output, error = self.__run_command('-s', self.__target_sn,
                                           'pull', remote, local)
        if 'error' in output:
            raise PathException(
                'Remote path {!r} does not exist.'.format(remote))

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

    def input_tap(self, x, y):
        '''
        simulate finger click
        '''
        self.__run_command('-s', self.__target_sn, 'shell',
                           'input', 'tap', str(x), str(y))

    def input_swipe(self, x1, y1, x2, y2, duration=''):
        '''
        simulate finger slide
        '''
        self.__run_command('-s', self.__target_sn, 'shell',
                           'input', 'swipe', str(x1), str(y1), str(x2), str(y2), str(duration))

    def input_text(self, text):
        '''
        input text
        '''
        text = text.replace(' ', '\ ')
        self.__run_command('-s', self.__target_sn, 'shell',
                           'input', 'text', text)

    def input_keyevent(self, keyevent):
        '''
        input keyevent
        '''
        self.__run_command('-s', self.__target_sn, 'shell',
                           'input', 'keyevent', keyevent)

    def reboot(self, mode='default'):
        '''
        reboot the device;
        defaults to booting system image but supports bootloader and recovery too.
        sideload reboots into recovery and automatically starts sideload mode,
        sideload-auto-reboot is the same but reboots after sideloading.
        '''
        self.__run_command('-s', self.__target_sn, 'reboot')

    def __enter__(self, *arg):
        return self

    def __exit__(self, *arg):
        self.kill_server()
