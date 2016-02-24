..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

======================================
Nailgun API to manage serialized facts
======================================

https://blueprints.launchpad.net/fuel/+spec/serialized-facts-nailgun-api

In this proposal we describe an API for
serialized deployment facts. It shall be used for
the following scenarios:

* access facts from 3rd party applications
* access facts directly from Puppet agent
  via Hiera HTTP backend

This proposal is focused on the last
use case.

--------------------
Problem description
--------------------

Currently, the serialized facts are uploaded to target nodes as an
``/etc/hiera/astute.yaml`` file, and Puppet agents access it via
Hiera's standard ``yaml`` backend as ``astute`` datasource.

Based on facts from ``astute.yaml`` and from local facter,
the deployment task ``globals`` creates another set of facts and
writes them to file ``globals.yaml``. It serves as ``globals``
data source for Hiera.

There are also overrides from plugins, OpenStack configuration
feature [1]_ and node-specific overrides all defined in Hiera's
hierarchy of data sources as local ``yaml`` files.

Thus, all facts that define deployment of a node are
accumulated on that node. While some of them (i.e. ``astute.yaml``)
are available from Nailgun API, others (e.g. plugin-defined
overrides and facts from ``globals.yaml``) are not exposed
by any means. Therefore, it's difficult for 3rd-party
application to access all facts relevant for the node's
deployment process. It is also difficult to consistently
update facts without need to source them
through the deployment process.

Keeping the deployment data at the node doesn't allow
for keeping track of changed settings. Revert to the
original facts is impossible as well.

----------------
Proposed changes
----------------

Terms and definitions:

* *ConfigDB API* is an API defined in this specification.
  Initially it shall be implemented as an extension to
  the standard Nailgun API. [2]_ In future releases, it
  shall be implemented as a separate service
  (codenamed ``tuning-box``) [3]_.

* *Datasource* is a specific set of key/value pairs
  that represents a configuration provided by a certain
  component of the system, for example, by a deployment
  task, a plugin or similar entity.

* *Resource* is another name for *datasource*. Resources are defined
  as templates and can reference another resources.

* *Effective values* are values returned by the ConfigDB API after
  processing the resource at all levels, including per-level user-defined
  overrides.

* *Component* is an entity that contains definitions for resources.
  It corresponds to some element of the system that consumes or
  exposes data via ConfigDB API.

* *Environment* is an entity that contains instances of resources,
  spread among different levels of hierarchy. Different *environments*
  could have different hierarchies. *Environment* isolates its resources
  from resources of other environments.

* *LCM* (Life Cycle Management) is a general name for
  a number of operations on the already installed and
  working OpenStack environment, which include
  services management, configuration management,
  installation of new versions of packages,
  installation of new components and elements of
  the system, and more.

The proposed change will provide the new way to expose
the data produced by existing data processors.

ConfigDB API shall allow to save arbitrary key/value
formatted data. We will use this ability to save and
expose serialized deployment data created by Fuel
components, specifically Nailgun and deployment
tasks from Fuel Library. The service will also
support overriding and extending of the said data.

As described in `Problem description`_ section,
the actual configuration data for each node are
created and stored at that node, and are not available
from other sources. Therefore, we shall collect the
data from nodes and upload them to the ConfigDB API.

The uploaded data will be saved to backend database
(PostgreSQL at the Fuel Master node) in unstructured
format (BLOB).

Every data BLOB shall be identified by ID of the
node it was uploaded from, ID of the environment the
node belogned to and a version number.

Since the 3rd-party LCM application might not be aware
of the Nailgun's internal ID and only have a host name
to identify the node, the mapping of the node's ID and
FQDN shall be implemented in applications that consume
the ConfigDB API.

**Consumers**

There are 3 main consumers of ConfigDB API:

* Deployment task that performs upload of deployment
  configuration from files at a node to the API [4]_.

* Custom Hiera backend included in Fuel plugin for
  Puppet Master LCM [5]_.

* Fuel client application which allows the User to
  change (override) or extend the uploaded
  deployment data (see `Fuel Client`_ section below).

Web UI
======

No changes to UI are proposed in this spec.

Nailgun
=======

New API calls and corresponding handlers shall be introduced to
provide access to results of serialization of deployment facts
for a node. These handlers shall be implemented as an extension
in Nailgun [2]_.

Data model
----------

