Bottle WebTools
===============
**Description:** Execute command line tools from a web interface.

**Copyright:** 2017 Fabio Castelli (Muflone) <muflone(at)vbsimple.net>

**License:** GPL-2+

**Source Code:** https://github.com/muflone/bottle-webtools

System Requirements
-------------------

* Python 2.x (developed and tested for Python 2.7.5)
* Bottle (https://pypi.python.org/pypi/bottle)
* Beaker (https://pypi.python.org/pypi/Beaker)
* A Bottle enabled WSGI Server
  http://www.bottlepy.org/docs/dev/deployment.html#switching-the-server-backend

Installation
------------

Simply pull the sources, configure conf/app_webtools.ini and conf/general.ini
files and start the server using

Usage
-----

Before the first use edit the configuration file ```conf/general.ini``` to suit
your needs.

Alternatively you can create a ```conf/custom.ini``` file to override the
general configuration file.

To start the application simply use:

    python2 start.py
