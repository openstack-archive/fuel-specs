..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

================================================
Add VMware clusters to operational's environment
================================================

https://blueprints.launchpad.net/fuel/+spec/add-vmware-clusters

Fuel supports add and remove nodes after deploy to extend existing and
operational environment. However this functionality works only for compute
nodes with KVM hypervisor.

--------------------
Problem description
--------------------

If you use an operational environment with VMware vSphere as a hypervisor and
you'd like to extend it, you can add a new compute-vmware node to the
environment. Once done, you will have to assign this node to the cluster and
configure it as follows:

::

   - datastore_regex: .*
     service_name: sn1
     target_node:
       current:
         id: node-2
         label: node-2
       options:
       - id: controllers
         label: controllers
       - id: node-2
         label: Untitled (54:fb) (4b:54:fb)
     vsphere_cluster: Cluster1

Nevertheless, this is not possible because Nailgun doesn't allow chanding
any VMware settings after deploy. Since new cluster wouldn't assigned to new
compute-vmware node this node will misconfigured.

----------------
Proposed changes
----------------

Allow changing list of vSphere's clusters after deploy similar as it done with
list of ubuntu repositories. [1]

Web UI
======

Nova Compute Instance on the Fuel Web UI should be left unlocked after
deployment.

Nailgun
=======

Nailgun shoud allow changing vmware settings after deployment.

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

None?


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

User should add compute-vmware node as usual and has to set special data in to
the postgres database directly.

--------------
Upgrade impact
--------------

None

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

None

--------------------
Documentation impact
--------------------

This feature should be described in the documentation.

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee: Igor Gajsin <igajsin@mirantis.com>

Other contributors:Elena Kosareva <ekosareva@mirantis.com>

Mandatory design reviewer:
  Aleksandr Kislitskii <akislitsky@mirantis.com>,
  Ivan Kliuk <ikliuk@mirantis.com>, Maciej Kwiek <mkwiek@mirantis.com>


Work Items
==========

* Do proof of concept. Add a cluster manually.
* Unlock nailgun and add cluster via CLI Fuel client.
* Add cluster using Fuel Web UI.

Dependencies
============

None

------------
Testing, QA
------------

New test should be written which covers this scenario:

1. Create VMware related environment with 1 cluster.

#. Deploy this environment and make OSTF check.

#. Add new compute-vmware node and assign it with new cluster on vSphere.

#. Deploy changes and make OSTF check again.

Acceptance criteria
===================

The test which described above should pass.

----------
References
----------

[1] Example for unlocked after deploy Fuel Web UI elements
  (https://goo.gl/senW2j)