Refer to the ConfigDB specification for the details
of the proposed Data Model [3]_.

From the standpoint of external Puppet Master LCM, the most
important part of the API data model is a hierarchy of data
sources.

Following data sources are defined for the 3rd-party LCM
use case:

* ``astute``
  This data source represents the Nailgun-originated deployment
  data. This is the source of truth about settings picked
  by the user for the initial deployment of cloud.

* ``globals``
  Certain data are generated by deployment task ``globals``
  and written to file ``/etc/hiera/globals.yaml`` at the
  node. These data are not exposed anywhere outside the
  node, while still used by most other deployment tasks
  at that node. Data source ``globals`` contains data from
  that file for every node in environment.

* ``override/plugins``
  This data source contains data provided by plugins to
  override the settings from ``globals`` and ``astute``
  data sources. The corresponding file on a node that
  provides the data for ``override/plugins`` data source
  is ``/etc/hiera/override/plugins.yaml``.

* ``override/configuration/node``
  ``override/configuration/role``
  ``override/configuration/cluster``
  These data sources are used by OpenStack configuration
  feature. [1]_ Data files for those sources are:

  ``override/configuration/node.yaml``
  ``override/configuration/role.yaml``
  ``override/configuration/cluster.yaml``

  respectively.

* ``override/node``
  This is the data source for the most specific node-level
  deployment data overriding any other levels. Source
  file for this data source is ``/etc/hiera/override/node.yaml``.

REST API
--------

* Create a component that provides data sources.

    * Method type: POST

    * ``<:endpoint_uri>/components``

    * Normal HTTP response code(s): 200 OK

    * Expected error HTTP response code(s): None

    * Parameters which can be passed via the URL

      * ``endpoint_uri`` is a parameter that depends on contents of
        Keystone service catalog for the node. Defaults to ``/api/v1/config``.

    * Data payload in request: JSON-formatted definition of the component.

      **Example:**

     ::

          {
            "id": <int>,  # can be absent in POST request
            "name": <string>,
            "resource_definitions": {
              "resource_name": {}  # empty until we implement schema validation
                  # resource name can be any reasonable URL string, can include
                  # "/"
            }
          }

    * Data payload in response: same as in request, ``<id>`` parameter is
      mandatory in response.

* Create environment in ConfigDB API.

    * Method type: POST

    * ``<:endpoint_uri>/environments``

    * Normal HTTP response code(s): 200 OK

    * Expected error HTTP response code(s): None

    * Parameters which can be passed via the URL

      * ``endpoint_uri`` is a parameter that depends on contents of
        Keystone service catalog for the node. Defaults to ``/api/v1/config``.

    * Data payload in request: JSON-formatted definition of the environment.

      **Example:**

      ::

          {
            "id": <int>,                        # Same as the Nailgun's
                                                # cluster ID

            "components": [<component_id>,...], # List of ints for now
                                                # or they can be names
                                                # instead of ids

            "hierarchy_levels": ["node"]        # The only supported level
                                                # in 9.0 is 'node'
          }

    * Data payload in response: JSON-formatted definition of the environment
      (see request format example above).

* Get the definition of the environment.

    * Method type: GET

    * ``<:endpoint_uri>/environments/<:env_id>``

    * Normal HTTP response code(s): 200 OK

    * Expected error HTTP response code(s): None

    * Parameters which can be passed via the URL

      * ``endpoint_uri`` is a parameter that depends on contents of
        Keystone service catalog for the node. Defaults to ``/api/v1/config``.

      * ``env_id`` identifies an OpenStack environment
        that contains the node being queried

    * Data payload in response: JSON-formatted definition of the environment.

      **Example:**

      ::

         {
            "id": <int>,                        # Same as the Nailgun's
                                                # cluster ID

            "components": [<component_id>,...], # List of ints for now
                                                # or they can be names
                                                # instead of ids

            "hierarchy_levels": ["node"]        # The only supported level
                                                # in 9.0 is 'node'
          }

