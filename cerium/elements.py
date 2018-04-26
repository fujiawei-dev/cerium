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

from .keys import Keys


class Elements(object):
    '''Represents a element.'''

    def __init__(self, parent, node, key, value, coord, click_point):
        self._parent = parent
        self._node = node
        self._key = key
        self._value = value
        self._coord = coord
        self._click_point = click_point

    def __repr__(self):
        return '<{0.__module__}.{0.__name__} (element="{2}: {3}", coord="{4}")>'.format(type(self), self._key, self._value, self._coord)

    @property
    def text(self):
        """The text of the element."""
        return self._node['text']

    @property
    def resource_id(self):
        """The resource-id of the element."""
        return self._node['resource-id']

    @property
    def class_(self):
        """The class of the element."""
        return self._node['class']

    @property
    def package(self):
        """The package of the element."""
        return self._node['package']

    @property
    def content_desc(self):
        """The content-desc of the element."""
        return self._node['content-desc']

    @property
    def checkable(self):
        """The checkable of the element."""
        return self._node['checkable']

    @property
    def bounds(self):
        """The bounds of the element."""
        return self._coord

    @property
    def coord(self):
        """The coord of the element."""
        return self._coord

    def click(self):
        """Clicks the element."""
        self._parent.click(*self._click_point)

    def clear(self):
        """Clears the text if it's a text entry element."""
        self.click()
        for i in self.text:
            self._parent.send_keyevents(Keys.DEL)

    def is_selected(self) -> bool:
        """Returns whether the element is selected.

        Can be used to check if a checkbox or radio button is selected.
        """
        return self._node['selected']

    def is_enabled(self) -> bool:
        """Returns whether the element is enabled."""
        return self._node['enabled']

    def is_checked(self) -> bool:
        """Returns whether the element is checked."""
        return self._node['checked']

    def is_clickable(self) -> bool:
        """Returns whether the element is clickable."""
        return self._node['clickable']

    def is_focusable(self) -> bool:
        """Returns whether the element is focusable."""
        return self._node['focusable']

    def is_focused(self) -> bool:
        """Returns whether the element is focused."""
        return self._node['focused']

    def is_scrollable(self) -> bool:
        """Returns whether the element is scrollable."""
        return self._node['scrollable']

    def is_long_clickable(self) -> bool:
        """Returns whether the element is long-clickable."""
        return self._node['long-clickable']

    def is_password(self) -> bool:
        """Returns whether the element is password."""
        return self._node['password']
