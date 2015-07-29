..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

====================================
Networking templates support in Fuel
====================================

https://blueprints.launchpad.net/fuel/+spec/templates-for-networking

Fuel will be able to provide more flexible networking configurations via
templates.
Services will not be tied to networks 1:1. User will be able to create
any number of networks and map them to services (i.e. network roles).
User will be able to use different sets of network roles for different nodes
depending on node roles' sets for those nodes.

It is required to support both "new" and "old" networking strategies
in RPC. We need to support "old" one for environments based on earlier
releases and for environments configured via API.

Nova-Network is not supported for new environments, it is supported for old
ones only. Multi-rack is supported with templates only.


Problem description
===================

Fuel 6.1 has a very straightforward networking configuration procedure.
It's required for environment to use 4-5 networks depending on environment
configuration. Every service uses its own (predefined) network. Furthermore,
most networks are configured on all environment nodes no matter are they
required or not (with the exception of Public network for Fuel 5.1 and later).
Topology configuration is not flexible enough (e.g. subinterface bonding cannot
be used via API).


Proposed change
===============

Template solution is proposed to provide the following capabilities:

* Ability to create additional networks and delete networks (new API handlers
  to be added to support this).
* Have a specific set of network roles.
* Ability to create network only in case relevant node role is present on the
  node.
* Ability to provide custom networking topologies (e.g. subinterface bonding).

Template solution details:

* REST API handler is added to load/cancel template for given environment
  (/clusters/x/network_configuration/template/).
* Template is applied during serialization if it was set for the env. So,
  template can be loaded/reloaded any time before deployment is started and
  after reset. So, it is the same behaviour as for all network settings now.
  Deployment serializer for networking will be selected with regard to the fact
  whether template was loaded or not.
* Template has priority over network schema (not network addresses or node
  groups) in the DB (explained better below). If it is applied then DB data
  (related to network roles to networks mapping, networks to interfaces mapping
  and network objects topology) is ignored by networking serializer. If it is
  not applied then DB data is taken into account by networking serializer.
  Serialization of other data is not affected.
* Astute.yaml for particular node has priority over template by default.
  If yaml was uploaded for particular nodes serialized data for them will be
  taken from there. Additional flag is added to node to override network part
  of astute.yaml. It the flag is set then network data is taken from serializer
  output regardless of template presence. Node's yaml overriding task can be
  postponed due to lack of time.
* Template allows to override network roles to networks mapping and topology
  (to support complex cases which cannot be configured via API, like
  subinterface bonding). Network roles' set can be not equal to core set, it is
  up to user. No verification of network roles' set is provided at this stage.
  Network roles to networks mapping can be set for each node role
  independently. Sets of network roles and networks may be different on every
  particular node. Validation should be added to ensure that all required roles
  are present on every node. It's naturally done with network roles to tasks
  mapping but can be postponed due to lack of time.
* Template allows to use distinct network schemes for different node roles and
  for different node network groups. It also allows to use different NICs' sets
  for particular node network groups and particular nodes.

User should be able to use specific networks for swift & cinder traffic:

* Puppet manifests should support separated network roles for these services.
* Template solution will allow to use the separation of network roles and
  networks.

All the networking metadata which is now defined within networks should be
moved to network roles description:

* Every task description has section [network_roles] where the list of names of
  network roles required is declared. (It's required for template validation at
  least.) It can be out of first feature release as not highest priority task
  which takes significant time.
* Descriptions of network roles are propagated to Nailgun and include metadata
  which is required for serialization to orchestrator.
* VIPs assignment is done using network roles metadata instead of networks
  metadata. It is true for both template and general flow.


Alternatives
------------

N/A


Data model impact
-----------------

