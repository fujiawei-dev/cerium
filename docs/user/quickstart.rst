.. _quickstart:

Quickstart
==========

Eager to get started? This page gives a good introduction in how to get started with Cerium.

First, make sure that:

* Cerium is :ref:`installed <install>`
* Your Android phone has USB debugging turned on in developer options.


Let's get started with some simple examples.


Unlock Your Android Phone
------------------------------

Unlock your Android phone with Cerium is very simple.

Begin by importing the Cerium module::

    >>> from cerium import AndroidDriver

Now, let's create a new instance of the android driver::

    >>> driver = AndroidDriver()

OK, let's unlock your Android phone by password::

    >>> driver.unlock(1997)

That's all well and good, but it's also only the start of what Cerium can do.


Use Basic Button
------------------

Home Button::

    >>> driver.home()

Back Button::

    >>> driver.back()

Menu Button::

    >>> driver.menu()

Switch Button::

    >>> driver.switch()

Power Button::

    >>> driver.power()

Brightness Down Button::

    >>> driver.brightness_down()

Brightness Up Button::

    >>> driver.brightness_up()

Volume Mute Button::

    >>> driver.volume_mute()

Volume Up Button::

    >>> driver.volume_up()

Volume Down Button::

    >>> driver.volume_down()


There are more buttons waiting for you to discover.
Even you can use *driver.send_keyevents()* to send a Android keyevent.


Device Connection Management
-----------------------------------

I really don't like play Cerium with a USB cable, so let's embracing the wireless world::

    >>> driver.auto_connect()   # connect to your device via TCP/IP automatically
    Now you can unplug the USB cable, and control your device via WLAN.


We can get rid of the limit of the USB cable within a certain range it!


Application Management
---------------------------

Show all packages fliter by keyword::

    >>> driver.view_packgets_list(keyword='tencent')
    ['com.tencent.mm', 'com.tencent.android.qqdownloader', 'com.tencent.tim']

Let's install an application::

    >>> driver.install('tv.apk')
    >>> driver.view_packgets_list(keyword='tv')
    ['com.hunantv.imgo.activity']

And then, uninstall it::

    >>> driver.uninstall('com.hunantv.imgo.activity')
    >>> driver.view_packgets_list(keyword='tv')
    []

View focused activity::

    >>> driver.view_focused_activity()
    'com.tencent.mm/.ui.LauncherUI'


Interact with Applications
---------------------------

Launch WeChat::

    >>> driver.launch_app('com.tencent.mm/com.tencent.mm.ui.LauncherUI')

Let's enter the chat interface and start chatting::

    >>> element = driver.find_element_by_class('android.widget.EditText')
    >>> element.clear()
    >>> element.send_keys("I'm White Turing.")

Close WeChat::

    >>> driver.close_app('com.tencent.mm')


File Management
---------------------------

Copy files from your computer to your phone::

    >>> driver.push('tv.apk', '/sdcard/tv.apk)


Copy files from your phone to your computer::

    >>> driver.pull('/sdcard/LICENSE', 'LICENSE')


Taking a screenshot of a device display, then copy it to your computer::

    >>> driver.pull_screencap(local='screencap.png')



-----------------------

Ready for more? Check out the :ref:`advanced <api>` section.
