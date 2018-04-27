.. _api:

Developer Interface
===================

.. module:: cerium

This part of the documentation covers all the interfaces of Cerium. For
parts where Cerium depends on external libraries, we document the most
important right here and provide links to the canonical documentation.


Main Interface
--------------

All of Cerium' functionality can be accessed by an instance of the :class:`AndroidDriver <AndroidDriver>` object.


.. autoclass:: AndroidDriver
   :inherited-members:


Exceptions
----------

.. autoexception:: cerium.ApplicationsException
.. autoexception:: cerium.CharactersException
.. autoexception:: cerium.DeviceConnectionException
.. autoexception:: cerium.NoSuchElementException
.. autoexception:: cerium.NoSuchPackageException
