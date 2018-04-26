# Cerium [![License](https://img.shields.io/badge/license-Apache_2-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0) [![PyPI version](https://badge.fury.io/py/cerium.svg)](https://badge.fury.io/py/cerium) 

> Cerium is an umbrella project encapsulating a variety of tools and
libraries enabling android automation.

Cerium's source code is made available under the [Apache 2.0 license](https://github.com/fjwCode/cerium/LICENSE).

## Introduction
[Android Debug Bridge (adb)](http://web.mit.edu/ruggles/MacData/afs/sipb/project/android/OldFiles/docs/tools/help/adb.html) is a versatile command line tool that lets you communicate with an emulator instance or connected Android-powered device. This project is based on it.

## Supported Python Versions
* Python 3.6+

## Supported Platforms
* Windows

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