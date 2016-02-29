..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================================
Upload serialized deployment facts to ConfigDB service API
==========================================================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/fuel/+spec/upload-deployment-facts-to-configdb

There are multiple levels of hierarhy in Hiera used by deployment tasks on
nodes. Some of those data exist only in YaML files on a node and can't be
accessed by 3rd party components.

With configuration database service, we can store serialized deployment data
for later use. It requires though that we can upload the data from nodes to
the service as a part of deployment process.

We propose to add a task to the deployment graph and in fuel-library to
upload the facts to external HTTP-based API.

--------------------
Problem description
--------------------

The store for serialized deployment information (e.g. ConfigDB service)
allows 3rd party applications to access it. It also enables alternative
deployment/lifecycle management solutions to synchronize their
configrations with Fuel installer. However, it doesn't solve the
problem of getting the information into the service, since the
service itself is a more or less passive store.

The solution is required to perform actual upload of required information
into the configuration database. It also must keep the data up to date
by synchronizing them on every change applied to the environment.

Synchronization required in the following cases:

#. Deployment settings changed in Nailgun via UI/CLI/API.
   In this case, Nailgun DB will have the latest changes, and Nailgun API
   will respond with properly updated serialized deployment data. [1]_
   This data can be imported into ConfigDB directly by requesting
   the Nailgun API and sending result to ConfigDB API. They are
   accessible by Hiera as ``astute`` data source [2]_

#. Deployment data changed due to changes made to the node (e.g. hardware
   updated, versions of packages updated, etc) outside the Fuel context.
   These changes are reflected in the serialized data generated and stored
   on the node itself, in YaML files:

  * ``/etc/hiera/globals.yaml`` - global configurations calculated by
    deployment task ``globals``.

  * ``/etc/hiera/override/plugins.yaml`` - plugin-specific overrides
    of parameters defined in data sources on higher levels (i.e.
    ``astute`` and ``globals``).

  * ``/etc/hiera/override/configuration.yaml`` - specific overrides
    for OpenStack configuration parameters which are not exposed
    by Nailgun directly.

  * ``/etc/hiera/override/<hostname>.yaml`` - node-level configurations
    that override the basic parameters from other sources.

#. Deployment data changed in 3rd party deployment/lifecycle management
   application (e.g. in Puppet Master's top-level manifests or in External
   Nodes Classifier application for the Puppet Master). Here we need
   to import data from the 3rd party application. This case is out of
   scope of the current proposal.

In this specification, we will focus on the use cases #1 and #2.

----------------
Proposed changes
----------------

The current deployment process implemented in Fuel installer assumes
that all actual deployment data is available to Puppet agent on a target
node locally as a set of YaML files in ``/etc/hiera`` directory.

By the time Puppet agent starts to execute actual deployment tasks,
all the configuration settings must be up to date. It means that we
can import the actual set of the deployment configuration data from
those files as a part of deployment process.

The following changes are proposed in scope of this specification:

* Create a deployment task that uploads the serialized
  deployment data from files in ``/etc/hiera`` of a target node to
  the corresponding resources in ConfigDB API endpoint (e.g.
  ``/environment<:id>/node/<:id>/resource/<:datasource>/values``).
  See Orchestration_ section for details.

* Integrate the a task into the deployment graph using plugins
  mechanisms of Fuel. The task must run in the end of the deployment
  process to make sure that all the tasks that impact
  the deployment settings files are already executed, including:

  * ``globals``

  * ``override_configuration``

  * any plugin task that updates/overrides basic deployment settings

Web UI
======

None.

Nailgun
=======

None.

Data model
----------

None.

REST API
--------

None.

Orchestration
=============

A new deployment task shall be added to ensure
that all changes to files in ``/etc/hiera`` directory
are synchronized with the ConfigDB.

The task shall send a requests to the URI of the
resource in ConfigDB based on the parameters
of the deployment:

``<:service_uri>/environment/<:env_id>/node/<:node_id>/resource/<:datasource>/values``

* ``service_uri`` is a endpoint from Keystone Service Catalog

* ``env_id`` is an identifier of cluster the node belongs to

* ``node_id`` is an identifier of the node, shall be node's ``fqdn``

* ``datasource`` is a name of the data source

See detailed description of the API in corresponding specification. [2]_

RPC Protocol
------------

None.

Fuel Client
===========

None.

Fuel Library
============

None.

------------
Alternatives
------------

The alternative way to keep deployment data from nodes in
sync with ConfigDB is to upload data to API from deployment tasks.

While it is possible to adjust ``globals`` and ``openstack_config``
tasks to upload configuration data to external service, it is
generally impossible to do with all supported plugins.

A plugin can override default values in ``astute.yaml``
generated by the Nailgun-provided serialized data. However,
this overrides are configured by plugin tasks
on a per-node basis. Override information is not available
to Nailgun or even Astute directly. So, to ensure sync
of plugins' override data we need to modify each and every plugin,
which apparently is not an option.

Another way to keep data in sync is to upload it from some
bottom-level catch-all Astute post-deployment task. This
would allow to keep Nailgun/ConfigDB credentials limited to
the Master node and not expose them to target nodes
in the deployment.

On the other hand, there was a work done on Astute to
convert its tasks into standard deployment tasks in
``fuel-library``. Thus, we should net add new tasks
to Astute in this proposal.

--------------
Upgrade impact
--------------

None.

---------------
Security impact
---------------

Sensitive configuration data, such as passwords and access credentials,
shall be uploaded to the ConfigDB API using proposed functions.
It is recommended to use encrypted HTTP protocol to
transfer these data.

--------------------
Notifications impact
--------------------

None.

---------------
End user impact
---------------

None.

------------------
Performance impact
------------------

None.

-----------------
Deployment impact
-----------------

None.

----------------
Developer impact
----------------

None.

---------------------
Infrastructure impact
---------------------

None.

--------------------
Documentation impact
--------------------

None.

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  <gelbuhos> Oleg S. Gelbukh

Other contributors:
    <sryabin> Sergey Ryabin

Mandatory design review:
  <rustyrobot> Evgeniy Li
  <ikalnitsky> Igor Kalnitsky
  <vsharshov> Vladimir Sharshov
  <vkuklin> Vladimir Kuklin


Work Items
==========

* Develop deployment task in ``fuel-library`` source code repository.

* Develop automated integration tests in ``openstack/fuel-library``
  and ``openstack/fuel-qa`` repository.

Dependencies
============

#. ConfigDB API implementation as Nailgun extension [2]_

------------
Testing, QA
------------

TBD

Acceptance criteria
===================

TBD

----------
References
----------

.. [1] Nailgun API for Deployment Information https://github.com/openstack/fuel-web/blob/master/nailgun/nailgun/api/v1/handlers/orchestrator.py#L190
.. [2] Nailgun API extension for serialized deployment facts https://review.openstack.org/#/c/284109/
