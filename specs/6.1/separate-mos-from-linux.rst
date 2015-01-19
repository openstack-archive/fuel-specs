..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=============================
Separate MOS from Linux repos
=============================

https://blueprints.launchpad.net/fuel/+spec/separate-mos-from-linux

Problem description
===================

To facilitate patching and to make Fuel more modular we need to keep the
operating system separate from MOS and have them external to Fuel. During
the first phase, which is covered by this document, we must separate
Linux distribution and MOS packages into the following repositories:

* repository with vanilla untouched Linux packages
* repository with everything else (repository with other Linux packages,
  OpenStack packages, Fuel packages etc)

Proposed change
===============

This bluprint proposes to modify the following parts of the Fuel build
system:

* local mirrors creation module
* docker containers building module
* ISO assembly module

Local mirrors creation module
-----------------------------

There are two approaches to the mirroring code modification:

* quick-n-dirty: separation MOS and upstream packages based on
  packages source URL (produced by 'yumdownloader --urls' and 
  'apt-get --print-uris').

* slow and correct one: fetch the Fuel packages repository as-is and
  download all other packages from upstream Linux repository into
  a different repository. Requires thorough cleanup of OSCI package
  repositores - we need to keep there only packages that must differ
  from upstream ones.

Either way, packages structure for divided repositories on a local
mirror will look like this:

 fuel-main/local_mirror
 |-- centos-fuel
 |   `-- os
 |       `-- x86_64
 |           |-- images
 |           |-- isolinux
 |           |-- Packages
 |           `-- repodata
 |-- centos-base
 |   `-- os
 |       `-- x86_64
 |           |-- images
 |           |-- isolinux
 |           |-- Packages
 |           `-- repodata
 |-- ubuntu-fuel
 |   |-- dists
 |   |-- images
 |   |-- indices
 |   `-- pool
 `-- ubuntu-base
     |-- dists
     |-- images
     |-- indices
     `-- pool

centos-base and ubuntu-base - contains upstream Linux packages
centos-fuel and ubuntu-fuel - contains all other packages


Docker containers building module
---------------------------------

All Dockerfile configs will be adjusted to include "centos-base"
and "centos-fuel" repositories instead of a current "nailgun" one.


ISO assembly module
-------------------

The structure of separated repositories on a master node:

 /var/www/nailgun
 |-- centos-fuel
 |   `-- fuelweb
 |       `-- x86_64
 |           |-- images
 |           |-- isolinux
 |           |-- Packages
 |           `-- repodata
 |-- centos-base
 |   `-- fuelweb
 |       `-- x86_64
 |           |-- images
 |           |-- isolinux
 |           |-- Packages
 |           `-- repodata
 |-- ubuntu-fuel
 |    `-- fuelweb
 |        `-- x86_64
 |            |-- dists
 |            |-- images
 |            |-- indices
 |            `-- pool
 `-- ubuntu-base
     `-- fuelweb
         `-- x86_64
             |-- dists
             |-- images
             |-- indices
             `-- pool

The following parts must be adjusted:

TBD

Alternatives
------------

None

Data model impact
-----------------

None

REST API impact
---------------

None

Upgrade impact
--------------

Upgrade repositories use their own paths inside /var/www/nailgun, so they
shouldn't be affected.

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
  <launchpad-id or None>

Other contributors:
  <launchpad-id or None>

Work Items
----------

Work items or tasks -- break the feature up into the things that need to be
done to implement it. Those parts might end up being done by different people,
but we're mostly trying to understand the timeline for implementation.


Dependencies
============

* Include specific references to specs and/or blueprints in fuel, or in other
  projects, that this one either depends on or is related to.

* If this requires functionality of another project that is not currently used
  by Fuel, document that fact.

* Does this feature require any new library dependencies or code otherwise not
  included in Fuel? Or does it depend on a specific version of library?


Testing
=======

Please discuss how the change will be tested. It is assumed that unit test
coverage will be added so that doesn't need to be mentioned explicitly,
but discussion of why you think unit tests are sufficient and we don't need
to add more functional tests would need to be included.

Is this untestable in gate given current limitations (specific hardware /
software configurations available)? If so, are there mitigation plans (3rd
party testing, gate enhancements, etc).


Documentation Impact
====================

What is the impact on the docs team of this change? Some changes might require
donating resources to the docs team to have the documentation updated. Don't
repeat details discussed above, but please reference them here.


References
==========

Please add any useful references here. You are not required to have any
reference. Moreover, this specification should still make sense when your
references are unavailable. Examples of what you could include are:

* Links to mailing list or IRC discussions

* Links to relevant research, if appropriate

* Related specifications as appropriate

* Anything else you feel it is worthwhile to refer to
