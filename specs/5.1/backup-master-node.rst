..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==================
Backup Master Node
==================

https://blueprints.launchpad.net/fuel/+spec/backup+master+node


Because Fuel Master HA is viewed as a waste of a user's resources, we need
to provide value by allowing for backup/recovery for disaster recovery
scenarios. Now that Fuel Master is running on Docker containers, backup and
recovery are quite painless and simple.

Problem description
===================

A detailed description of the problem:

* Fuel Master currently cannot be backed up or restored

* Reconfiguration of the Fuel Master requires significant manual input

Proposed change
===============

Fuel Master backup and recovery can be simplified by use of scripts and a
simple mechanism to compress and save the archive wherever the user requests.

Recovery in its first stage of implementation will be simplified. It will not
include astute.yaml settings (IP addresses, DHCP settings, DNS, NTP, etc). It 
will simply restart the Docker containers to the backed up state.
other words, what's the scope of this effort?

Alternatives
------------

Backup and restore can be done with docker-0.10 without freezing running
containers, but it may result in inconsistent data.

Using docker-0.12 will allow freezing containers to save running state without
any destructive risks.

Data model impact
-----------------

Changes which require modifications to the data model often have a wider impact
on the system.  The community often has strong opinions on how the data model
should be evolved, from both a functional and performance perspective. It is
therefore important to capture and gain agreement as early as possible on any
proposed changes to the data model.

Questions which need to be addressed by this section include:

* None

REST API impact
---------------

Each API method which is either added or changed should have the following

* None

Security impact
---------------

None

Notifications impact
--------------------

None

Other end user impact
---------------------

The user will interact with backup and restore via the dockerctl command
line utility.

Performance Impact
------------------

Minimal. There will be performance hits during backup process, resulting in
downtime.

Other deployer impact
---------------------

Discuss things that will affect how you deploy and configure Fuel
that have not already been mentioned, such as:

* What config options are being added? Should they be more generic than
  proposed? Are the default values ones which will work well in
  real deployments?

Default backup path /var/backup/fuel

* Is this a change that takes immediate effect after its merged, or is it
  something that has to be explicitly enabled?

Yes. Immediate effect, but no backups are automatic.

Developer impact
----------------

Discuss things that will affect other developers working on Fuel,
such as:

* There will be an impact on dockerctl config dependency on container names.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  raytrac3r

Other contributors:
  None

Work Items
----------

Work items or tasks -- break the feature up into the things that need to be
done to implement it. Those parts might end up being done by different people,
but we're mostly trying to understand the timeline for implementation.

* Add backup feature to create archive of all containers, repositories, and
  puppet manifests.
* Add restore feature to overwrite all containers, repositories, and puppet
  manifests.
* Upgrade docker-io to 0.12.
* User documentation on how to backup and restore.
* (Nice to have) backup via rsync, ftp, or http.


Dependencies
============

docker-io-0.12 RPM

Testing
=======

Automated tests for backup/save need to be added to current Fuel system tests.

Documentation Impact
====================

User-facing docs are required to show users the different ways to perform 
the back up and restore.

References
==========

None
