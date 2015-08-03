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

 deb http://${mirror_host}/mos/ubuntu mos${mos_release}          main restricted
 deb http://${mirror_host}/mos/ubuntu mos${mos_release}-security main restricted
 deb http://${mirror_host}/mos/ubuntu mos${mos_release}-updates  main restricted
 deb http://${mirror_host}/mos/ubuntu mos${mos_release}-proposed main restricted
 deb http://${mirror_host}/mos/ubuntu mos${mos_release}-holdback main restricted

This stucture yields several issues:
 - it's impossible to distinguish between repositories targeted for different
   Ubuntu versions (i.e. for trusty and vivid)
 - it's impossible to distinguish between Ubuntu and Debian
 - it's difficult to support per customer repositories

.. _separate_mos_from_linux: https://github.com/stackforge/fuel-specs/blob/master/specs/6.1/separate-mos-from-linux.rst


Proposed change
===============

Change the codename to mos${mos_release}-${distro_codename}, so the URLs are

:: 

 deb http://${mirror_host}/mos-repos/${distro} mos${mos_release}-${distro_codename}          main
 deb http://${mirror_host}/mos-repos/${distro} mos${mos_release}-${distro_codename}-security main
 deb http://${mirror_host}/mos-repos/${distro} mos${mos_release}-${distro_codename}-updates  main
 deb http://${mirror_host}/mos-repos/${distro} mos${mos_release}-${distro_codename}-proposed main
 deb http://${mirror_host}/mos-repos/${distro} mos${mos_release}-${distro_codename}-holdback main

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

We need to update every suite in transaction way.
Each suite should be a symlink to particular snapshot:

  mos-repos/ubuntu/dists/{suite} -> snapshots/{suite}-{datetime}
  mos-repos/ubuntu/dists/snapshots/{suite}-{datetime}

Each snapshot should contain all the data related to corresponding suite

  mos-repos/ubuntu/dists/snapshots/{suite}-{datetime}/
     main/
     resticted/
     pool/
     Release
     Release.gpg

Updating steps:

  - create new snapshot:
    snapshots/{suite}-{newdatetime}/{main,resticted,pool,Release*} based on
    previous one (in order to reduce uploading traffic, all unchanged files
    will be linked from previous snapshot with ``rsync --link-dest`` option)

  - update {suite} symlink to new snapshot
    dists/{suite} -> snapshots/{suite}-{newdatetime}

As far as current development suite is updating very often (up to ten times
per minute), we need a way to freeze its state for all CI processes.
We could use snapshots as freezed suite state. Just dereference current
suite symlink to actual snapshot.
In order to get the actual target of symlink we need to have a kind of
dereference mechanism. It can be plain text file in the same directory:

  - mos-repos/ubuntu/dists/{suite}.target.txt

which contains target of {suite} symlink:

  - ``snapshots/{suite}-{timestamp}``

We could use this value instead of symlink:

  - current repository string:
    deb {host}/mos-repos/ubuntu {suite} {components}

  - dereference suite symlink:
    {suite} -> snapshots/{suite}-{datetime}

  - new repository string:
    deb {host}/mos-repos/ubuntu snapshots/{suite}-{datetime} {components}

But we can't use such repository string because of given suite name
``snapshots/{suite}-{datetime}`` doen't match with ``Suite`` tag at Release
file, which doesn't meet Debian the repository structure requirements.

To resolve the above issue we need to move "snapshots" naming approach
from distribution to base section.
We can create additional folder structure:

  - dists/{suite} -> snapshots/{suite}-{datetime}

  - snapshots/{suite}-{datetime}

  - snapshots/ubuntu/{suite}-{datetime}/dists/{suite} -> snapshots/{suite}-{datetime}

In this case we could use snapshots in a way:

  - current repository string:
    deb {host}/mos-repos/ubuntu {suite} {components}

  - dereference suite symlink:
    {suite} -> snapshots/{suite}-{datetime}
    append URI with `/snapshots/ubuntu/{suite}-{datetime}`

  - new repository string:
    deb {host}/mos-repos/ubuntu/snapshots/ubuntu/{suite}-{datetime} {suite} {components}

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