Template example::

    adv_net_template:
      default:
        nic_mapping:
          default:
            if1: eth0
            if2: eth1
            if3: eth2
          node-3:
            if1: eth0
            if2: eth1
            if3: eth2
            if4: wlan0
        network_scheme:
          common:
            transformations:
              - action: add-br
                name: br-fw-admin
              - action: add-br
                name: br-mgmt
              - action: add-br
                name: br-storage
            endpoints:
              - br-mgmt
              - br-storage
              - br-fw-admin
            roles:
              admin/pxe: br-fw-admin
              neutron/api: br-mgmt
              mgmt/corosync: br-mgmt
              mgmt/database: br-mgmt
              mgmt/messaging: br-mgmt
              mgmt/api: br-mgmt
              mgmt/vip: br-mgmt
              nova/api: br-mgmt
              murano/api: br-mgmt
              sahara/api: br-mgmt
              ceilometer/api: br-mgmt
              heat/api: br-mgmt
              keystone/api: br-mgmt
              horizon: br-mgmt
              glance/api: br-mgmt
              ceph/public: br-mgmt
              swift/api: br-mgmt
              cinder/api: br-mgmt
              mongo/db: br-mgmt
              swift/replication: br-storage
              ceph/replication: br-storage
              cinder/iscsi: br-storage
          public:
            transformations:
              - action: add-br
                name: br-ex
              - action: add-br
                name: br-floating
                provider: ovs
              - action: add-patch
                bridges:
                - br-floating
                - br-ex
                mtu: 65000
                provider: ovs
            endpoints:
              - br-ex
              - br-floating
            roles:
              public/vip: br-ex
              ceph/radosgw: br-ex
              swift/public: br-ex
              neutron/floating: br-floating
          private:
            transformations:
              - action: add-br
                name: br-prv
                provider: ovs
              - action: add-br
                name: br-aux
              - action: add-patch
                bridges:
                - br-prv
                - br-aux
                mtu: 65000
                provider: ovs
            endpoints:
              - br-prv
              - br-aux
            roles:
              neutron/private: br-prv
        templates_for_node_role:
          controller:
            - common
            - public
            - private
          compute:
            - common
            - private
        network_assignments:
          storage:
            ep: br-storage
          private:
            ep: br-prv
          public:
            ep: br-ex
          management:
            ep: br-mgmt
          fuelweb_admin:
            ep: br-fw-admin

Network roles are introduced. Network role description contain:

* id - string, can be treated as name. It should be used in tasks' descriptions
  for referencing network roles required for particular task. It is also used
  in manifests.
* default_mapping - string, name of the network to map this role be default
  (when template is not in use).
* properties - dictionary, properties which are required for underlying network
  are described here, like CIDR, gateway, VIPs.
* metadata - dictionary, it is metadata which is not related to networks,
  e.g. neutron settings. It is in our DSL format. It will be shown in UI and
  could be edited there. It is passed to orchestrator as is. Nailgun doesn't
  process it. It will not be used in 7.0. So, it can be skipped for now.

Network role description example::

    id: "mgmt/vip"
    default_mapping: "management"
    properties:
      subnet: true
      gateway: false
      vip:
        - name: "vrouter"
          namespace: "vrouter"
        - name: "management"
          namespace: "haproxy"
          node_roles: ["primary-controller", "controller"]

VIPs can be requested in network role's description. Description of VIP
includes:

* name - string, it should be unique name within the environment, it cannot be
  skipped.
* namespace - string, network namespace, that should be used for landing of
  the VIP, will be serialized to null when skipped.
* node_roles - list, node roles where VIPs should be set up. It can be skipped.
  Its value will be set to ["primary-controller", "controller"] then.

Network role descriptions are accessible for Nailgun. They are accumulated into
network_role_metadata field of Release DB table. They are used for assignment
of VIPs at this stage. They will be used more heavily when network roles to
networks mapping will be added to API.

Network roles to networks mapping can be set almost freely via templates. There
is no check of network roles' set which is defined in template at this stage.
It is on user now. Network roles to networks mapping is fixed when template is
not applied.

Assignment of VIPs will be changed: it will be done using network roles
metadata for 7.0 environments regardless of template usage.
Assignment of VIPs for pre-7.0 environments will remain the same. This duality
will be solved with versioning of network manager.

There is an ability to load a template for networking configuration. It is
loaded/cancelled with separate API call. When it is loaded/cancelled, networks
DB objects are not changed. Networks to interfaces mapping in DB will be wrong
when template is being used. It is not synchronized as template provides much
more flexible scheme than DB relations can address for now. So, some checks of
network configuration consistency will be disabled while working with template.

Template is loaded into 'configuration_template' field of 'networking_configs'
DB table. Serialization of network configuration for deployment supports two
modes: serialization according template and serialization according DB. In both
cases DB will be used as source of information about networks L3 configuration
and IP addresses. But there will be difference regarding network roles to
networks mapping, networks to interfaces mapping, L2 topology.

IPs allocation for nodes in case of template will take in account which
networks are in use on particular node.

Basic verification of template should be done while it is being loaded:
nodes and node network groups listed in template must exist in DB.
Verification of network roles, nodes' interfaces, etc. is to be added later.

Proper parameters for network verification tool should be provided in case of
template usage to allow network verification in this mode. It can be done using
template parsing or using some additional metadata provided by user in the
same template.

The following symbols will not be used in Nailgun output for orchestrator for
7.0 environments as we do not have fixed names of networks any longer:
- internal_address
- internal_int
- internal_netmask
- management_network_range
- network_size
- novanetwork_params
- private_int
- public_address
- public_int
- public_netmask
- storage_address
- storage_hash
- storage_netmask
- storage_network_range
Network properties will be tied to network roles and/or endpoints instead.
We need to write up a migration plan here, we cant drop this in a single
release - TBD.


