..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=================================================================
MOS RPM repositories: URLs, metadata, and other interface details
=================================================================

Improve the API (URLs and metadata) of MOS RPM repositories

Problem description
===================

Currently the codename is bound to the MOS release number, that is, the repo
URLs look like (as documented in separate_mos_from_linux_)

::

 http://${mirror_host}/mos/centos-6/proposed
 http://${mirror_host}/mos/centos-6/security
 http://${mirror_host}/mos/centos-6/updates

This stucture yields several issues:
 - it's impossible to distinguish between repositories targeted for different
   Centos versions
 - it's difficult to support per customer repositories


.. _separate_mos_from_linux: https://github.com/stackforge/fuel-specs/blob/master/specs/6.1/separate-mos-from-linux.rst


Proposed change
===============

Add change the codename mos${mos_release}-${distro_codename}, so the URLs are

::

 http://${mirror_host}/mos-repos/${distro}/mos${mos_release}-${distro}${distro_version}/os/x86_64/
 http://${mirror_host}/mos-repos/${distro}/mos${mos_release}-${distro}${distro_version}/updates/x86_64/
 http://${mirror_host}/mos-repos/${distro}/mos${mos_release}-${distro}${distro_version}/security/x86_64/
 http://${mirror_host}/mos-repos/${distro}/mos${mos_release}-${distro}${distro_version}/holdback/x86_64/
 http://${mirror_host}/mos-repos/${distro}/mos${mos_release}-${distro}${distro_version}/cr/x86_64/

Example: MOS 7.0/centos6
--------------------------

::

 http://${mirror_host}/mos-repos/centos/mos7.0-centos6/os/x86_64/
 http://${mirror_host}/mos-repos/centos/mos7.0-centos6/updates/x86_64/
 http://${mirror_host}/mos-repos/centos/mos7.0-centos6/security/x86_64/
 http://${mirror_host}/mos-repos/centos/mos7.0-centos6/holdback/x86_64/
 http://${mirror_host}/mos-repos/centos/mos7.0-centos6/cr/x86_64/

Example: MOS 7.0/centos6-fuel
-------------------------------

::

 http://${mirror_host}/mos-repos/centos/mos7.0-centos6-fuel/os/x86_64/
 http://${mirror_host}/mos-repos/centos/mos7.0-centos6-fuel/updates/x86_64/
 http://${mirror_host}/mos-repos/centos/mos7.0-centos6-fuel/security/x86_64/
 http://${mirror_host}/mos-repos/centos/mos7.0-centos6-fuel/holdback/x86_64/
 http://${mirror_host}/mos-repos/centos/mos7.0-centos6-fuel/cr/x86_64/


Example: Customer 7.0/centos6
-------------------------------

::

 http://${mirror_host}/customer/centos/mos7.0-centos6/os/x86_64/
 http://${mirror_host}/customer/centos/mos7.0-centos6/updates/x86_64/
 http://${mirror_host}/customer/centos/mos7.0-centos6/security/x86_64/
 http://${mirror_host}/customer/centos/mos7.0-centos6/holdback/x86_64/
 http://${mirror_host}/customer/centos/mos7.0-centos6/cr/x86_64/


Suffix *fuel* was removed from mirror path since MOS 9.0

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

Alternatives
------------

Data model impact
-----------------

Default set of RPM repositories for OpenStack and FUEL nodes should be changed.

REST API impact
---------------

None.

Upgrade impact
--------------

None.


Security impact
---------------

None.

Notifications impact
--------------------

None.

Other end user impact
---------------------

None.

Performance Impact
------------------

None.

Plugin impact
-------------

None.

Other deployer impact
---------------------

None.

Developer impact
----------------

None.

Infrastructure impact
---------------------


Implementation
==============


Assignee(s)
-----------


Work Items
----------


Dependencies
============

None.


Testing
=======


Acceptance criteria
-------------------


Documentation Impact
====================

* New RPM URLs and repo metadata should be documented so
  people can create their repositories the right way.


References
==========
