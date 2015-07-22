..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=================================================================
MOS APT repositories: URLs, metadata, and other interface details
=================================================================

Improve the API (URLs and metadata) of MOS APT repositories

Problem description
===================

Currently the codename is bound to the MOS release number, that is, the repo
URLs look like (as documented in separate_mos_from_linux_)

::

 deb http://${mirror_host}/mos/centos-6/proposed
 deb http://${mirror_host}/mos/centos-6/security
 deb http://${mirror_host}/mos/centos-6/updates

This stucture yields several issues:
 - it's impossible to distinguish between repositories targeted for different
   Centos versions
 - it's difficult to support per customer repositories
 - it's impossible to distinguish between repositories targeted for fuel and openstack 
   nodes

.. _separate_mos_from_linux: https://github.com/stackforge/fuel-specs/blob/master/specs/6.1/separate-mos-from-linux.rst


Proposed change
===============

Add change the codename to mos${mos_release}-${distro_codename}, so the URLs are

:: 
 http://${mirror_host}/mos-repos/centos/mos${mos_release}-${distro_version}/os/x86_64/
 http://${mirror_host}/mos-repos/${distro}/mos${mos_release}-${distro_version}/updates/x86_64/
 http://${mirror_host}/mos-repos/${distro}/mos${mos_release}-${distro_version}/security/x86_64/
 http://${mirror_host}/mos-repos/${distro}/mos${mos_release}-${distro_version}/holdback/x86_64/


and the repository metadata is

Origin: Mirantis
Codename: mos${mos_release}-${distro_codename}
Label: mos${mos_release}-${distro_codename}
Suite: mos${mos_release}-${distro_codename}${component}

Example: MOS 7.0/trusty
-------------------------

:: 

 deb http://${mirror_host}/mos-repos/ubuntu mos7.0-trusty          main
 deb http://${mirror_host}/mos-repos/ubuntu mos7.0-trusty-security main
 deb http://${mirror_host}/mos-repos/ubuntu mos7.0-trusty-updates  main
 deb http://${mirror_host}/mos-repos/ubuntu mos7.0-trusty-proposed main
 deb http://${mirror_host}/mos-repos/ubuntu mos7.0-trusty-holdback main

The Release files are:

Origin: Mirantis
Codename: mos7.0-trusty
Label: mos7.0-trusty
Suite: mos7.0-trusty{,-security,-updates,-proposed,-holdback}

Example: MOS 7.0/trusty-fuel
----------------------------

:: 

 deb http://${mirror_host}/mos-repos/ubuntu mos7.0-trusty-fuel          main
 deb http://${mirror_host}/mos-repos/ubuntu mos7.0-trusty-fuel-security main
 deb http://${mirror_host}/mos-repos/ubuntu mos7.0-trusty-fuel-updates  main
 deb http://${mirror_host}/mos-repos/ubuntu mos7.0-trusty-fuel-proposed main
 deb http://${mirror_host}/mos-repos/ubuntu mos7.0-trusty-fuel-holdback main

The Release files are:

Origin: Mirantis
Codename: mos7.0-trusty-fuel
Label: mos7.0-trusty-fuel
Suite: mos7.0-trusty-fuel{,-security,-updates,-proposed,-holdback}

Example: Customer 7.0/trusty
----------------------------

:: 

 deb http://${mirror_host}/customer/ubuntu customer7.0-trusty          main
 deb http://${mirror_host}/customer/ubuntu customer7.0-trusty-security main
 deb http://${mirror_host}/customer/ubuntu customer7.0-trusty-updates  main
 deb http://${mirror_host}/customer/ubuntu customer7.0-trusty-proposed main
 deb http://${mirror_host}/customer/ubuntu customer7.0-trusty-holdback main

The Release files are:

Origin: Customer
Codename: customer7.0-trusty
Label: customer7.0-trusty
Suite: customer7.0-trusty{,-security,-updates,-proposed,-holdback}

Advantages:
 - MOS release can target arbitrary number of Ubuntu/Debian versions
   (limited only by available resources).
 - It's possible to create arbitrary number of per customer (or per team)
   APT repositories using codenames and custom url, but still keeping
   the overall structure.
 - It's possible to maintain a separate set of repositories which are
   not intended for OpenStack nodes (say, packages relevant for Fuel master
   node only).

Alternatives
------------

Decouple the codename from the MOS release number and use the OpenStack
release codename instead, i.e

deb http://${mirror_host}/mos-repos/ubuntu kilo-trusty main

Data model impact
-----------------

Default set of APT repositories for OpenStack nodes should be changed.

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

EXTRA_DEB_REPOS should provide a compatible metadata in order for repo
priorities to work properly.

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

* New APT URLs and repo metadata (Release files) should be documented so
  people can create their repositories the right way.


References
==========