REST API impact
---------------

Add "/clusters/x/network_configuration/template/" URL to load/cancel template
for given environment.

Template body is provided with this API call. It should be verified and loaded
into DB. If validation failed DB is kept without changes.
Template is cancelled if empty template body was provided with this API call.
DB will be updated with empty template then.

Add "/networks/" URL to create networks and get their parameters (POST/GET).
Add "/networks/x/" URL to get/set parameters of individual network and delete
network (GET/PUT/DELETE).

All parameters and metadata can be changed for individual network via
"/networks/x/".


Upgrade impact
--------------

Migration of schema and data must be provided to support previously created
environments and creation of environments with older releases. It should
include migration of existing releases and clusters.


Security impact
---------------

No additional security modifications needed.


Notifications impact
--------------------

N/A.


Other end user impact
---------------------

N/A

Performance Impact
------------------

No Nailgun/Library performance impact is expected.


Other deployer impact
---------------------

N/A


Developer impact
----------------

N/A


Implementation
==============

Assignee(s)
-----------

Feature Lead: Aleksey Kasatkin

Mandatory Design Reviewers: Andrew Woodward, Sergey Vasilenko

Developers: Ivan Kliuk, Ryan Moe, Sergey Vasilenko, Stas Makar

QA: Alexander Kostrikov, Artem Panchenko


Work Items
----------

* Nailgun:
   a. Add network roles descriptions for core network roles
      (Estimate: 2d)
   b. VIPs allocation using network roles info
      (Estimate: 2d)
   c. Add API handler for loading/cancellation of template and serialization
      double-logic
      (Estimate: 2-4d)
   d. Add template structure validation for API handler
      (Estimate: 1-2d)
   e. Add template serialization
      (Estimate: 5-8d)
   f. Add 'roles' section into 'network_metadata' (to get rid of
      internal_address, etc. in library)
      (Estimate: 3-4d)
   g. Change networks and IPs in DB according to template
      (Estimate: 1-2d)
   h. IPs allocation using info about network to nodes mapping
      (Estimate: 2d)
   i. Add API handler for networks creating/removal
      (Estimate: 2-3d)
   j. Add section [network_roles] into task descriptions
      (Estimate: 1-2d + library to provide info)
   k. Provide data for network verification tool in case of template
      (to be estimated)
   l. Add simple template data validation for API handler
      (Estimate: 2-3d)
   m. Add overriding of network configuration after uploading of yaml for node.
      (Estimate: 2-3d)

* Network verification tool:
   a. Update verification for template solution.
      Under consideration. Update of Nailgun part maybe enough.

* Library:
   a. Decoupling of networks and roles in manifests.
      (Estimate: ?)

* CLI:
   a. Add templates functionality
      (Estimate: 2-3d in total)

* Documentation / Testing:
   a. Produce a number of common templates to serve as both documentation of
      common needs and to feed into testing.
      (Estimate: 2-3d)
   b. Produce test cases from (a).
      (Estimate: ?)


Dependencies
============

https://blueprints.launchpad.net/fuel/+spec/multiple-cluster-networks


Testing
=======

* Additional unit/integration tests for Nailgun.
* Additional System tests against a test environment with networking
  configuration set using a template.

* Some part of old tests of all types will become irrelevant and
  are to be redesigned.

Acceptance Criteria
-------------------

* Descriptions of network roles are propagated to Nailgun and include metadata
  which is required for serialization to orchestrator.
* API handler is added to load/cancel template for given environment.
* API handler is added to create/remove networks for given environment.
* Template is applied during serialization if it was set for the env.
* Template has priority over networking data in DB. If it is applied DB data is
  ignored by networking serializer. If it is cancelled DB data is taken into
  account by networking serializer.
* Astute.yaml for particular node has priority over template. If yaml was
  uploaded for particular nodes serialized data will be taken from there.
* Template allows to override network roles to networks mapping,
  topology (to support complex cases which cannot be configured via API, like
  subinterface bonding). Network roles' set can be not equal to core set, it is
  up to user. No verification of network roles' set is provided at this stage.
* Template allows to use distinct network schemes for different node roles and
  for different node network groups. It also allows to use different NICs order
  for particular node network groups and particular nodes.


Documentation Impact
====================

The documentation should describe new networking architecture of Fuel,
networking templates workflow, limitations of network scheme provided by
templates, a library of templates.


References
==========

https://blueprints.launchpad.net/fuel/+spec/templates-for-networking
