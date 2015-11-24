..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

============================
FUEL Master Node on CentOS 7
============================

https://blueprints.launchpad.net/fuel/+spec/master-on-centos7


--------------------
Problem description
--------------------

FUEL master nodes up to MOS 7.0 were built on CentOS6 base with many
packages rebuild internally even when there are suitable versions
available in upstream repositories. This becomes a problem since
codebase becomes outdated and there is a growing amount of security
patches that must be applied.

Updating master node to CentOS7 solves the following issues:

* Update system packages (including kernel) to newer versions

* Update core packages (docker, puppet, ruby, openstakc components)
  to newer versions

* Update a lot of other packages to newer versions

* Use upstream repositories with MOS repos together

----------------
Proposed changes
----------------

The proposal is to update all packages that are built internally to versions
from CentOS 7 repositories, then rebuild ISO using CentOS7 base repositories
and updated internal repository. Since updating the packages will affect some
puppet manifests logic they should be updated too.


Web UI
======

None


Nailgun
=======

Python requirements should be updated to work with versions available in
base repo or compatible with OpenStack global requirements.

Data model
----------

None

REST API
--------


Orchestration
=============

RPC Protocol
------------

None


Fuel Client
===========

Python requirements should be updated to support version available from base
repos or be compatible with OpenStack global requirements.



Plugins
=======

None


Fuel Library
============

CentOS 7 uses systemd so puppet manifests should be checked and updated
to be compatible:

* templates for services should be updated

* components that tries to use scripts in /etc/init.d directly should be
  rewritten

* templates for other components should be updated to match configuration
  files from updated packages


------------
Alternatives
------------

None


--------------
Upgrade impact
--------------

There is a separate blueprint that describes update procedure:

https://blueprints.launchpad.net/fuel/+spec/upgrade-master-node-centos7


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

None, or slightly improved performance.


-----------------
Deployment impact
-----------------

CentOS7 uses predictable network interface naming schema, which
is covered by network-interfaces-naming-schemes spec.


----------------
Developer impact
----------------

Developers should update components to support requirements from CentOS7.

---------------------
Infrastructure impact
---------------------

QA infrastructure should be updated to support systemd based ISO.


--------------------
Documentation impact
--------------------

None

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  <None>

Mandatory design review:
  Anastasia Urlapova <aurlapova@mirantis.com>
  Oleg Gelbukh <ogelbukh@mirnatis.com>
  Sergii Golovatiuk <sgolovatiuk@mirantis.com>

Work Items
==========

* Fuel Library

  Review all the changes tagged with 'centos7-master-node' topic, and merge.

* Fuel Main

  Review all the changes tagged with 'centos7-master-node' topic, and merge.

* Fuel OSTF

  Review all the changes tagged with 'centos7-master-node' topic, and merge.

* Fuel Astute

  Review all the changes tagged with 'centos7-master-node' topic, and merge.

* Fuel Web

  Review all the changes tagged with 'centos7-master-node' topic, and merge.


Dependencies
============

None


------------
Testing, QA
------------

None


Acceptance criteria
===================

Custom ISO passes BVT, swarm, and scale tests.


----------
References
----------

None

