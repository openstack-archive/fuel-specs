..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

================================================
Puppet noop run for Fuel puppet deployment tasks
================================================

https://blueprints.launchpad.net/fuel/+spec/astute-yaml-dissect


--------------------
Problem description
--------------------

Today we have an astute.yaml as a source of truth when gathering data for
puppet modules. This file has a complex structure, some sections of it can
be met several times. It contains all the data about current cluster and as a
result it leads to following problems:

  * This file generates from DB objects, so when there are many nodes in a
    cluster, it takes too much time to serialize all these entities to a file
  * Astute.yaml has complex structure with too loose logic which leads to badly
    written YAQL queries based on it
  * Some data in this file meets twice or more frequently, which breaks DRY
    principle


----------------
Proposed changes
----------------

Data which serialized from DB should be restructured to better fit current
demands. There are thoughts which we should be guided by for this
restructurization:

  * Common data for all nodes should be splittedi from other data and serialized
    only once. It gives us acceleration when serialize initial data from DB
  * All the data met twice or more in serialized objects must be united in one
    place
  * Similar data sections should be aggregated to bigget sections

The implementation of this approach requires changes in the Fuel:

  * Puppet manifests should be changed accordingly to changed sections

  * Deployment tasks: should be adapted to new serialized data objects

  * Nailgun: serialization should be changed from one big monolithic call to
    separate calls for different sections. Also DB structure should be changed
    to optimize serialization calls

Data structure proposed from bird's-eye perspective:

   .. code-block:: yaml

      openstack_data:
        nova:
          enabled: true
          state_path: /var/lib/nova
          db_password: fhLct13RyfnmJlkfAmIEon8x
          user_password: vkjvbHDjNQeXzkQSP8LYTje1

      cluster_data:
        plugins: []

        deployment:
          configuration: {}
          deployed_before:
            value: false

        provision:
          codename: trusty
          engine:
            master_ip: 10.109.0.2
            password: elEZjTWKE79piXA8jnDVs2JX
            url: http://10.109.0.2:80/cobbler_api
            username: cobbler

        networking:
          master_ip: 10.109.0.2
          management_network_range: 10.109.1.0/24

      node_data:
        fqdn: node-1.test.domain.local
        uid: 1
        name: node-1
        node_volumes:
        - bootable: true
          extra:
          - disk/by-id/virtio-941e0d9ababe43429607

      nodes_data:
        network_metadata:
          nodes:
            node-1:
              fqdn: node-1.test.domain.local
              name: node-1
              network_roles:
                admin/pxe: 10.109.0.5
                aodh/api: 10.109.1.4
                ceilometer/api: 10.109.1.4
        network_scheme:
          endpoints:
            br-ex:
              IP:
              - 10.109.3.4/24
        nodes:
        - fqdn: node-1.test.domain.local
          internal_address: 10.109.1.4

      common_data:
        base_syslog:
          syslog_port: '514'
          syslog_server: 10.109.0.2
        cgroups:
          metadata:
            always_editable: true


Web UI
======

None


Nailgun
=======

* Nailgun should serialize common data only once for cluster and do it
  separately from other serialization tasks


Data model
----------

* DB structure should be changed to represent new scructure


REST API
--------

None


Orchestration
=============

None


Fuel Client
===========

None


Plugins
=======

Plugins for new releases should be rewritten according to the new astute.yaml
structure. Support of old astute.yaml structure will be dropped according to
global Fuel features deprecation policy.


Fuel Library
============

Puppet manifests uses hiera should be rewritten to use new data structure. The
same should be done with noop tests.


------------
Alternatives
------------

None


--------------
Upgrade impact
--------------

* Wrapper which will convert old DB structure to the new on upgrades should be
  written


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

Performance for big clusters will be significantly improved (speed factor is
clearly depends on cluster size as common data grown based on nodes count).


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

None


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  Stanislaw Bogatkin <sbogatkin@mirantis.com>

Other contributors:
  Bulat Gaifullin <bgaifullin@mirantis.com>

Mandatory design review:
  Vladimir Kuklin <vkuklin@mirantis.com>

QA engineer:
  Alexander Kurenyshev <akurenyshev@mirantis.com>


Work Items
==========

* Change Nailgun to serialize data according to new structure

* Create deployment tasks to copy data to target nodes

* Change fuel-library hiera hierarchy to consume new data

* Change fuel-library puppet modules accordinglyhierarchy to consume new data

* Change fuel-library puppet modules accordingly

* Change fuel-noop-fixtures to reflect new data structure


Dependencies
============

None

------------
Testing, QA
------------

* Nailgun's unit and integration tests will be extended to test new feature.

* Fuel-library noop tests will be changed accordingly

* Fuel Client's unit and integration tests will be extended to test new feature.


Acceptance criteria
===================

* Deploy should be successfully ran without old astute.yaml file

* Fuel-library tests should be passed with new data structure


----------
References
----------

1. LP Blueprint https://blueprints.launchpad.net/fuel/+spec/astute-yaml-dissect
