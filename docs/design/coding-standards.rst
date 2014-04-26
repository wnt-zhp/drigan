Coding standards
================

Basic stuff
-----------

First solve bugs then add features
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Bug fixes are more important then new features.

Code Reviews
^^^^^^^^^^^^

Every story is created in it's own branch. Person developing code then adds
pull request. This pull request must be accepted by someone else.

When asigning someone with a code-review, please mark your story as
``In Review`` and assign it to this person in JIRA.

Meaningfull commit messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Use meaningfull commit messages. Please reference JIRA issue if appropriate.


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


