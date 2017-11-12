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

Quickstart
----------

Create a new virtualenv and install the needed dependencies:

    virtualenv2 ~/bottle-webtools
    cd ~/bottle-webtools
    source bin/activate
    git clone https://github.com/muflone/bottle-webtools.git
    cd bottle-webtools
    pip install -r requirements.txt
    python2 start.py

The server will listen on the default port 10041 (see ```conf/general.ini```),
then open the webpage <http://localhost:10041> and login with the admin account:

* Username: admin
* Password: admin

![Folder configuration](/docs/en/new-folder.png?raw=true "Folder configuration")

The first step is to create at least some folders which will contain
your commands (<http://localhost:10041/folders>).

After creating some folder you can add your first commands
(<http://localhost:10041/commands>).

**WARNING!** All the commands must not require user input or they will hang
your application waiting for input.

![Simple command](/docs/en/command-simple.png?raw=true "Simple command")

Simple commands are ```dmesg``` or ```date``` as they doesn't require arguments
to run.

![Command with parameters](/docs/en/command-with-parameters.png?raw=true "Command with parameters")

Command with variable command-line parameters can be written defining the
parameters in the corresponding text area.

The syntax for custom parameters is:

    TEXT PARAMETER NAME=text:
    LIST PARAMETER NAME=list:value1,value2,value3

To use the parameters you can use:

    command --argument %(PARAMETER NAME)s

Please note that ```%(PARAMETER NAME)s``` will be replaced with the value of the
parameter during the execution.

![Command with shell](/docs/en/command-with-shell.png?raw=true "Command with shell")

Commands using the shell (eg pipes, globbing) can be specified by checking the
corresponding checkbox.

**No sanitization** or checks are made for the shell commands, so please be
aware about what are asking to your commands. None will prohibit you to delete
everything in your system with a wrong command. If you allow your user to input
data as arguments, **NEVER** do this with shell commands as they could insert
malicious commands in the parameters and the shell will execute them.
