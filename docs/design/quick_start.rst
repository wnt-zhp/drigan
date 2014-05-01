Quick start
===========

Installation
------------

Pre-requirements
^^^^^^^^^^^^^^^^

Altough most requirements will be installed for you automatically using 
`PIP <https://github.com/pypa/pip>`_, there are some pre-requirements:

 * `Python <https://www.python.org/>`_ >= 3.4
 * `PostgreSQL <http://www.postgresql.org/>`_ >= 9.3.4 with `HStore
   <http://www.postgresql.org/docs/9.0/static/hstore.html>`_ enabled
 * `git <http://git-scm.com/>`_

Enabling HStore
"""""""""""""""

To enable HStore in Postgresql type:

.. code-block:: bash

    $ psql -d template1 -c 'create extension hstore;'

From now on all created databases would have HStore installed. You can also
run this command only for one database, after creating it.

Setting up virtual environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is recommended to use virtual environments to decouple Python packages. For
example, using `venv <https://docs.python.org/3/library/venv.html>`_ (included
in Python >= 3.3):

.. code-block:: bash

    $ pyvenv /path/to/environment        #  create virtual environment
    $ cd /path/to/environment            #  cd to its directory
    $ source bin/activate                #  activate virtual environment

From now you can use only packages installed in this virtual environment.
additionally, copies of `python` and `pip` binaries were created.

Take a look at `virtualenvwrapper <http://virtualenvwrapper.readthedocs.org/en/latest/>`_
to make those commands even simpler.

Downloading project
^^^^^^^^^^^^^^^^^^^

Clone it using git:

.. code-block:: bash

    $ git clone https://bitbucket.org/zeroos/drigan.git

Installing requirements
^^^^^^^^^^^^^^^^^^^^^^^

All requirements are in `requirements.txt`. You can install it with (don't
forget about activating virtual environment!):

.. code-block:: bash

    $ pip install -r requirements.txt

Hooray! Everything is installed, time to configure it and run.

Setup
-----

Like in every Django application, you have to provide a `settings.py` file.
There is a template for it in `drigan/settings_example.py`, just copy it and
edit with your favourite editor:

.. code-block:: bash

    $ cp drigan/settings_example.py drigan/settings.py
    $ vim drigan/settings.py

Creating database
^^^^^^^^^^^^^^^^^

Now it's time to create a database. If you are doing it on your own just for
development purposes you can for example use the following command. You have to
issue it as a user with permissions to create PostgreSQL databases on your
system (usually `postgres`).

.. code-block:: bash

    postgres $ createdb drigan     # or other database name

If you ever need to reset your database to initial state you can ofcourse use
Django management command (`reset`) or just recreate the database (probably more
reliable):

.. code-block:: bash

    postgres $ dropdb drigan     # drop the database
    postgres $ createdb drigan     # and create it again

Before first stable version is released we are not going to use migrations, so
you will have to reset the database after each model change.

settings.py
^^^^^^^^^^^

Every setting in the copied `settings_example.py` file is documented, so you can
just go through them and adjust them. 

If you are just trying to run it in developing mode, you don't have to
change much -- just adjust your database credentials if needed and everything 
should work.

However, if you'd like to set up a production environment, you should look over
each setting. And don't forget to set `DEBUG = False`!

Database
^^^^^^^^

.. code-block:: bash

    $ python ./manage.py syncdb

Collecting static files
^^^^^^^^^^^^^^^^^^^^^^^

.. note::
    
    You don't have to do it when `DEBUG = False`, i.e. in a development
    environmennt. In this case static files are served automatically by Django.

Before doing it make sure `STATIC_ROOT` is set correctly in `settings.py`.

.. code-block:: bash

    $ python manage.py collectstatic

That's it!
----------

And that's everything. If you're just running development instance you can run
the server with

.. code-block:: bash

    $ python manage.py runserver

and start coding!

If you are setting up a production environment you can use any technique that's
used to `deploy Django <https://docs.djangoproject.com/en/dev/howto/deployment/>`_.

