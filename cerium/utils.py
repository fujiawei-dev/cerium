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

"""The utils methods."""

import socket
from typing import Dict, Optional


def free_port() -> int:
    """Determines a free port using sockets."""
    free_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    free_socket.bind(('0.0.0.0', 0))
    free_socket.listen(5)
    port = free_socket.getsockname()[1]
    free_socket.close()
    return port


def is_connectable(host: str, port: Optional[int, str]) -> bool:
    """Tries to connect to the device to see if it is connectable.

    Args:
        host: The host to connect.
        port: The port to connect.

    Returns:
        True or False.
    """
    socket_ = None
    try:
        socket_ = socket.create_connection((host, port), 1)
        result = True
    except socket.timeout:
        result = False
    finally:
        if socket_:
            socket_.close()
    return result


def merge_dict(dict1: Optional[Dict], dict2: Optional[Dict]) -> Dict:
    new_dict = {**dict1, **dict2}
    return new_dict