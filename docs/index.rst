.. Cerium documentation master file, created by
   sphinx-quickstart on Thu Apr 26 15:07:20 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Cerium: A Toy for Android Automation
==================================

Release v\ |version|. (:ref:`Installation <install>`)

.. image:: https://img.shields.io/pypi/l/cerium.svg
    :target: https://pypi.org/project/cerium/

.. image:: https://img.shields.io/pypi/wheel/cerium.svg
    :target: https://pypi.org/project/cerium/

.. image:: https://img.shields.io/pypi/pyversions/cerium.svg
    :target: https://pypi.org/project/cerium/


**Cerium** is an Android automation framework for Python, safe for human consumption.

.. note:: The use of **Python 3** is *highly* preferred over Python 2. And I prefer the latest version of Python. So Cerium only supports Python 3.6 officially. Consider upgrading your applications and infrastructure if you find yourself *still* using Python 2 in production today. 


-------------------

**Behold, the power of Cerium**::

    >>> from cerium import AndroidDriver
    >>> driver = AndroidDriver()
    >>> driver.unlock(1997)   # unlock your device by password
    >>> driver.auto_connect()   # connect to your device via TCP/IP automatically
    Now you can unplug the USB cable, and control your device via WLAN.
    >>> driver.view_packgets_list(keyword='tencent')
    ['com.tencent.mm', 'com.tencent.android.qqdownloader', 'com.tencent.tim']
    >>> driver.make_a_call(18268237856)   # call me


**Cerium** allows you to send *organic, grass-fed* commands, without the the need for manual labor.


The User Guide
-----------------

This part of the documentation, which is mostly prose, begins with some
background information about Cerium, then focuses on step-by-step
instructions for getting the most out of Cerium.

.. toctree::
   :maxdepth: 2

   user/intro
   user/install
   user/quickstart


The API Documentation / Guide
----------------------------------

If you are looking for information on a specific function, class, or method,
this part of the documentation is for you.

.. toctree::
   :maxdepth: 2

   api


The Contributor Guide
------------------------

If you want to contribute to the project, this part of the documentation is for
you.

.. toctree::
   :maxdepth: 3

    authors


There are no more guides. You are now guideless.
Good luck.