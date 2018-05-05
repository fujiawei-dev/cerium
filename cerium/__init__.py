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

import sys
import warnings

from .androiddriver import AndroidDriver
from .by import By
from .intent import Actions, Category
from .keys import Keys


# Meta information
__author__ = "White Turing"
__version__ = "1.2.0"


# Sanity checking.
try:
    assert sys.version_info.major == 3
    assert sys.version_info.minor > 5
except AssertionError:
    raise RuntimeError('Cerium requires Python 3.6+!') from AssertionError

if sys.platform != 'win32':
    warnings.warn('Cerium only supports Windows officially! Cannot guarantee normal operation on other platforms!', RuntimeWarning)

__all__ = [
    'AndroidDriver',
    'By',
    'Keys',
    'Actions',
    'Category,'
]
