..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=========================================
Containerized Control Plane on Kubernetes
=========================================

https://blueprints.launchpad.net/fuel/+spec/ccp

This is a meta specification to describe in details creation of the new
experimental project under the Fuel project umbrella to provide to users
Containerized OpenStack deployment on top of Kubernetes, codename
"Fuel CCP".

--------------------
Problem description
--------------------

Containerized Control Plane (CCP) is the initiative to package OpenStack
services in the containers and use standard container management framework to
run and manage them. It includes following areas, but not limited to them:

* OpenStack containerization and container image building tooling
* CI/CD to produce properly layered and versioned containers for the supported
  stable and current master branches of OpenStack projects
* OpenStack deployment in containers on top of Kubernetes with HA for OpenStack
  services and their dependencies (e.g. MySQL, RabbitMQ, etc.)
* Tooling for deploying and operating OpenStack clusters with support for the
  upgrades, patching, scaling and changing configuration

Fuel CCP governance will be a separate experimental project under the openstack
git namespace with unique specs and core team. There is no intention right now
to apply for the Big Tent. The nearest example of the same governance is 3rd
party Fuel plugin done not by Mirantis that aren't under Big Tent and not
controlled by the main Fuel core team.

Separate Launchpad project will be used for the blueprints and bugs management.
Fuel's main IRC channels will be initially used for communication (#fuel and
#fuel-dev) and there will be weekly sub-team meetings as part of the main Fuel
weekly IRC meetings.

CCP is to be a set of repositories with Docker image definitions together with
Kubernetes applications definitions. It is a single git repository per
OpenStack component plus few repositories with related software, tooling,
such as 3rd party CI config, installer and etc. We’re going to start with the
minimal set of the repositories for the “core” OpenStack implementation plus
logging and monitoring implementation based on the existing Stacklight [0]_
[1]_ expertise. The CI system will use upstream infra CI as much as possible
and 3rd party CI for running end-to-end deployment tests.

The initial list of repositories for CCP initiative:

* fuel-ccp (main repo, image build tool, app framework, tooling)
* fuel-ccp-specs
* fuel-ccp-installer
* fuel-ccp-tests
* fuel-ccp-ci-config (~ project-config for 3rd party CI)
* fuel-ccp-debian-base
* fuel-ccp-openstack-base
* fuel-ccp-entrypoint
* fuel-ccp-mariadb
* fuel-ccp-keystone
* fuel-ccp-glance
* fuel-ccp-memcached
* fuel-ccp-horizon
* fuel-ccp-neutron (incl. ovs)
* fuel-ccp-rabbitmq
* fuel-ccp-nova
* fuel-ccp-stacklight (LMA stack)

Each repository will have it's own core reviewers team and there will be one
general core reviewers team with permissions in all repositories.

----------------
Proposed changes
----------------

None. There will be no changes to the existing Fuel projects now.

Web UI
======

None. There is no intention to integrate with Web UI on the early stages of
the initiative.


Nailgun
=======

None. There is no intention to integrate with Nailgun on the early stages of
the initiative.

Data model
----------

None


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

This spec is actually describes an alternative experimental approach for
OpenStack deployment, but there are few questions to answer about alternatives.


1. Why not use Kolla's container images?
   There is a set of fundamental requirements for container images that is
   currently not covered or controversial to some Kolla development principles.
   This list    will be maintained and discussed with Kolla community under
   the following specification published to Kolla project:
   I18b319cb796192a1e61ecd516a485dc82d52652f

2. Why not contribute to Kolla-Kubernetes?
   It's based on the Kolla container images, while we need to solve list of
   requirements described in I18b319cb796192a1e61ecd516a485dc82d52652f

--------------
Upgrade impact
--------------

It'll be separate activity to define migration path from current to the
Kubernetes / CCP based OpenStack version.

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

Separate 3rd party CI will be used to run end-to-end tests.

--------------------
Documentation impact
--------------------

Separate documentation will be needed for CCP initiative.

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  slukjanov

Other contributors:
  None

Mandatory design review:
  None


Work Items
==========

None

Dependencies
============

None

-----------
Testing, QA
-----------

None

Acceptance criteria
===================

None

----------
References
----------

.. [0] https://www.mirantis.com/blog/stacklight-logging-monitoring-alerting-lma-toolchain-mirantis-openstack/
.. [1] https://www.youtube.com/watch?v=JF1BKgH9uco
