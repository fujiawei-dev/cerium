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

"""The Intent implementation."""


class Actions(object):
    """Set of special actions."""

    # Broadcast
    CONNECTIVITY_CHANGE = 'android.net.conn.CONNECTIVITY_CHANGE'
    SCREEN_ON = 'android.intent.action.SCREEN_ON'
    SCREEN_OFF = 'android.intent.action.SCREEN_OFF'
    BATTERY_LOW = 'android.intent.action.BATTERY_LOW'
    BATTERY_OKAY = 'android.intent.action.BATTERY_OKAY'
    BOOT_COMPLETED = 'android.intent.action.BOOT_COMPLETED'
    DEVICE_STORAGE_LOW = 'android.intent.action.DEVICE_STORAGE_LOW'
    DEVICE_STORAGE_OK = 'android.intent.action.DEVICE_STORAGE_OK'
    PACKAGE_ADDED = 'android.intent.action.PACKAGE_ADDED'
    STATE_CHANGE = 'android.net.wifi.STATE_CHANGE'
    WIFI_STATE_CHANGED = 'android.net.wifi.WIFI_STATE_CHANGED'
    BATTERY_CHANGED = 'android.intent.action.BATTERY_CHANGED'
    INPUT_METHOD_CHANGED = 'android.intent.action.INPUT_METHOD_CHANGED'
    ACTION_POWER_CONNECTED = 'android.intent.action.ACTION_POWER_CONNECTED'
    ACTION_POWER_DISCONNECTED = 'android.intent.action.ACTION_POWER_DISCONNECTED'
    DREAMING_STARTED = 'android.intent.action.DREAMING_STARTED'
    DREAMING_STOPPED = 'android.intent.action.DREAMING_STOPPED'
    WALLPAPER_CHANGED = 'android.intent.action.WALLPAPER_CHANGED'
    HEADSET_PLUG = 'android.intent.action.HEADSET_PLUG'
    MEDIA_UNMOUNTED = 'android.intent.action.MEDIA_UNMOUNTED'
    MEDIA_MOUNTED = 'android.intent.action.MEDIA_MOUNTED'
    POWER_SAVE_MODE_CHANGED = 'android.os.action.POWER_SAVE_MODE_CHANGED'

    # Action
    VIEW = 'android.intent.action.VIEW'
    WEB_SEARCH = 'android.intent.action.WEB_SEARCH'
    SYNC = 'android.intent.action.SYNC'
    CALL = 'android.intent.action.CALL'
    ANSWER = 'android.intent.action.ANSWER'
    ADD_SHORTCUT = 'android.intent.action.ADD_SHORTCUT'
    ALL_APPS = 'android.intent.action.ALL_APPS'
    SETTINGS = 'android.intent.action.SETTINGS'


class Category(object):
    """Set of special category."""

    ALTERNATIVE = 'android.intent.category.ALTERNATIVE'
    WALLPAPER = 'android.intent.category.WALLPAPER'
    UNIT_TEST = 'android.intent.category.UNIT_TEST'
    TEST = 'android.intent.category.TEST'
    TAB = 'android.intent.category.TAB'
    SAMPLE_CODE = 'android.intent.category.SAMPLE_CODE'
    PREFERENCE = 'android.intent.category.PREFERENCE'
    HOME = 'android.intent.category.HOME'
    BROWSABLE = 'android.intent.category.BROWSABLE'
    DEFAULT = 'android.intent.category.DEFAULT'
    DEVELOPMENT_PREFERENCE = 'android.intent.category.DEVELOPMENT_PREFERENCE'
    EMBED = 'android.intent.category.EMBED'
    FRAMEWORK_INSTRUMENTATION_TEST = 'android.intent.category.FRAMEWORK_INSTRUMENTATION_TEST'
    GADGET = 'android.intent.category.GADGET'
    LAUNCHER = 'android.intent.category.LAUNCHER'
    SELECTED_ALTERNATIVE = 'android.intent.category.SELECTED_ALTERNATIVE'
