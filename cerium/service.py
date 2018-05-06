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

from typing import Any, Dict, Union

from .commands import _PATH, Commands
from .exceptions import DeviceConnectionException
from .utils import free_port, is_connectable, merge_dict


class BaseService(Commands):
    '''Object that manages the starting and stopping of the AndroidDriver.'''

    def __init__(self, executable: _PATH = 'default', port: Union[int, str] = 5037, env: Dict = None) -> None:
        super(BaseService, self).__init__(executable)
        self.port = port
        if self.port == 0:
            self.port = free_port()
        self.options = {'env': env}

    @property
    def service_tcp(self) -> str:
        '''Gets the TCP of the Service.'''
        return f"tcp://localhost:{self.port}"

    def service_args(self) -> NotImplemented:
        raise NotImplemented(
            "This method needs to be implemented in a sub class")

    def _build_cmd(self, args: Union[list, tuple]) -> str:
        '''Build command.'''
        cmd = [self.path]
        cmd.extend(self.service_args())
        cmd.extend(args)
        return cmd

    def _execute(self, *args: str, **kwargs: Any) -> tuple:
        '''Execute command.'''
        return self.execute(args=args, options=merge_dict(self.options, kwargs)).communicate()

    def start(self) -> None:
        '''Starts the Service.'''
        self._execute('start-server')

    def stop(self) -> None:
        '''Stops the service.'''
        self._execute('kill-server')

    def restart(self) -> None:
        '''Restart the server if it is running.'''
        self.stop()
        self.start()

    def version(self) -> str:
        '''Show the version number of Android Debug Bridge.'''
        output, _ = self._execute('version')
        return output.splitlines()[0].split()[-1]

    def devices(self) -> list:
        '''List connected devices.'''
        output, _ = self._execute('devices')
        return output.split()[4::2]

    def devices_l(self) -> Dict:
        '''List connected devices (-l for long output).'''
        output, _ = self._execute('devices', '-l')
        devices = output.split()[4::6]
        models = output.split()[7::6]
        return dict(zip(devices, models))

    def connect(self, host: str = '192.168.0.3', port: Union[int, str] = 5555) -> None:
        '''Connect to a device via TCP/IP directly.'''
        self.device_sn = f'{host}:{port}'
        if not is_connectable(host, port):
            raise ConnectionError(f'Cannot connect to {self.device_sn}.')
        self._execute('connect', self.device_sn)

    def __disconnect(self, host: str = '192.168.0.3', port: Union[int, str] = 5555) -> None:
        '''Disconnect from given TCP/IP device [default port=5555].'''
        self.device_sn = None
        self._execute('disconnect', f'{host}:{port}')

    def __disconnect_all(self) -> None:
        '''Disconnect all.'''
        self.device_sn = None
        self._execute('disconnect')

    def get_state(self) -> str:
        '''offline | bootloader | device'''
        output, error = self._execute('get-state')
        if error:
            raise DeviceConnectionException(error.split(':', 1)[-1].strip())
        return output.strip()


class Service(BaseService):
    '''Object that manages the starting and stopping of the AndroidDriver.'''

    def __init__(self, executable_path: _PATH = 'default', port: Union[int, str] = 5037, env: Dict = None, service_args: Union[list, tuple] = None) -> None:
        '''Creates a new instance of the Service.

        Args:
            executable_path: Path to the AndroidDriver.
            port: Port the service is running on.
            env: Environment variables.
            service_args: List of args to pass to the androiddriver service.
        '''

        self._service_args = service_args or []

        super(Service, self).__init__(executable_path, port=port, env=env)

    def service_args(self) -> str:
        '''Parameters when starting the service.'''
        return ['-P', str(self.port)] + self._service_args
