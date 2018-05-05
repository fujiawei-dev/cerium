# Cerium
[![PyPI version](https://img.shields.io/pypi/v/cerium.svg)](https://pypi.org/project/cerium/)
[![Wheel](https://img.shields.io/pypi/wheel/cerium.svg)](https://pypi.org/project/cerium/)
[![Python version](https://img.shields.io/pypi/pyversions/cerium.svg)](https://pypi.org/project/cerium/)
[![License](https://img.shields.io/badge/license-Apache_2-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)
[![Documentation status](https://readthedocs.org/projects/cerium/badge/?version=latest)](http://cerium.readthedocs.io/en/latest/?badge=latest)

> Cerium is an umbrella project encapsulating a variety of tools and
libraries enabling android automation.

Cerium's source code is made available under the [Apache 2.0 license](https://github.com/fjwCode/cerium/LICENSE).

Welcome to **Read the Docs** for [Cerium](http://cerium.readthedocs.io/)!


## Introduction

**Cerium: A Toy for Android Automation**

**Cerium** is an Android automation framework for Python, safe for human consumption.

**Behold, the power of Cerium**:

```python
>>> from cerium import AndroidDriver
>>> driver = AndroidDriver()
>>> driver.unlock(1997)   # unlock your device by password
>>> driver.auto_connect()   # connect to your device via TCP/IP automatically
Now you can unplug the USB cable, and control your device via WLAN.
>>> driver.view_packgets_list(keyword='tencent')
['com.tencent.mm', 'com.tencent.android.qqdownloader', 'com.tencent.tim']
>>> driver.make_a_call(18268237856)   # call me
```

**Cerium** allows you to send *organic, grass-fed* commands, without the the need for manual labor.

[Android Debug Bridge (adb)](http://web.mit.edu/ruggles/MacData/afs/sipb/project/android/OldFiles/docs/tools/help/adb.html) is a versatile command line tool that lets you communicate with an emulator instance or connected Android-powered device. This project is based on it.

## Supported Python Versions
* Python 3.6+

## Supported Platforms
* Windows 10 (Other platforms have not been tested and are not intended to be supported for the time being officially)

## Installation
If you have [pip](https://pip.pypa.io/) on your system, you can simply install or upgrade cerium:

    pip install -U cerium

Alternately, you can download the source distribution from [PyPI](https://badge.fury.io/py/cerium), unarchive it, and run:

    python setup.py install

Or by [github.com](https://github.com/fjwCode/cerium):

    git clone git@github.com:fjwCode/cerium.git
    cd cerium
    python setup.py install

> Note: You may want to consider using [virtualenv](http://www.virtualenv.org/) to create isolated Python environments.


## [Android Debug Bridge](http://web.mit.edu/ruggles/MacData/afs/sipb/project/android/OldFiles/docs/tools/help/adb.html) 
Cerium requires Android Debug Bridge Tool to with the chosen android device. And Cerium contains *Android Debug Bridge*  by default. You don't need to set the environment variable by yourself.


## Quickstart

* List connected android devices or simulator.
* Show the version of Android Debug Bridge.

```python
from cerium import AndroidDriver

driver = AndroidDriver()

print(driver.devices())
print(driver.devices_l())  # show devices and models

print(driver.version())
```

* Copy local files/directories to device.
* Copy files/directories from device.
* Taking a screenshot of a device display, then copy it to your computer.

```python
from cerium import AndroidDriver

driver = AndroidDriver()

driver.push(local='README.md', remote='/sdcard/README.md')
driver.pull(remote='/sdcard/README.md', local='README.md')

driver.pull_screencap(local='screencap.png')
```

* Simulate finger click.
* Simulate finger slide.
* Input text.

```python
from cerium import AndroidDriver

driver = AndroidDriver()

driver.click(100, 100)
driver.swipe(100, 200, 100, 100, duration=100)
driver.send_keys("I'm White Turing.")
```


## Author

Cerium is written and maintained by [White Turing](https://github.com/fjwCode) (fujiawei@stu.hznu.edu.cn).