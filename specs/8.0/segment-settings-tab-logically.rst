..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==============================
Segment Settings tab logically
==============================

https://blueprints.launchpad.net/fuel/+spec/segment-settings-tab-logically

Settings are bad-structured on Settings tab, it's not obvious for the user
where to find the appropriate settings group.


--------------------
Problem description
--------------------

There is a real mess on the Settings tab - groups are malformed: some of them
contain only one checkbox, others contain not related information. It's not
clear for the user where to find the needed settings item.


----------------
Proposed changes
----------------

It is suggested to move component-related settings under one subtab, so that,
e.g. Acess-related settings will be under one tab and Storage-related under
other.

There are also some network settings on the Settings tab, which is not correct,
because we have a separate Networks tab for networks management.


Web UI
======

The existing Settings tab will be restructured - they will split to several
groups: 'General', 'Security', 'Hypervisor', 'Network', 'Storage', 'Logging',
'OpenStack Services', settings with undefined group will go to the 'Other'
group. Additionally Plugins can provide his own groups.

The proposed change for Settings tab:
[tbd: prepare screenshots, when ready]

Also all settings under 'Network' group will move to the Network Tab.

The list of settings organized by groups:

* General:

  * Kernel parameters ["kernel_params"]
  * Host OS DNS Servers ["external_dns"]
  * Host OS NTP Servers ["external_ntp"]
  * Repositories ["repo_setup"]

* Security:

  * Access ["access"]
  * Common ["common"] > Public Key ["auth_key"]
  * Public TLS ["public_ssl"]

* Hypervisor:

  * Common ["common"] > Nova quotas ["nova_quota"]
  * Common ["common"] > Hypervisor type ["libvirt_type"]
  * Common ["common"] > Resume guests state on host boot
    ["resume_guests_state_on_host_boot"]
  * Common ["common"] > ["use_vcenter"]

* Network:

  * Neutron Advanced Configuration ["neutron_advanced_configuration"]
  * Public network assignment ["public_network_assignment"]
  * Common ["common"] > Auto assign floating IP ["auto_assign_floating_ip"]

* Storage:

  * Common ["common"] > Use qcow format for images ["use_cow_images"]
  * Storage ["storage"]

* Logging:

  * Common ["common"] > OpenStack debug logging ["debug"]
  * Common ["common"] > Puppet debug logging ["puppet_debug"]
  * Syslog ["syslog"]

* OpenStack Services:

  * Additional Components ["additional_components"]
  * External MongoDB ["external_mongo"]
  * Murano Settings ["murano_settings"]
  * Mellanox Neutron components ["neutron_mellanox"]

* Other

  * Workloads Collector User ["workloads_collector"]
  * Corosync ["corosync"]
  * Provision ["provision"]

Nailgun
=======

In openstack.yaml in 'metadata' section of setting - will be added a new
'group' attribute, so that it will be possible to specify the corresponding
settings group for the setting.

.. code-block:: yaml

  additional_components:
    metadata:
        label: "Additional Components"
        weight: 20
        group: "openstack_services"

List of possible 'group' values: 
  * 'general'
  * 'security'
  * 'hypervisor'
  * 'network'
  * 'storage'
  * 'logging'
  * 'openstack_services'

Data model
----------

None.


REST API
--------

None.


Orchestration
=============

None.


RPC Protocol
------------

None.


Fuel Client
===========

None.


Plugins
=======

Plugin should be able define its group (in can be group from the list abow,
or plugin can provide own group) or in case it doesn't, it should go
to "Others".


Fuel Library
============

None.


------------
Alternatives
------------

None.


--------------
Upgrade impact
--------------

None.


---------------
Security impact
---------------

None.


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

New 'group' attribute will be added for OpenStack Environment settings which
will give the developers an ability to structure their settings logically.


--------------------------------
Infrastructure/operations impact
--------------------------------

None.


--------------------
Documentation impact
--------------------

Specific mentions of settings should be change according to the new structure.
Also plugins and developers documentation should be updated to mention this new
field.


--------------------
Expected OSCI impact
--------------------

None.


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  Kate Pimenova, kpimenova (kpimenova@mirantis.com)

QA engineer:
  Anastasia Palkina, apalkina (apalkina@mirantis.com)

Mandatory design review:
  Vitaly Kramskikh, vkramskikh (vkramskikh@mirantis.com)
  Sheena Gregson, sgregson (sgregson@mirantis.com)


Work Items
==========

#. Make a decision on appropriate settings grouping
#. Restructure settings tab according to the new segmentation
#. Move network-related settings to the Networks tab

Dependencies
============

None.

------------
Testing, QA
------------

#. Manual testing
#. UI functional tests of Settings and Networks tabs should be updated
   accordingly.


Acceptance criteria
===================

#. Settings tab content is easy to read and navigate even for newbie users
#. All network-related settings are on Networks tab


----------
References
----------

* #fuel-ui on freenode
