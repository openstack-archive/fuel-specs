..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Separate logs from /var on Fuel Master
==========================================

https://blueprints.launchpad.net/fuel/+spec/fuel-master-separate-logs

Create separate partition for /var/log in order to isolate logs from
other data on the Fuel Master to avoid service interruptions.


Problem description
===================

Many services can be disrupted if /var partition fills up. A list of issues
includes:

* Corruption of postgres DB
* Corruption of ext4 filesystem inside Docker container
* Read-only mount of Docker containers
* Corruption of SQLite DB of docker
* Corruption of devicemapper metadata used by Docker
* Diagnostic snapshot fails to write
* pidfiles for services cannot be written

Solving each of these issues is possible and documented, but the root cause is
unchecked growth of logs data filling up the /var partition.

Proposed change
===============

Create new partition for /var/log during Fuel Master installation. The
intended result is the following breakdown of disk space:
* 10GB root filesystem (/) (unchanged)
* 2-4gb swap (unchanged)
* Greater of 5gb or 30% of remaining disk space for /var
* Greater of 5gb or 40% of remaining disk space for /var/log
* 1GB for Docker metadata*
* Greater of 8gb or 30% of remaining disk space for Docker main data*

(* Docker changes tracked in https://blueprints.launchpad.net/fuel/+spec/dedicated-docker-volume-on-master)

This change will not be made available to existing installations and will
not be applied during Fuel Master upgrade.

Alternatives
------------

There may be other ways to impose quotas on rsyslog and logrotate, but it
generally runs as root user, both of which cannot be restricted.
The other option is to simply avoid creating a new partition for /var/log.
It would be possible to move just Docker data out of /var, but the Docker
SQLite DB is still vulnerable in this case.

Data model impact
-----------------

None

REST API impact
---------------

None

Upgrade impact
--------------

This feature is not possible to automatically implement during upgrades
because it is not possible to reduce the size of the XFS partition of
/var for versions of Fuel below 6.1. This is an XFS limitation.
The only workaround is to copy the data to an external disk,
recreate the logvol and filesystem. This process is delicate and could
be documented, but not automated safely.

That having been said, docker daemon args will vary between new installations
and upgraded installations. There is already a distinction in fuel-library
for the host Puppet manifests which provides this.

Security impact
---------------

None

Notifications impact
--------------------

None

Other end user impact
---------------------

None

Performance Impact
------------------

None

Other deployer impact
---------------------

None

Developer impact
----------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  Matthew Mosesohn <mmosesohn@mirantis.com>

Other contributors:
  None

Work Items
----------

* Create new /var/log logvol in installation

Dependencies
============

* Related blueprint https://blueprints.launchpad.net/fuel/+spec/dedicated-docker-volume-on-master

Testing
=======

The test can be confirmed by creating a large file in /var/log and ensuring
that no services  are interrupted. Such a test would include deploying a
new OpenStack environment.

Beyond a simple check here, the existing test suites in place are adequate
to validate this spec.

Documentation Impact
====================

A manual conversion document will be added to the Operations Guide for Fuel
in order to allow those who wish to manually adjust their systems to take
advantage of this feature.

References
==========

Relevant bug https://bugs.launchpad.net/bugs/1383741
