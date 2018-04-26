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

import os

from .commands import Commands
from .utils import free_port, is_connectable


class BaseService(Commands):
    '''Object that manages the starting and stopping of the AndroidDriver.'''

    def __init__(self, executable='default', port=5037, env=None):
        super(BaseService, self).__init__(executable)
        self.port = port
        if self.port == 0:
            self.port = free_port()
        self.env = env or os.environ

    def service_tcp(self):
        '''Gets the TCP of the Service.'''
        return "tcp://localhost:{}".format(self.port)

    def command_line_args(self):
        raise NotImplemented(
            "This method needs to be implemented in a sub class")

    def _build_cmd(self, args):
        '''Build command.'''
        cmd = [self.path]
        cmd.extend(self.command_line_args())
        cmd.extend(args)
        return cmd

    def _execute(self, *args):
        '''Execute command.'''
        process = self.execute(*args)
        return process.communicate()

    def start(self):
        '''Starts the Service.'''
        self._execute('start-server')

    def stop(self):
        '''Stops the service.'''
        self._execute('kill-server')

    def restart(self):
        '''Restart the server if it is running.'''
        self.stop()
        self.start()

    def version(self):
        '''Show the version number of Android Debug Bridge.'''
        output, _ = self._execute('version')
        return output.splitlines()[0].split()[-1]

    def devices(self):
        '''List connected devices.'''
        output, _ = self._execute('devices')
        return output.split()[4::2]

    def devices_l(self):
        '''List connected devices (-l for long output).'''
        output, _ = self._execute('devices', '-l')
        devices = output.split()[4::6]
        models = output.split()[7::6]
        return dict(zip(devices, models))

    def connect(self, host='192.168.0.3', port=5555):
        '''Connect to a device via TCP/IP directly.'''
        self.device_sn = '{}:{}'.format(host, port)
        if not is_connectable(host, port):
            raise ConnectionError(
                'Cannot connect to {}.'.format(self.device_sn))
        self._execute('connect', self.device_sn)

    def __disconnect(self, host='192.168.0.3', port=5555):
        '''Disconnect from given TCP/IP device [default port=5555].'''
        self.device_sn = None
        self._execute('disconnect', '{}:{}'.format(host, port))

    def __disconnect_all(self):
        '''Disconnect all.'''
        self.device_sn = None
        self._execute('disconnect')

    def get_state(self):
        '''offline | bootloader | device'''
        output, error = self._execute('get-state')
        if error:
            raise DeviceConnectionException(
                'No devices are connected. Please connect the device with USB or \
                                via WLAN and turn on the USB debugging option.')
        return output.strip()


class Service(BaseService):
    '''Object that manages the starting and stopping of the AndroidDriver.'''

    def __init__(self, executable_path='default', port=5037, env=None, service_args=None):
        '''Creates a new instance of the Service.

        Args:
            executable_path: Path to the AndroidDriver.
            port: Port the service is running on.
            env: Environment variables.
            service_args: List of args to pass to the androiddriver service.
        '''

        self.service_args = service_args or []

        super(Service, self).__init__(executable_path, port=port, env=env)

    def command_line_args(self):
        return ['-P', str(self.port)] + self.service_args