* Download the latest version of serialized deployment
  facts for the given node ID and data source

    * Method type: GET

    * ``<:endpoint_uri>/environments/<:env_id>/nodes/<:node_id>/resources/<:datasource>/values?effective&version=<:version>``

    * Normal HTTP response code(s): 200 OK

    * Expected error HTTP response code(s):

      * 404 Not Found
        Data source is not supported.

      * 404 Not Found
        Cannot find a node with the given identifier.

      * 404 Not Found
        Cannot find a given version of data for the given cluster, node and
        data source.

      * 404 Not Found
        Node with the given ID not assigned to cluster with the given ID.

    * Parameters which can be passed via the URL

      * ``endpoint_uri`` is a parameter that depends on contents of
        Keystone service catalog for the node. Defaults to ``/api/v1/config``.

      * ``env_id`` identifies an OpenStack environment
        that contains the node being queried

      * ``node_id`` is an ID of node being queried

      * ``datasource`` is a text name of the queried data source.
        See the `Data Model`_ section for the available data sources.

      * ``effective`` flag is used to identify that hierarchically merged
        data must be returned (i.e. *effective data*).

      * ``version`` identifies the version to access. Optional parameter.
        Defaults to the latest version available for the given data source.

    * Response contains serialized data stored for the given version
      of the data source. The data is unstructured set of key/value
      pairs in JSON format.

* Upload serialized deployment facts for a node by ID and data source

    * Method type: PUT

    * ``<:endpoint_uri>/environments/<:env_id>/nodes/<:node_id>/resources/<:datasource>/values``

    * Normal HTTP response code(s): 200 OK

    * Expected error HTTP response code(s):

      * 404 Not Found
        Data source is not supported.

      * 404 Not Found
        Cannot find a node with the given identifier.

      * 404 Not Found
        Node with the given ID not assigned to cluster with the given ID.

    * Parameters which can be passed via the URL

      * ``endpoint_uri`` is a parameter that depends on contents of
        Keystone service catalog for the node. Defaults to ``/api/v1/config``.

      * ``env_id`` identifies an OpenStack environment
        that contians the node being queried

      * ``node_id`` is an ID of node being queried

      * ``datasource`` is a text name of the queried data source
        See the `Data Model`_ section for the available data sources.

    * Request payload should contain serialized data
      in JSON format, no specific schema is defined.

    * Response payload contains the same serialized data as
      the request.

* Upload override of serialized deployment facts for a node by ID and
  data source

    * Method type: PUT

    * ``<:endpoint_uri>/environments/<:env_id>/nodes/<:node_id>/resources/<:datasource>/override``

    * Normal HTTP response code(s): 200 OK

    * Expected error HTTP response code(s):

      * 404 Not Found
        Data source is not supported.

      * 404 Not Found
        Cannot find a node with the given identifier.

      * 404 Not Found
        Node with the given ID not assigned to cluster with the given ID.

    * Parameters which can be passed via the URL

      * ``endpoint_uri`` is a parameter that depends on contents of
        Keystone service catalog for the node. Defaults to ``/api/v1/config``.

      * ``env_id`` identifies an OpenStack environment
        that contians the node being queried

      * ``node_id`` is an ID of node being queried

      * ``datasource`` is a text name of the queried data source
        See the `Data Model`_ section for the available data sources.

    * Request payload should contain serialized data
      in JSON format, no specific schema is defined.

    * Response payload contains the same serialized data as
      the request.

Orchestration
=============

A deployment task shall be implemented to fetch all
``yaml`` files from ``/etc/hiera`` directory, and upload their contents
into corresponding data sources. [5]_

RPC Protocol
------------

No specific changes to orchestration or RPC protocol are proposed
by this particular specification. However, in future it might allow to
exclude serialized deployment facts data from the RPC exchange between
Astute and Nailgun.

Fuel Client
===========

Client should be implemented with the support for the described
API calls. This command should yield a serialized facts data in selected
format (``json`` or ``yaml``) to the ``stdout`` stream.

A separate client option shall be added to add or update facts to the
store. This client must provide an ability to read/write key-value pairs
from the ConfigDB API for all available data sources.

Following CLI parameters shall be supported for ``config`` subcommand:

* ``--env <ID>`` identifies the cluster-level namespace. Mandatory
  argument.

* ``--level node=<FQDN>`` identifies a node part of namespace.
  The 'level' keyword defines the abstract 'level' of the intra-environment
  hierarchy, internal to the ConfigDB extension. Currently there are 4 levels
  (environment itself, role, node_group and individual node) in Fuel. The
  ConifgDB service shall (in future) allow to create custom levels and
  hierarchies if needed, but in version 9.0 it only will work with the
  node-level data.

* ``--level cluster`` identifies environment-wide settings.

