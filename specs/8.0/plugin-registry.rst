..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===============
Plugin registry
===============

https://blueprints.launchpad.net/fuel/+spec/plugin-registry

Implement mechanism of compatibility between plugins.

--------------------
Problem description
--------------------

Currently when Fuel plugins provide deployment scenarios to install third
party components for OpenStack Compute, Network or Storage parts there is no
way to check compatibility between them which causes fail of deployment
process or broken OpenStack environment in the end. For instance: in future
we want to have multi-networking functionality but not all Network core
plugins like Contrail can be combined via ML2 so we need restrict available
options before deployment. Another example: we have cinder-vmware as Storage
backend component which works only when ESX networking provided. In such case
we should restrict this option if inappropriate net provider was chosen.


----------------
Proposed changes
----------------

Plugin developers should be able to describe plugin compatibilites in context
of subtypes. For example: some plugin provide new Network type and compatible
only with hypervisor core plugins (KVM, QEMU) or only with vmware (ESX).

Data model
----------

Compatibility between plugins should be shown explicitly. To avoid direct
compatible relation between specific plugins we can group them in sets (or
subtypes) and then working in context of compatibility between subtypes. Such
aproach decrease dimension of compatibility matrix (K-map matrix) which
represents compatible relations. For example current list of subtypes can
be next (in future may be extended):
  * hypervisor:core
  * hypervisor:vmware
  * network:core
  * network:ml2
  * storage:object:backend
  * storage:block:backend
  * storage:image:backend
  * monitoring:core

Compatibility matrix can be next (some subtypes skipped for simplifying):

+-----------------------------------------------------------------------+
|           |hypervisor:|hypervisor:|network:   |network:ml2|monitoring:|
|           |core       |vmware     |core       |           |core       |
+-----------+-----------+-----------+-----------+-----------+-----------+
|hypervisor:|           |           |           |           |           |
|core       |           |           |           |           |           |
+-----------+-----------+-----------+-----------+-----------+-----------+
|hypervisor:|           |           |           |           |           |
|vmware     |           |           |           |           |           |
+-----------+-----------+-----------+-----------+-----------+-----------+
|network:   |           |           |     X     |     X     |           |
|core       |           |           |           |           |           |
+-----------+-----------+-----------+-----------+-----------+-----------+
|network:ml2|           |           |     X     |           |           |
|           |           |           |           |           |           |
+-----------+-----------+-----------+-----------+-----------+-----------+
|monitoring:|           |           |           |           |           |
|core       |           |           |           |           |           |
+-----------+-----------+-----------+-----------+-----------+-----------+

From this representation we can see that network:core plugins like Contrail
not compatible with others netwroking types. For DVS ML2 plugin we can show
that it's compatible only for hypervisor:vmware and so on.


REST API
--------

N/A


Web UI
------

N/A


Nailgun
-------

Plugin sync method should store wizard metadata into DB like it already
done for other plugin entities.


Orchestration
-------------

N/A


RPC Protocol
------------

N/A


Fuel Client
-----------

TODO


Plugins
-------

Extend current metadata structure with new options.


Fuel Library
------------

N/A


------------
Alternatives
------------

Keep notes for workarounds in plugin documentation like it done now.


--------------
Upgrade impact
--------------

N/A


---------------
Security impact
---------------

N/A


--------------------
Notifications impact
--------------------

N/A


---------------
End user impact
---------------

N/A


------------------
Performance impact
------------------

N/A


-----------------
Deployment impact
-----------------

N/A


----------------
Developer impact
----------------

N/A


--------------------------------
Infrastructure/operations impact
--------------------------------

N/A


--------------------
Documentation impact
--------------------

There are should be documented notes how plugin developers can modify
wizard tab for their needs.


--------------------
Expected OSCI impact
--------------------

N/A


--------------
Implementation
--------------

Assignee(s)
-----------

Primary assignee:
  * Andriy Popovych <apopovych@mirantis.com>
  * Elena Kosareva <ekosareva@mirantis.com>

Mandatory design review:
  * Igor Kalnitsky <ikalnitsky@mirantis.com>


Work Items
----------

* [Nailgun] Implement mechanisme fof generation binds and restrictions based
  on compatiblity matrix for wizard options which provided by plugins.



Dependencies
------------

N/A


------------
Testing, QA
------------

TBA


Acceptance criteria
-------------------

* Wizard can expose all options of a specific type (e.g. Networking,
  Compute, Cinder storage)

* Wizard can expose compatibility (and incompatibility) between selections
  (e.g. if vCenter is selected as only Compute option, then Contrail should
  not be a valid Networking option)

* Metadata required by plugins to self-define compatibility, type and
  sub-type has been defined and added to plugin SDK, shared with Partner
  Enablement team


----------
References
----------

N/A
