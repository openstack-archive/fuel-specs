..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=================================================================
MOS RPM repositories: URLs, metadata, and other interface details
=================================================================

Improve the API (URLs and metadata) of MOS RPM repositories


--------------------
Problem description
--------------------

Currently the codename is bound to the MOS release number, that is, the repo
URLs look like (as documented in separate_mos_from_linux_)

::

 http://${mirror_host}/mos/centos-6/proposed
 http://${mirror_host}/mos/centos-6/security
 http://${mirror_host}/mos/centos-6/updates

This stucture yields several issues:
 - it's impossible to distinguish between repositories targeted for different
   CentOS versions
 - it's difficult to support per customer repositories


.. _separate_mos_from_linux: https://github.com/stackforge/fuel-specs/blob/master/specs/6.1/separate-mos-from-linux.rst


----------------
Proposed changes
----------------

Add change the codename mos${mos_release}-${distro_codename}, so the URLs are

::

 http://${mirror_host}/mos-repos/${distro}/mos${mos_release}-${distro}${distro_version}/os/x86_64/
 http://${mirror_host}/mos-repos/${distro}/mos${mos_release}-${distro}${distro_version}/updates/x86_64/
 http://${mirror_host}/mos-repos/${distro}/mos${mos_release}-${distro}${distro_version}/security/x86_64/
 http://${mirror_host}/mos-repos/${distro}/mos${mos_release}-${distro}${distro_version}/holdback/x86_64/
 http://${mirror_host}/mos-repos/${distro}/mos${mos_release}-${distro}${distro_version}/cr/x86_64/


Example: MOS 9.0/centos7
-------------------------------

::

 http://${mirror_host}/mos-repos/centos/mos9.0-centos7/os/x86_64/
 http://${mirror_host}/mos-repos/centos/mos9.0-centos7/updates/x86_64/
 http://${mirror_host}/mos-repos/centos/mos9.0-centos7/security/x86_64/
 http://${mirror_host}/mos-repos/centos/mos9.0-centos7/holdback/x86_64/
 http://${mirror_host}/mos-repos/centos/mos9.0-centos7/cr/x86_64/


Advantages:
 - MOS release can target arbitrary number of Centos versions
   (limited only by available resources).
 - It's possible to create arbitrary number of per customer (or per team)
   RPM repositories using codenames and custom url, but still keeping
   the overall structure.
 - It's possible to maintain a separate set of repositories which are
   not intended for OpenStack nodes (say, packages relevant for Fuel master
   node only).


Web UI
======

None


Nailgun
=======

None


Data model
----------

Default set of RPM repositories for OpenStack and FUEL nodes should be changed.


REST API
--------

None


Orchestration
=============

None


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

None


--------------
Upgrade impact
--------------

None


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

None


----------------
Developer impact
----------------

None


---------------------
Infrastructure impact
---------------------

CI jobs should be configured to consume packages from the correct mirrors


--------------------
Documentation impact
--------------------

* New RPM URLs and repo metadata should be documented so
  people can create their repositories the right way.


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  `Sergey Kulanov`_

Other contributors:
  `Dmitry Burmistrov`_

Mandatory design review:
  - `Alexander Evseev`_
  - `Dmitry Burmistrov`_
  - `Roman Vyalov`_
  - `Vladimir Kozhukalov`_
  - `Vitaly Parakhin`_


Work Items
==========

* Fix repo path in related fuel projects:
    - fuel-main;
    - fuel-mirror;
    - fuel-web;

* Fix repo path in related CI jobs:
    - packaging-ci;
    - fuel-ci with deployment tests;


Dependencies
============


------------
Testing, QA
------------


Acceptance criteria
===================

* RPM Packages build jobs should consume new mirror;

* Deployment tests should consume new mirror;

* Related changes should be reflected in nailgun fixtures;


----------
References
----------

.. _`Sergey Kulanov`: https://launchpad.net/~skulanov
.. _`Alexander Evseev`: https://launchpad.net/~aevseev-h
.. _`Dmitry Burmistrov`: https://launchpad.net/~dburmistrov
.. _`Roman Vyalov`: https://launchpad.net/~r0mikiam
.. _`Sergey Kulanov`: https://launchpad.net/~skulanov
.. _`Vladimir Kozhukalov`: https://launchpad.net/~kozhukalov
.. _`Vitaly Parakhin`: https://launchpad.net/~vparakhin