* ``--resource <NAME>`` identifies a data source, combined
  with a node name defines a complete name space
  for a data source.

* ``--key KEY`` defines a name of
  key to manage. Mandatory argument.

* ``--value VALUE`` defines a value
  to be assigned to the key identified by first argument. Optional
  argument. If omitted, a value of ``KEY`` is returned.

* ``--format [json|yaml]`` defines a format of input/output.
  Default is ``json``.

Following operations shall be supported for ``config`` command:

* ``get`` - print the *effectvie values* of all parameters defined in the
  resource.

* ``set`` - update data in the data resource, either as a BLOB or individual
  keys. Users normally should run ``override`` command to override values
  of parameters instead of this command.

* ``override`` - update data in the data resource's override for the given
  level. This will change the *effective values* of parameters, without
  changing the values themselves.

**Examples**

* get whole resource as one yaml/json

  ::

    fuel config get --env <id> --level node=<fqdn>
        --resource <name> --format [json|yaml]

* get one key from the resource

  * plain format is just get string representation of the value

  * json/yaml format means smth like "<key>: <value>" preserving value type

  ::

    fuel config get --env <id> --level node=<fqdn>
        --resource <name> --key <key>
        --format [plain|json|yaml]

* set whole resource as one yaml/json from stdin

  ::

    fuel config set --env <id> --level node=<fqdn>
        --resource <name> --format [json|yaml] < resource.[json|yaml]

* override one key in the resource

  * allow to set simple types with --value arg (null doesn't
    require it)

  * set complex types with their json/yaml representation from stdin

  ::

    fuel config overriide --env <id> --level node=<fqdn>
        --resource <name> --key <key> --type [null|int|str|json|yaml|bool]
        [--value <value> | < value.[json|yaml] ]

Plugins
=======

Plugins configuraion data shall be included in the serialization of
``astute`` data source. The overrides for the elements of the
``astute`` data not related to Plugin data will be available via
``override/plugins`` data source.

Fuel Library
============

None.

------------
Alternatives
------------

The alternative approach would be to create a dedicated service to facilitate
the exchange of the serialized data between different components of the Fuel
installer (i.e. ConfigDB [3]_). However, this requires significant changes to
the architecture of the system. This path shall be pursued in the following
major release of Fuel software.

--------------
Upgrade impact
--------------

With the upgrade of the Fuel Admin node, the serialized facts data will be
reset. No tracking of changes in facts shall be available between upgrades.

---------------
Security impact
---------------

The serialized deployment facts contain sensitive data such as access
credentials to different components in the system.

The access to the endpoint must follow the same conventions as other
API endpoints in Nailgun. The endpoint must support Keystone-based
authentication and Basic HTTP Auth. The endpoint must provide SSL
connection.

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

The potential performance impact on the deployment process
is coming from the way the data uploaded to the API. It should
be insignificant compared to other operations.

Impact on the function of Puppet Master shall be significant
as every parameter lookup will require an HTTP request.

The actual impact has to be estimated on top of some baseline
numbers. Therefore, solution will require performance testing
once implemented.

-----------------
Deployment impact
-----------------

The ConfigDB API itself has no impact on deployment
with Fuel. However, the complete solution with a
3rd-party LCM application will change the deployment
workflow once the initial installation is complete
and the LCM application is enabled.

The exact impact of 3rd-party LCM application on
the deployment tasks in operational cluster should
be determined in the documentation to the complete
solution.

----------------
Developer impact
----------------

None.

---------------------
Infrastructure impact
---------------------

New repository in project space ``openstack/`` shall be created to host the
code of the extension. In future release, this code shall be decoupled from
Nailgun into separate service with own code tree and maintenance team. Having
descrete repository from the very beginning will simplify that process.

New repository shall be called ``openstack/tuning-box``. Project codename
``tuning-box`` reflect the nature of the service that allows to manipulate
all kinds of settings.

An RPM package named ``tuning-box`` shall be built from the repository.

The package has the following dependencies that shall be added to Fuel build
system:

* ``python-flask-sqlalchemy``

* ``python-flask-restful``

--------------------
Documentation impact
--------------------

Nailgun API documentation shall be extended with
descriptions of the proposed API calls.

Operations documentation for the ConfigDB API
and client application shall be added to
Operations Guide in Fuel documentation.

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  <gelbuhos> Oleg S. Gelbukh

