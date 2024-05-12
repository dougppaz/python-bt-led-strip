.. Python LED Strip Bluetooth Controller API documentation master file, created by
   sphinx-quickstart on Sat May 11 11:45:12 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Documentation
=============

Python LED Strip Bluetooth Controller API was created by `Douglas Paz <https://www.douglaspaz.com/>`_ implemented with `bleak <https://github.com/hbldh/bleak>`_.

Supported controllers/devices
=============================

- MELK: :class:`MELKController<btledstrip.MELKController>`

Install
=======

Install from Pypi repository.

.. code-block:: console

   pip install btledstrip

Usage
=====

.. code-block:: python

   from btledstrip import (
       BTLedStrip,
       MELKController,
   )

   mac_address = "00:00:00:00:00:00"
   controller = MELKController()
   async with BTLedStrip(controller, mac_address) as led_strip:
       # turn on
       await led_strip.exec.turn_on()
       # turn off
       await led_strip.exec.turn_off()

Demonstrations
==============

MELK:
-----

.. code-block:: console

   python -m btledstrip.demonstrations.melk -h

Dev Command Terminal
====================

Debug a controller sending programmatically commands via Bluetooth.

Usage:

.. code-block:: console

   python -m btledstrip.dev -h

API
===

.. automodule:: btledstrip
   :members:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
