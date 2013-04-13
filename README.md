QAA
===

QAA is a Question and Answer Web App. 
QAA is built on top of Django framework and is initially forked from the [OSQA](http://www.osqa.net/) source code to make it better and more convenient for everyone to use and develope it.  



Requirements
------------

### Production Environment

* Nginx
* Gunicorn
* Virtualenv
* Python 2.7.3
* Django 1.4.x
* MySQL 5.5
* Ubuntu server 12.04

### Development Environment

* Virtualenv
* Python 2.7.3
* Django 1.4.x
* MySQL 5.5
* Ubuntu 12.xx


Documentation
-------------

https://qaa.readthedocs.org/en/latest/


Installation
------------

1. Download the latest [tar ball](https://github.com/dangtrinh/qaa/tarball/master).
2. Untar and copy it to your directory (e.g. '/var/www/django_projects/')
3. Copy the settings_local.py.dist file to settings_local.py and modify it with your own information.
4. Activate your virtualenv environment and run syncdb to create the database schema.
5. Run the command 'python manage.py runserver' and enjoy QAA. 


License
-------

QAA is licensed under the GPLv3 License. See the [LICENSE](https://github.com/dangtrinh/qaa/blob/master/LICENSE) file for more details.


Contributors
------------

We are SCAFA Team. Our core members and maintainers are:

* @[dangtrinh](https://github.com/dangtrinh)
* @[nghitran](https://github.com/nghitran)
* @[vietjovi](https://github.com/vietjovi)

See the [CONTRIBUTORS](https://github.com/dangtrinh/qaa/blob/master/CONTRIBUTORS) file for more details.
