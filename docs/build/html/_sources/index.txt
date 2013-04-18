.. QAA documentation master file, created by
   sphinx-quickstart on Fri Apr 12 14:01:50 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to QAA's documentation!
===============================

Contents:

.. toctree::
   :maxdepth: 2



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


QAA
===

A Question and Answer Web App


Requirements
==================

Production Environment
----------------------

* Nginx
* Gunicorn
* Virtualenv
* Python 2.7.3
* Django 1.4.x
* MySQL 5.5
* Ubuntu server 12.04

Development Environment
-----------------------

* Virtualenv
* Python 2.7.3
* Django 1.4.x
* MySQL 5.5
* Ubuntu 12.xx


Documentation
=============

https://qaa.readthedocs.org/en/latest/



Installation
============

1. Download the latest tar ball (https://github.com/dangtrinh/qaa/tarball/master).
2. Untar and copy it to your directory (e.g. '/var/www/django_projects/')
3. Copy the settings_local.py.dist file to settings_local.py and modify it with your own information.
4. (Optional) Create and activate your virtualenv environment.
5. Install requirement packages:

::
    pip install -r requirements.txt

6. Get your database ready:

::
    python manage.py syncdb
    python manage.py migrate --all

7. Run the command 'python manage.py runserver' and enjoy QAA. 


License
=======

QAA is licensed under the GPLv3 License. See the LICENSE (https://github.com/dangtrinh/qaa/blob/master/LICENSE) file for more details.


Contributors
============

QAA is a fork from the OSQA (http://www.osqa.net/) software and being actively maintained by SCAFA Team.

Our core members and maintainers are:

* @dangtrinh (https://github.com/dangtrinh)
* @nghitran (https://github.com/nghitran)
* @vietjovi (https://github.com/vietjovi)

See the CONTRIBUTORS (https://github.com/dangtrinh/qaa/blob/master/CONTRIBUTORS) file for more details.

