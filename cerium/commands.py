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
import subprocess
from subprocess import PIPE


class Commands(object):
    '''Defines execution for the standard commands.'''

    def __init__(self, executable='default'):
        '''Creates a new instance of the Commands.

        Args:
            executable_path: Path to the AndroidDriver.
        '''

        if executable == 'default':
            self.path = os.path.join(os.path.dirname(__file__), 'executable', 'adb.exe')
        elif executable.endswith('adb.exe'):
            if not os.path.isfile(executable):
                raise FileNotFoundError('{!r} does not exist.'.format(self.path))
            self.path = executable
        elif executable in ['adb', 'adb.exe']:
            PATH = os.environ['PATH']
            if not ('adb' in PATH or 'android' in PATH):
                raise EnvironmentError('PATH does not exist.')
            self.path = executable
        else:
            self.path = os.path.join(os.path.dirname(__file__), 'executable', 'adb.exe')

    def _build_cmd(self, args):
        '''Build command.'''
        cmd = [self.path]
        cmd.extend(args)
        return cmd

    def execute(self, *args):
        '''Execute command.'''
        args = self._build_cmd(args)
        process = subprocess.Popen(
            args, stdout=PIPE, stderr=PIPE, stdin=PIPE, encoding='utf-8')
        return process