Other contributors:
  <sabramov> Sergey Abramov
  <sryabin>  Sergey Ryabin
  <ytaraday> Yuriy Taraday

Mandatory design review:
  <sbrimhall>  Scott Brimhall
  <ikalnitsky> Igor Kalnitskiy
  <rustyrobot> Evgeniy Li
  <xarses>     Andrew Woodward

Work Items
==========

* Implement an API handlers in extension source code tree.

* Implement storage backend logic in extension source code tree.

* Implement extension logic to attach the extension to Nailgun
  using ``stevedore``.

* Update Fuel API documentation to reflect changes in the
  Nailgun API.

* Implement simple client application to communicate to the API
  as an extension to Fuel client.

* Develop custom Hiera backend to integrate into Puppet Master
  LCM plugin.

* Integrate custom Hiera backend with PM LCM plugin.

Dependencies
============

* This change depends on deployment task that uploads
  data to the proposed API [4]_.

* This change enables Puppet Master LCM plugin [5]_.

------------
Testing, QA
------------

* Unit tests coverage shall be provided for Nailgun extension
  source code and source code of custom Hiera backend.

* System API tests will ensure that the ConfigDB API responds
  with expected codes at proper endpoint.

* Integration tests shall verify that the data returned from
  ConfigDB API in Hiera lookups are consistent with the data
  from nodes.

* Integraion tests shall verify that the data returned from
  ConfigDB API in Hiera lookups are consistent with override
  data configured via the client application.

Acceptance criteria
===================

* **Use Case #1**
  Get all deployment data for specific node:

  #. Install the Fuel Master node.

  #. Install ConfigDB API extension as an RPM package.

  #. Install plugin for Puppet Master LCM using Fuel CLI.

  #. Create and configure a new environment, enable an LCM plugin
     in the environment.

  #. Add nodes to the environment.

  #. Deploy the environment.

  #. Run the command (for example, environment's ID and node's FQDN
     might be different):

     ::

        fuel config get --env 1 --level node=node-1.domain.tld --resource astute

  #. Validate that the output has the format specific for serialized data
     from ``/etc/hiera/astute.yaml`` file on the node.

* **Use Case #2**
  Get specific key/value pair from the ConfigDB API resource:

  #. Install the Fuel Master node, ConfigDB API and Puppet Master LCM plugin
     as described above in **Use Case #1**.

  #. Create, configure and deploy a new environment with LCM plugin enabled
     as described above in **Use Case #1**.

  #. Run the command (change environment's ID and node's FQDN to appropriate
     for the environment, change a key to any from the resource ``astute``):

     ::

        fuel config get --env 1 --level node=node-1.domain.tld
            --resource astute --key deployment_id

* **Use Case #3**
  Update specific key/value pair in the ConfigDB API resource:

  #. Install the Fuel Master node and deploy an OpenStack environment
     as described above in the **Use Case #1**.

  #. Look up value of a specific key as described above in the **Use
     Case #2**.

  #. Run the command (change environment and node's IDs to appropriate for
     your environment, change key name to the desired):

     ::

        fuel config set --env 1 --level node=node-1.domain.tld
            --resource astute --key deployment_id --value 2

  #. Look up a value of the key and validate that it was properly set in
     resource ``astute`` with the following command:

     ::

        fuel config get --env 1 --level node=node-1.domain.tld
            --resource astute --key deployment_id

* **Use Case #4**
  Hiera backend looks up correct values from the ConfigDB API:

  #. Install the Fuel Master node and deploy OpenStack as described above
     in the **Use Case #1**.

  #. Log in to Puppet Master node.

  #. Run ``hiera`` from the command line to look up ``deployment_id`` value
     using the following command:

     ::

        hiera deployment_id --yaml test_scope.yaml

----------
References
----------

.. [1] OpenStack configuration https://github.com/openstack/fuel-specs/blob/master/specs/8.0/openstack-config-change.rst
.. [2] Extensions mechanism in Nailgun https://github.com/openstack/fuel-specs/blob/master/specs/9.0/stevedore-extensions-discovery.rst
.. [3] ConfigDB specification draft https://review.openstack.org/#/c/281331/
.. [4] Upload serialized deployment facts to ConfigDB https://blueprints.launchpad.net/fuel/+spec/upload-deployment-facts-to-configdb
.. [5] Puppet Master LCM specification TBD
