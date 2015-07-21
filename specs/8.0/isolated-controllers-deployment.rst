..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===========================================================
Deploy controllers in isolation from environment's networks
===========================================================

https://blueprints.launchpad.net/fuel/+spec/example

Highly available reference architecture of OpenStack that is created by Fuel
installer implies that OpenStack Controllers are tightly coupled to each other
and coordinated by multiple clustered services:

* corosync

* galera

* haproxy

In addition, Virtual IP addresses are used to provide common endpoints for
services in the cluster.

In-place upgrade scenario without creating the new environment implies that
parallel control plane is created and then the cluster switches to the new
control plane. This requires that new instances of clustered services are
created and attached to the same VIPs.

To avoid network conflicts between control planes, we must deploy the new
control plane separately from the old one.

--------------------
Problem description
--------------------

A detailed description of the problem:

* Duplicate control plane in a single environment without some kind of
  isolation creates multiple problems and simply render the environment
  completely unusable.

* Controller nodes cannot be deployed in isolation from each other as they
  run clustered software that has to communicate to install properly.
  The same is true for most of OpenStack services.

* Switchover to upgraded control plane has to be as seamless as possible not
  to cause service interruptions.

----------------
Proposed changes
----------------

* Reinstall Controllers in special isolation mode, without connection to
  physical networks, at least ones that have VIPs assigned to them.

** Specify 'isolated' deployment mode as a flag passed in deployment call.

** Automatically identify if 'isolated' mode is required based on compoistion
   of nodes and configuration of cluster.

** Support isolated deployment mode in Nailgun by changing serializers for
   deployment facts:

*** Don't add patch ports in network scheme

*** Don't include nodes with the old release version into list of nodes


Web UI
======

No impact.

Nailgun
=======

General changes to the architecture, tasks and encapsulated business logic
should be described here.

Data model
----------

We plan to utilize existing data model by using parameters that allow to
change the release ID of cluster and other elements of the model.

We shall add the following parameters to Node object:

* ``release_id`` is an ID number of the release which was used to deploy the
  node. This parameter will allow for selective serialization and grouping of
  nodes. Release ID will be assigned to every existing node by Nailgun DB
  migration scrips of version 8.0. Nailgun will set this parameter to any new
  node based on release ID of the cluster it is added to.

REST API
--------

None.

Orchestration
=============

Primary controller shall be reinstalled with no connection to existing
controllers and shall not join existing Corosync and Galera clusters. To
achieve that, we propose to exclude nodes other than the primary controller
from orchestrator serialization for reinstallation of the primary controller.


RPC Protocol
------------

TBD.

Fuel Client
===========

None.

Plugins
=======

Plugins shall not be affected by this change. However, plugins upgrade
mechanisms should be compatible with the isolated deployment of the primary
and/or other controllers.


Fuel Library
============

None.

------------
Alternatives
------------

Currently implemented alternative to the described mechanism of isolated
deployment is isolation ensured by external script that runs in between
provisioning and deployment stages of installation of the primary controller.

This method will be used as a backup if the described changes won't land in 8.0
release cycle.

The alternative that we're going to pursue in future is maintaining the
control plane through the whole upgrade process. In this case, upgraded
controllers will rejoin the existing clusters. We'll need to solve problems
with compatibility between older and newer versions of clustered software (i.e.
galera, corosync and rabbitmq).

--------------
Upgrade impact
--------------

This change suggests a way to upgrade software on the controller node.

---------------
Security impact
---------------

None.

--------------------
Notifications impact
--------------------

None.

---------------
End user impact
---------------

End users won't have direct access to deployment in isolated mode. There
is no separate API call that allows to specify mode of deployment.

------------------
Performance impact
------------------

None.

-----------------
Deployment impact
-----------------

Isolated deployment mode will be used to reinstall primary controller in
upgraded environment. This will provide a method to deploy new version of
OpenStack, in addition to standard path to deploy from scratch on the
clean hardware.

----------------
Developer impact
----------------

None.

--------------------------------
Infrastructure/operations impact
--------------------------------

System test and corresponding Jenkins job shall be implemented to verify
the integrity of isolated deployment.

--------------------
Documentation impact
--------------------

Modified workflow for upgrade of Control Plane shall be described in
corresponding section of Environment Upgrade chapter of Operations Guide.

--------------------
Expected OSCI impact
--------------------

None.

--------------
Implementation
--------------

Assignee(s)
===========

Who is leading the writing of the code? Or is this a blueprint where you're
throwing it out there to see who picks it up?

If more than one person is working on the implementation, please designate the
primary author and contact.

Primary assignee:
  gelbuhos (Oleg S. Gelbukh)

Other contributors:
  akscram (Ilya Kharin)
  yorik-sar (Yuriy Taraday)
  sryabin (Sergey Ryabin)

Mandatory design review:
  dborodaenko (Dmitriy Borodaenko)


Work Items
==========

* Modify facts serializers to exclude all nodes except the upgraded controller

* Modify network scheme serializers to exclude patch ports for isolated
  deployment mode

Dependencies
============

TBD.

------------
Testing, QA
------------

System test should be created to verify the isolated deployment success and
integrity.

Acceptance criteria
===================

* Default deployment information is available for a node with role 
  'primary-controller' when the environment is in 'upgrade' status.

* Default deployment information doesn't contain facts of other nodes in the
  environment.

* Default deployment information contains 'network_schema' section with no
  patch ports connecting logical bridges to physical interfaces (for ovs), or
  no actions that add physical interfaces to logical bridges (for linux
  bridge).

* Controller with 'primary-controller' role reinstalled in the same environment
  after its settings are upgraded by fuel-upgrade script.

* Reinstalled controller node is isolated from networks where Virtual IP
  addresses are configured. VIPs are up and running on the reinstalled
  controller.

----------
References
----------

Please add any useful references here. You are not required to have any
reference. Moreover, this specification should still make sense when your
references are unavailable. Examples of what you could include are:

* Links to mailing list or IRC discussions

* Links to relevant research, if appropriate

* Related specifications as appropriate

* Anything else you feel it is worthwhile to refer to
