..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

================================================
Add VMware clusters to operational's environment
================================================

https://blueprints.launchpad.net/fuel/+spec/add-vmware-clusters

Fuel supports adding and removing nodes after deployment to extend existing and
operational environment. However this functionality works only for compute
nodes with KVM hypervisor.

--------------------
Problem description
--------------------

If there's an operational environment with VMware vSphere for hypervisor and
we'd like enlarge it. We should do 4 steps for it:

#. Create a new cluster on vSphere and add esxi nodes to it.

#. Add a new compute-vmware node to the environment.

#. Put data in the Nailgun: 'datastore_regex', 'service_name', 'target_node'
   and 'vsphere_cluster'. Where 'target_node' is id of new node and
   'vsphere_cluster' is the name of new vSphere cluster.

#. Deploy the new node. It will be configured to serve the new cluster since
   we've assigned 'vsphere_cluster' to 'target_node'.

The problem is that we can't accomplish step 3 because Nailgun doesn't
provide any changes of VMware settings after deployment. Without information
about the new cluster the compute-vmware node can't be configured properly.

----------------
Proposed changes
----------------

Allow to change the list of vSphere's clusters after deployment similar to the
way it's done for Ubuntu repositories. [1]

Web UI
======

There are Nova Compute Instance sections on VMware tab of the Fuel Web UI for
setting vSphere cluster's data. And there are buttons "+" and "-" which allow
to add or remove these sections. Now these buttons are locked after deployment.

We want to unlock them when pending addition or deletion of the node with role
compute-vmware in the environment.


Nailgun
=======

There are two changes from nailgun side:

#. Modification of PUT '/api/v1/clusters/<:id>/vmware_attributes' handler to
   allow user modified cluster VMWare Atrributes for locked cluster if there
   are any 'compute-vmware' nodes pinding for addition/deletion.

#. Add validation of input vmware_attributes data.

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

Primary assignee:
  Igor Gajsin <igajsin@mirantis.com>

Other contributors:
  Nailgun part: Elena Kosareva <ekosareva@mirantis.com>
  UI part: Anton Zemlyanov <azemlyanov@mirantis.com>
  QA section:Olesia Tsvigun <otsvigun@mirantis.com>

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
