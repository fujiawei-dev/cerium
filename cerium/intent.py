"""
The Actions implementation.
"""


class Actions(object):
    """
    Set of special actions.
    """
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
