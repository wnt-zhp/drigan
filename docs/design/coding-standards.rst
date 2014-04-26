Zasady pracy
============

Basic stuff
-----------

Code Reviews
^^^^^^^^^^^^

Every story is created in it's own branch. Person developing code then adds
pull request. This pull request must be accepted by someone else.

Documentation
^^^^^^^^^^^^^

For now code is fairly undocumented, which is bad.

Every class, and public function needs a proper docstring. These docstrings
are in sphinx format. We'll use `autodoc <http://sphinx-doc.org/ext/autodoc.html>`_
to extract documentation from docstrings.

Unittests
^^^^^^^^^

Aim for 100% unittest coverage (for changed code).

Django stuff
------------

* Prefer `class based views <https://docs.djangoproject.com/en/1.6/topics/class-based-views/>`_ to function ones.
 * Even better: use `class based generic views <https://docs.djangoproject.com/en/1.6/topics/class-based-views/generic-display/>`_.
* Try to keep inter application dependencies to minimum
* Separate scout code with generic code


