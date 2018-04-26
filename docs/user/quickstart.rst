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


Open WeChet And Interact with Applications