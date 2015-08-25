..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
CI test for repository consistency
==========================================

https://blueprints.launchpad.net/fuel/+spec/ci-repo-test

Sometimes, new packages added to repository break some other packages
residing in this repository. Deploy test will catch such error but not
always and it takes much time. At the moment only these new packages
are tested for installation, but not the whole repository.


--------------------
Problem description
--------------------

One case when new package (``N``) breaks already existing package
(``E``) is when ``E`` depends on ``N`` but ``N`` conflicts with some
other dependency of ``E``.


----------------
Proposed changes
----------------

To catch such errors a new test is proposed. It will simulate
installation of each package in environment where both main and
temporary repositories are enabled.

Testing script works in 2 stages. First it makes several attempts to
install all packages from main and temporary repositories, removing
conflicting packages from installation set as it goes. Normally this
process will end with installation set that has no conflicts. In the
second stage it will try to install conflicting packages one by
one. In the worst case it will be impossible to reduce installation
set to the set of non-conflicting packages with such naive
algorithm. Then all packages in installation set will be tested one by
one.


Web UI
======

None.


Nailgun
=======

None.


Data model
----------

None.


REST API
--------

None.


Orchestration
=============

None.


RPC Protocol
------------

None.


Fuel Client
===========

None.


Plugins
=======

None.


Fuel Library
============

None.


------------
Alternatives
------------

None.


--------------
Upgrade impact
--------------

None.


---------------
Security impact
---------------

None.


--------------------
Notifications impact
--------------------

None.


---------------
End user impact
---------------

None.


------------------
Performance impact
------------------

The worst case described in `Proposed changes`_ may take up to 20
minutes.


-----------------
Deployment impact
-----------------

None.


----------------
Developer impact
----------------

Developers will have to wait longer for the results of CI install test
but in exchange they will be notified of problems in advance.


--------------------------------
Infrastructure/operations impact
--------------------------------

This check will be implemented as an additional script executed by
install test jobs. It shouldn't consume many resources.

Jenkins slaves which are running install tests should have working
commands yum and repoquery.


--------------------
Documentation impact
--------------------

This test should be documented on the wiki.


--------------------
Expected OSCI impact
--------------------

Described above.


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  `Alexander Tsamutali`_

Other contributors:
  `Alexey Sheplyakov`_

.. _`Alexander Tsamutali`: https://launchpad.net/~astsmtl
.. _`Alexey Sheplyakov`: https://launchpad.net/~asheplyakov
  

Work Items
==========

* Refactor current install test. Split it into separate scripts.
* Write script to test yum repositories.
* Adapt script by Alexei Sheplyakov to CI environment.
* Add new scripts to ``7.0.mos.install-{deb,rpm}``.


Dependencies
============

None.


------------
Testing, QA
------------

It is possible to perform testing by submitting deliberately broken
change request.


Acceptance criteria
===================

Each CR that produces temporary repositiry, which is then merged into
main repository, triggers repository test. This test simulates
installation of every package in main and temporary repositories.


----------
References
----------

Initial version of testing script by Alexei Sheplyakov: 
https://github.com/asheplyakov/mosrepochk/blob/master/repocheck
