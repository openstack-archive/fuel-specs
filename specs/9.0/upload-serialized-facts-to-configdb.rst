..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================================
Upload serialized deployment facts to ConfigDB service API
==========================================================

https://blueprints.launchpad.net/fuel/+spec/upload-deployment-facts-to-configdb

There are multiple levels of hierarchy in Hiera used by deployment tasks on
nodes. Some of those data exist only in YaML files on a node and can't be
accessed by 3rd party components.

With configuration database service, we can store serialized deployment data
for later use. It requires though that we can upload the data from nodes to
the service as a part of deployment process.

We propose to develop a deployment task to
upload the facts to external HTTP-based API
and add it to a plugin that enables
3rd-party LCM application with Fuel [1]_.

--------------------
Problem description
--------------------

The store for serialized deployment information (e.g. ConfigDB API
extension in Nailgun [2]_) allows 3rd party applications to access
it. It also allows alternative deployment/lifecycle management
solutions to synchronize their configrations with Fuel installer.

However, it doesn't solve the problem of getting the information
into the service, since the extension itself is a more or less
passive store.

The solution is needed to perform actual upload of required information
into the configuration database. It also must keep the data up to date
by synchronizing them upon every change applied to the environment.

Synchronization required in the following cases:

#. Deployment settings changed in Nailgun via UI/CLI/API.
   In this case, Nailgun DB will have the latest changes, and Nailgun API
   will respond with properly updated serialized deployment data [2]_.
   This data can be imported into ConfigDB directly by requesting
   the Nailgun API and sending result to ConfigDB API. They are
   accessible by Hiera as ``astute`` data source [3]_.

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
  ``/environment/<:id>/node/<:id>/resource/<:datasource>/values``).
  See Orchestration_ section for details.

* Integrate the a task into the deployment graph using plugins
  mechanisms of Fuel. The task must run in the end of the deployment
  process to make sure that all the tasks that impact
  the deployment settings files are already executed, including:

  * ``globals``

  * ``override_configuration``

  * any plugin task that updates/overrides basic deployment settings

* Implement a pass of auth information for ConfigDB API
  extension of Nailgun API to the deployment task in question
  in a secure way.

**Deployment task details**

The deployment task shall have the following ID:

::

    upload_data_to_configdb


The task shall depend on the following tasks:

::

    globals
    upload_configuration
    pre_deployment_end

The task shall run at the Fuel Master node. Auth credentials for the
ConfigDB API shall be made available for it upon LCM plugin installation
from the following file:

::

    /var/www/nailgun/plugins/<lcm-plugin-name>/environment_config.yaml

That file will be created by the plugin builder and will contain metadata
of the LCM application, including auth credentials in question.

The task shall perform the following operations using ConfigDB API:

* Verify if the environment ``env_id`` exists in the ConfigDB API.

  * If not, create an environment with ``POST`` request. It should
    contain a list of data sources to create for the environment. See details
    in ConfigDB API specification [2]_.

  * The list of data sources is fetched from ``astute.yaml`` file,
    from parameter ``data_sources`` of Puppet Master LCM plugin's metadata.

* Read data from files in ``/etc/hiera`` directory.

* Upload data to ConfigDB API's data sources based on the filenames from which
  the data was read.

**Auth mechanism details**

ConfigDB API extension as a part of Nailgun API
uses Keystone to verify and authorize users.

The plugin that uses ConfigDB shall be extended to create
a service user in Keystone as a part of installation
of the plugin.

Command ``fuel plugins --install`` will be extended
to create a temporary access to Keystone for the
plugin being installed.

Plugin with this access creates credentials for the
service it deploys (for example, Puppet Master) and
uses the same credentials internally to configure
the service in question.

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

The task shall send a series of requests to the URI of the
resource in ConfigDB based on the parameters
of the deployment:

::

  <:service_uri>/environment/<:env_id>/node/<:node_id>/resource/<:datasource>/values

* ``service_uri`` is a endpoint from Keystone Service Catalog,
  defaults to ``/api/v1/config``.

* ``env_id`` is an identifier of cluster the node belongs to.
  The ID of environment shall be fetched
  from deployment fact ``deployment_id``.

* ``node_id`` is an identifier of the node,
  shall be equal to the node's ``fqdn``.

* ``datasource`` is a name of the data source.

See detailed description of the API in corresponding
specification. [2]_

RPC Protocol
------------

None.

Fuel Client
===========

Fuel client's ``plugins`` command shall be extended.
Flag ``--install`` used with that command shall create
a 'trust' [4]_ in Keystone and write the token ID of the
trust to file ``/var/lib/fuel/plugin_trust``. After
the installation of plugin, the file shall be deleted.

This will allow a plugin aware about the location of
the file to access Keystone with the permission to
create a service user for service installed
by the plugin in question.

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

The deployment task proposed in this spec will take
some time to upload all data to the ConfigDB API.
Moreover, if many nodes trying to write to the same
API endpoint at the same time, it might significantly
affect the overall duration of deployment.

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

* Extend Fuel client ``plugins`` command to provide
  necessary access to Keystone API for plugin.

* Develop deployment task as a part of Puppet Master LCM
  plugin code base [1]_.

* Develop unit tests for the deployment task in the
  plugin's code base.

* Develop automated integration tests for the plugin in
  ``openstack/fuel-qa`` repository.

Dependencies
============

#. ConfigDB API implementation as Nailgun extension [2]_

------------
Testing, QA
------------

* The feature shall be tested in conjunction with
  ConfigDB API feature [2]_

* Tests shall verify that contents of data sources
  are consistent with contents of files in ``/etc/hiera``
  at nodes after the deployment finishes.

Acceptance criteria
===================

* Deployment data from nodes uploaded to corresponding
  data sources in ConfigDB API upon successful
  deployment of the OpenStack environment.

----------
References
----------

.. [1] Puppet Master LCM plugin specification TBD
.. [2] Nailgun API extension for serialized deployment facts https://review.openstack.org/#/c/284109/
.. [3] Nailgun API for Deployment Information https://github.com/openstack/fuel-web/blob/master/nailgun/nailgun/api/v1/handlers/orchestrator.py#L190
.. [4] Trusts API in Keystone https://specs.openstack.org/openstack/keystone-specs/api/v3/identity-api-v3-os-trust-ext.html
