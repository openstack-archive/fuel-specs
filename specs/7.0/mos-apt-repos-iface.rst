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

We need to have a kind of transactional mechanism for updating repository
suites. Every time when we re-build one of deb packages we create
so called snapshot repository which is guaranteed to be consistent once its
creation has finished. All snapshot repositories are avilable under:

  mos-repos/ubuntu/dists/snapshots/{suite}-{timestamp}

All these repositories contain everything that we need to use this repositories
in isolation, inculding their own pool with all the packages listed in all
repository sections like main, restricted, etc.

  mos-repos/ubuntu/dists/snapshots/{suite}-{timestamp}
    main/
    resticted/
    pool/
    Release
    Release.gpg

Every new snapshot repository is based on the previous one in the sense that
we override only those packages that are re-built for the snapshot. All other
packages are the same. It is like a chain where every new link is almost the
same but differs in several packages.

From all said above it follows that we need
to have a kind of de-duplication mechanism to reduce the disk space necessary
for storing all these separate pools. So, instead of copying all the packages
every time when we create new snapshot repository, we create a set of
hardlinks to all those packages that are the same as in previous snapshot.

It is necessary to note that we can not use common pool as a de-duplication
mechanism. Technically every new snapshot is just another instance of the same
suite and standard deb tools like ``reprepro`` can not bind several
versions of a particular package to the same suite. However, this problem
seems potentially solvable (needs additional research).
Common pool works well when we have more than one suite referencing to the
same package. It allows to avoid having two (more) copies of the package
like we have in case of separate pools. Besides, we still don't have working
mechanism to increment package versions every time when we re-build them.
So, it is like two different package versions with the same name. Obviously,
we can not put such packages into one common pool. This issue is going to
be addressed by 8.0.

However, the thing is that we can not use snapshot repositories directly
because Codename defined in the Release file is {suite} not
snapshots/{suite}-{timestamp}, i.e. we can not use this source

  deb http://{host}/mos-repos/ubuntu snapshots/{suite}-{timestamp} {sections}

Fortunately, we can use symlinks like the following:

  mos-repos/ubuntu/dists/{suite} -> snapshots/{suite}-{timestamp}

That link can be used directly, but we also need to take into account
the fact that we create more than 100 new snapshots every day.
So, if we update a particuar link
every 10 minutes it will be barely possible to use this link as
a deb source, because the link might be updated while apt-get is running.
It is common situation for unstable upstream repositories like debian sid,
but it is not so critical there, because sid is usually updated 3 times a
day not 100.

So, we'd better have one quasi-stable link which is going to be updated
not more than 4 times a day

  mos-repos/ubuntu/dists/{suite} -> snapshots/{suite}-{timestamp}

And a set of links for every snapshot but that are to be used directly. We
need this for development purposes.

  mos-repos/ubuntu/dists/ubuntu/{suite}-{timestamp}/dists/{suite} ->
    snapshots/{suite}-{timestamp}

In order to get the latest link we need to have a kind of dereference
mechanism. For example, it can be plain text file

  mos-repos/ubuntu/dists/{suite}.target.txt

with the content like ``snapshots/{suite}-{timestamp}`` pointing to the latest
available snapshot. We then can use this content to create the root repository
path like ``mos-repos/ubuntu/dists/ubuntu/{suite}-{timestamp}/dists/{suite}``.

Besides, using symlinks makes it possible to update repositories in a
transactional way. Once new snapshot is consistent and ready to use we
update repository symlink. If something goes wrong we can easily revert
the symlink to the previous state.

Updating steps:

  - create new snapshot (based on previous one + new packages)
  - update suite symlink to the new snapshot
  - revert suite symlink to the previous state (if it is needed)

Deb sources:
  - current (quasi-stable):
    deb http://{host}/mos-repos/ubuntu {suite} main restricted

  - dereferenced snapshot:
    deb http://{host}/mos-repos/ubuntu/dists/{suite}-{datetime} main restricted


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
