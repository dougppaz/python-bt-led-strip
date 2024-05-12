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

Usage
=====

.. include:: usage.md
   :parser: myst_parser.sphinx_

Demonstrations
==============

MELK:
-----

.. code-block:: console

   python -m btledstrip.demonstrations.melk -h

API
===

.. automodule:: btledstrip
   :members:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
