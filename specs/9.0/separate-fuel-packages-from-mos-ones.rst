..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode


====================================
Separate fuel packages from MOS ones
====================================

https://blueprints.launchpad.net/fuel/+spec/separate-fuel-packages-from-mos-ones

For Fuel upstream/downstream we need to separate Fuel packages from other MOS
ones. At the moment we publish fuel packages to repository with other MOS
packages (mos openstack, mos dependency, etc). Separation will allow us to build
ISO with upstream/downstream Fuel packages and deploy master node with packages
from upstream/downstream fuel repository.


--------------------
Problem description
--------------------

We need to have an ability to deploy environment with fuel packages build either
from upstream or donwstream. For now there are several ways to acheive this
goal:

- build custom mirrors using perestroika [1] and then pass them as parameters
  during ISO build [2];

- build fuel packages together with ISO by using parameters defined in
  fuel-main [3].

The above two cases have drawbacks:

- it's not possible to deliver maintains updates for fuel packages;

- fuel upstream/downstream mirrors doesn't exists and fuel packages reside
  together with MOS ones


----------------
Proposed changes
----------------

#. Move fuel packages from MOS mirror to separate Fuel mirror both for rpm and
   deb packages

#. Update peresotroika code to be able to publish fuel packages in separate
   mirror

#. Create separate fuel mirror in fuel-main project

#. Put fuel packages repos on mirrors in all location with `base path`
   defined below:

  +----------+---------------------------------------+
  | OS Dist. |          URI path on mirrors          |
  +==========+=======================================+
  | CentOS 7 | TBD                                   |
  +----------+---------------------------------------+
  | Ubuntu   | TBD                                   |
  +----------+---------------------------------------+

Web UI
======

None


Nailgun
=======

Data model
----------

None

REST API
--------

None


Orchestration
=============

RPC Protocol
------------

None


Fuel Client
===========

None


Plugins
=======

None


Fuel Library
============

None

------------
Alternatives
------------

There is no alternative


--------------
Upgrade impact
--------------

TBD


---------------
Security impact
---------------

None


--------------------
Notifications impact
--------------------

None


---------------
End user impact
---------------

None


------------------
Performance impact
------------------

None


-----------------
Deployment impact
-----------------

TBD


----------------
Developer impact
----------------

TBD


---------------------
Infrastructure impact
---------------------

TBD


--------------------
Documentation impact
--------------------

TBD


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  `Sergey Kulanov`_

CI-team:
  `Alexandra Fedorova`_

QA-team:
  TBD

Mandatory Design Reviewers:
  - `Dmitry Burmistrov`_
  - `Roman Vyalov`_
  - `Vladimir Kozhukalov`_
  - `Vitaly Parakhin`_


Work Items
==========

#. Create separate mirror for fuel packages both centos and ubuntu
#. Update perestroika code/publisher
#. Update packaging CI for building downstream packages
#. Implement external packaging CI for building upstream packages


Dependencies
============

TBD


------------
Testing, QA
------------

TBD

Acceptance criteria
===================

TBD


----------
References
----------

.. _`Alexandra Fedorova`: https://launchpad.net/~afedorova
.. _`Dmitry Burmistrov`: https://launchpad.net/~dburmistrov
.. _`Roman Vyalov`: https://launchpad.net/~r0mikiam
.. _`Sergey Kulanov`: https://launchpad.net/~skulanov
.. _`Vladimir Kozhukalov`: https://launchpad.net/~kozhukalov
.. _`Vitaly Parakhin`: https://bugs.launchpad.net/~vparakhi
