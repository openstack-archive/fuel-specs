..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===============
Fuel LCM plugin
===============

-------------------
Problem description
-------------------

The Fuel project does a very good job at initial cluster deployment and
configuration, but it lacks tools for supporting an already deployed
cluster. Users will require a way to apply different fixes to the working
cluster nodes, install updates, make changes and even add new services
as well as auditing the currently running configuration.

----------------
Proposed changes
----------------

The Life Cycle Management plugin should make it possible for the cluster
operators to use a custom Puppet manifests on the deployed cluster nodes.
In order to achieve this goal a new type of the cluster nodes is introduced:
LCM controller. This node can be deployed standalone or there can be several
of them working as a HA cluster with load balancing.

On the LCM nodes the Puppet master should be installed and all other cluster
nodes should run Puppet agents against these Puppet master. Puppet masters
should be able to use the existing Puppet modules which are being used during
the Fuel deployment process as well as any additional Puppet modules and
manifests a user will be willing to add.

There manifests can be assigned to nodes using the Foreman dashboard. It
allows user to add any of the defined Puppet manifests to nodes as well as
to set the parameters for them. Manifests can also get cluster configuration
information from the Hiera yaml files. These files will have to be gathered
from the entire cluster as stored in a centralized database.

The Puppet modules and manifests used to manage the cluster configuration
can be stored in a separate Git repository. The LCM nodes should download
the latest changes and add them to the Puppet master modules when requested.

If there are several LCM nodes installed they should spread the Puppet agent
connection between each other and the load balancer should be able to stop
sending new connections to a failed or disabled LCM node and let the other
nodes to take over the workload.

Nailgun
=======

This plugin required ad addition the the nailgun Web UI called "tuningbox".
It adds a new tab to the cluster settings containing the configuration
options for the LCM plugin.

The centralized database "ConfigDB" used to store the collected Hiera yaml
data will also be installed on the master node.

Data model
----------

The additions to the cluster settings are stored in the Nailgun database.

REST API
--------

None

Orchestration
=============

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

The LCM plugin is using a lot of the Fuel Library modules and manifests
during its deployment and the manifests used to manage the servers can
be based of the Fuel tasks too.

--------------
Upgrade impact
--------------

It should be possible to upgrade the LCM nodes by installing the newer version
of the plugin by running the deployment on them again or by any other means.

---------------
Security impact
---------------

The security of the new LCM controller nodes and the ConfigDB service on the
master node should be audited.

--------------------
Notifications impact
--------------------

None

---------------
End user impact
---------------

End user will be able to use the Web Dashboard on the LCM nodes to upload and
run custom manifests on the running cluster.

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

There should be CI tasks to run the deployment and destructive tests
of the new plugin nodes.

--------------------
Documentation impact
--------------------

The plugin should include documentation about its installation, usage,
architecture and development.

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  Alexey Odinokov

Other contributors:
  Aleksandr Kolinko  
  Aleksey Kolodyazhnyy  
  Alexander Noskov
  Alexei Vinogradov  
  Alexey Chekunov
  Alexey Odinokov
  Dmitriy Stremkovskiy  
  Dmitry Ilyin
  Dzmitry Stremkouski  
  Scott Brimhall
  Sergey Levchenko  
  Sergey Ryabin
  Stas Egorov
  Vasiliy Pleshakov  
  Vladimir Maliaev
  Yuriy Taraday

Mandatory design review:
  Alexey Odinokov

Work Items
==========

* Introduce tasks to install the required additions to
  the Fuel master node.

* Develop a set of tasks to deploy the LCM nodes with
  database and web servers running.

* Make tasks to gather the Hiera data and store it on
  the master node.

* Deploy the Puppet master and the Dashboard on the LCM nodes.

* Deploy the middleware on the LCM modes required to download
  the custom modules from the Git repository.

* Deploy the load balancing services on the LCM nodes.

Dependencies
============

None

-----------
Testing, QA
-----------

* The CI tasks should take a latest version of the plugin,
  install it on the supported Fuel master node and
  perform the deployment of a cluster with configured LCM
  nodes.

* The CI task should check that the LCM nodes are working,
  the Dashboard is accessible and other services running.

Acceptance criteria
===================

The LCM plugin should successfully install the LCM nodes,
configure the other nodes to work with them and should
not interfere with the basic cluster functionality.

* Web UI of the LCM nodes should be accessible from the public
  network through HTTPS protocol.

* Puppet agent on the cluster nodes should successfully connect
  to the Puppet masters on the LCM nodes.

* Foreman dashboard should be able to successfully apply a
  custom manifest downloaded from Git repository on any of
  the cluster nodes.

* LCM nodes should survive rebooting as well as disabling one
  of three nodes.

----------
References
----------

1. LP Request https://bugs.launchpad.net/fuel/+bug/1594856
