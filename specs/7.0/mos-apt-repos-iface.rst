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

The APT URLs and repository metadata is kind of an API (a contract between
the repo users and its maintainers). Quite a lot of Fuel components depend
on this interface. Building IBP target images, bootstrap images, and regular
OpenStack deployment is going to break if APT URLs or repository metadata
(such as a codename) gets changed.

Currently the codename is bound to the MOS release number, that is, the repo
URLs look like (as documented in separate_mos_from_linux_)

::

 deb http://${host}/mos/ubuntu mos${version}          main
 deb http://${host}/mos/ubuntu mos${version}-security main
 deb http://${host}/mos/ubuntu mos${version}-updates  main
 deb http://${host}/mos/ubuntu mos${version}-proposed main
 deb http://${host}/mos/ubuntu mos${version}-holdback main

This stucture yields several issues:
 - it's impossible to distinguish between repositories targeted for different
   Ubuntu versions (i.e. for trusty and vivid)
 - it's impossible to distinguish between Ubuntu and Debian
 - it's difficult to support per customer repositories

.. _separate_mos_from_linux: https://github.com/stackforge/fuel-specs/blob/master/specs/6.1/separate-mos-from-linux.rst


Proposed change
===============

Change the codename to mos${version}[-${distro_codename}], so the URLs are

:: 

 deb http://${host}/mos-repos/${distro}/{version} mos${version}          main
 deb http://${host}/mos-repos/${distro}/{version} mos${version}-security main
 deb http://${host}/mos-repos/${distro}/{version} mos${version}-updates  main
 deb http://${host}/mos-repos/${distro}/{version} mos${version}-proposed main
 deb http://${host}/mos-repos/${distro}/{version} mos${version}-holdback main

and the repository metadata is

Origin: Mirantis
Codename: mos${version}
Label: mos${version}
Suite: mos${version}-${component}

Example: MOS 7.0
-------------------------

:: 

 deb http://${host}/mos-repos/ubuntu/7.0 mos7.0          main
 deb http://${host}/mos-repos/ubuntu/7.0 mos7.0-security main
 deb http://${host}/mos-repos/ubuntu/7.0 mos7.0-updates  main
 deb http://${host}/mos-repos/ubuntu/7.0 mos7.0-proposed main
 deb http://${host}/mos-repos/ubuntu/7.0 mos7.0-holdback main

The Release files are:

Origin: Mirantis
Codename: mos7.0
Label: mos7.0
Suite: mos7.0{,-security,-updates,-proposed,-holdback}

Example: MOS 7.0/vivid
-------------------------

:: 

 deb http://${host}/mos-repos/ubuntu/7.0 mos7.0-vivid          main
 deb http://${host}/mos-repos/ubuntu/7.0 mos7.0-vivid-security main
 deb http://${host}/mos-repos/ubuntu/7.0 mos7.0-vivid-updates  main
 deb http://${host}/mos-repos/ubuntu/7.0 mos7.0-vivid-proposed main
 deb http://${host}/mos-repos/ubuntu/7.0 mos7.0-vivid-holdback main

The Release files are:

Origin: Mirantis
Codename: mos7.0-vivid
Label: mos7.0-vivid
Suite: mos7.0-vivid{,-security,-updates,-proposed,-holdback}

Example: MOS 7.0/vivid-fuel
----------------------------

:: 

 deb http://${host}/mos-repos/ubuntu/7.0 mos7.0-vivid-fuel          main
 deb http://${host}/mos-repos/ubuntu/7.0 mos7.0-vivid-fuel-security main
 deb http://${host}/mos-repos/ubuntu/7.0 mos7.0-vivid-fuel-updates  main
 deb http://${host}/mos-repos/ubuntu/7.0 mos7.0-vivid-fuel-proposed main
 deb http://${host}/mos-repos/ubuntu/7.0 mos7.0-vivid-fuel-holdback main

The Release files are:

Origin: Mirantis
Codename: mos7.0-vivid-fuel
Label: mos7.0-vivid-fuel
Suite: mos7.0-vivid-fuel{,-security,-updates,-proposed,-holdback}

Example: Customer 7.0
----------------------------

:: 

 deb http://${host}/customer/ubuntu/7.0 customer7.0          main
 deb http://${host}/customer/ubuntu/7.0 customer7.0-security main
 deb http://${host}/customer/ubuntu/7.0 customer7.0-updates  main
 deb http://${host}/customer/ubuntu/7.0 customer7.0-proposed main
 deb http://${host}/customer/ubuntu/7.0 customer7.0-holdback main

The Release files are:

Origin: Customer
Codename: customer7.0
Label: customer7.0
Suite: customer7.0{,-security,-updates,-proposed,-holdback}

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

deb http://${host}/mos-repos/ubuntu/7.0 kilo-trusty main

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

We need to update every release in transaction way.
Each release should be a symlink to particular snapshot:

  mos-repos/ubuntu/{version} -> snapshots/{version}-{datetime}
  mos-repos/ubuntu/snapshots/{version}-{datetime}

Each snapshot should contain all the data related to corresponding relese::

  mos-repos/ubuntu/snapshots/{version}-{datetime}/
   ├─ dists
   │  ├─ mos7.0
   │  │  ├─ main
   │  │  ├─ resticted
   │  │  ├─ Release
   │  │  └─ Release.gpg
   │  └─ mos7.0-updates
   │     ├─ main
   │     ├─ resticted
   │     ├─ Release
   │     └─ Release.gpg
   └─ pool

Updating steps:

  - create new snapshot:
    snapshots/{version}-{newdatetime}/{dists,pool} based on previous one
    (in order to reduce uploading traffic, all unchanged files will be
    linked from previous snapshot with ``rsync --link-dest`` option)

  - update {version} symlink to new snapshot
    {version} -> snapshots/{version}-{newdatetime}

As far as current development suite is updating very often (up to ten times
per minute), we need a way to freeze its state for all CI processes.
We could use snapshots as freezed suite state. Just dereference current
suite symlink to actual snapshot.
In order to get the actual target of symlink we need to have a kind of
dereference mechanism. It can be plain text file in the same directory:

  - mos-repos/ubuntu/{version}.target.txt

which contains target of {version} symlink:

  - ``snapshots/{version}-{timestamp}``

We could use this value instead of symlink:

  - current repository string:
    deb {host}/mos-repos/ubuntu/{version} {suite} main

  - dereference suite symlink:
    {version} -> snapshots/{version}-{datetime}

  - new repository string:
    deb {host}/mos-repos/ubuntu/snapshots/{version}-{datetime} {suite} main


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
