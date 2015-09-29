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

[tbd] - when final version is done

It is suggested to move component-related settings under one subtab, so that,
e.g. Compute-related settings will be under one tab and Storage-related under
other.

There are also some network settings on the Settings tab, which is not correct,
because we have a separate Networks tab for networks management.


Web UI
======

The existing Settings tab will be restructured - it's expected to have less
settings groups there.

All settings split to several groups: "Base", "Network", "Storage",
settings with undefined group will go to the "Other" group.

The proposed change to Settings tab:

 .. image:: ../../images/8.0/segment-settings-tab-logically/settings_groups.png

Also settings under "Network" group will move to the Network Tab.

The list of settings organized by groups:

* Base Settings:

  * Access ["access"]
  * Additional Components ["additional_components"]
  * External MongoDB ["external_mongo"]
  * Murano Settings ["murano_settings"]
  * Common ["common"]
  * Kernel parameters ["kernel_params"]
  * Repositories ["repo_setup"]

* Network Settings

  * Neutron Advanced Configuration ["neutron_advanced_configuration"]
  * Syslog ["syslog"]
  * Mellanox Neutron components ["neutron_mellanox"]
  * Public network assignment ["public_network_assignment"]
  * Host OS DNS Servers ["external_dns"]
  * Host OS NTP Servers ["external_ntp"]
  * Public TLS ["public_ssl"]

* Storage Settings

  * Storage ["storage"]

* Other

  * Workloads Collector User ["workloads_collector"]
  * Corosync ["corosync"]
  * Provision ["provision"]

[tbd] - discuss the group naming and groups composition

Nailgun
=======

In openstack.yaml in metadata section of setting - will be added a new
'group' attribute, so that it will be possible to specify the corresponding
settings group for the setting.

List of possible 'group' values: 'base_settings', 'network_settings',
'storage_settings'.

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

Plugin should be able define its group or in case it doesn't, it should go
to "others".


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

New 'group_id' attribute will be added for OpenStack Environment settings which
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
#. UI functional tests should be implemented


Acceptance criteria
===================

#. Settings tab content is easy to read and navigate even for newbie users
#. All network-related settings are on Networks tab


----------
References
----------

* #fuel-ui on freenode
