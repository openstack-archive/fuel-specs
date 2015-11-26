..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

================================================
Add VMware clusters to operational's environment
================================================

https://blueprints.launchpad.net/fuel/+spec/add-vmware-clusters

Fuel supports add and remove nodes after deploy to extend existing and
operational environment. However this functionality works only for KVM-only
environments.

--------------------
Problem description
--------------------

Let's an user has an operational environment which uses VMware vSphere as a
hypervisor and wants to extend it. He can create new cluster on vSphere and add
some esxi hosts in it. He can add new compute-vmware node to the environment.
After that he has to assign this node to the cluster and configure it like that

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

But he can't do it  due to the fact that nailgun doesn't provide change vmware
settings after deploy. New compute-vmware node should deploy but it would
complete useless.

----------------
Proposed changes
----------------

Allow changing list of vSphere's clusters after deploy similar as it done with
list of ubuntu repositories.

Web UI
======

Nova Compute Instance on the Fuel Web UI should be keep unlock after
deployment.


Nailgun
=======

Nailgun shoud allow changing some data after deploy.

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

Primary assignee: Igor Gajsin

Other contributors:Elena Kosareva

Mandatory design review: Alexander Arzhanov


Work Items
==========

* Do proof of concept. Add cluster manually.
* Unlock nailgun and add cluster by the proper way.


Dependencies
============

None


------------
Testing, QA
------------

Special test for add cluster after deployment should be written and add to
ostf.


Acceptance criteria
===================

The test which described above should pass.


----------
References
----------

None
