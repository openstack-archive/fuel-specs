..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==============================
Segment Settings tab logically
==============================

https://blueprints.launchpad.net/fuel/+spec/segment-settings-tab-logically

The current Settings groupings are not intuitive for users, and it is not
possible for additional settings to be included into the previously defined
groups. This causes a proliferation of settings headers and poor user
experience when attempting to locate a relevant setting.


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
e.g. Aсcess-related settings will be under one tab and Storage-related under
other.

There are also some network settings on the Settings tab, which is not
correct, because we have a separate Networks tab for networks management.


Web UI
======

#. The existing Settings tab will be restructured - they will split
   to several groups:

  * General
  * Security
  * Compute
  * Storage
  * Logging
  * OpenStack Services

  Settings with undefined group will go to the 'Other'group.
  Additionally, plugins can provide their own groups.

  Settings with 'network' group -will not be displayed on Settings tab
  anymore.

  To define group for settings - there will be new 'group' attribute into
  metadata section of openstack.yaml file:

  .. code-block:: yaml

    additional_components:
      metadata:
          label: "Additional Components"
          weight: 20
          group: "openstack_services"

  Common settings will be split to several groups - Compute, Storage
  and Logging. They will have 'General Settings' title on the page.

  To define groups for particular Common settings there will be new
  'group' attribute inside every singular settings separetely:

  .. code-block:: yaml

      common:
        metadata:
          label: "Common"
          weight: 30
        debug:
          value: false
          label: "OpenStack debug logging"
          group: "logging"
          ...
        nova_quota:
          value: false
          label: "Nova quotas"
          group: "compute"
          ...

  The list of current environment settings organized by groups:

  * General:

    * Kernel parameters ["kernel_params"]
    * Host OS DNS Servers ["external_dns"]
    * Host OS NTP Servers ["external_ntp"]
    * Repositories ["repo_setup"]
    * Workloads Collector User ["workloads_collector"]
    * Corosync ["corosync"]
    * Provision ["provision"]

  * Security:

    * Access ["access"]
    * Common ["common"] > Public Key ["auth_key"]
    * Public TLS ["public_ssl"]

  * Compute:

    * Common ["common"] > Nova quotas ["nova_quota"]
    * Common ["common"] > Hypervisor type ["libvirt_type"]
    * Common ["common"] > Resume guests state on host boot
      ["resume_guests_state_on_host_boot"]
    * Common ["common"] > ["use_vcenter"]

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

  * Other

    * Settings with undefined group attribute

  The proposed change for Settings tab:
   .. image:: ../../images/8.0/segment-settings-tab-logically/
      settings-group.png
      :scale: 75 %

  Groups sort order will be hardcoded in UI.
  Settings in the group will be sorted by their weight.

  Groups pills will support indication of corresponding settings invalid state.

#. All settings under current 'Network' group will move to the Network Tab

  * Network:

    * Neutron Advanced Configuration ["neutron_advanced_configuration"]
    * Public network assignment ["public_network_assignment"]
    * Common ["common"] > Auto assign floating IP
      ["auto_assign_floating_ip"]
    * Mellanox Neutron components ["neutron_mellanox"]

  The proposed cnange for Network tab:
   .. image:: ../../images/8.0/segment-settings-tab-logically/network-tab.png
      :scale: 75 %

Nailgun
=======

In openstack.yaml in 'metadata' section of setting - will be added a new
'group' attribute, so that it will be possible to specify the corresponding
settings group for the setting.

List of possible 'group' values:

* 'general'
* 'security'
* 'compute'
* 'network'
* 'storage'
* 'logging'
* 'openstack_services'

For Common settings, which should be splitted to several groups, there is
no changes inside metadata section, but 'group' attribute added inside every
singular settings separetely.

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

Plugin should be able to define its group (it can be group from the list
above, or plugin can provide own group). In case a plugin does not have
a group specified, the plugin will be placed under 'Others' group in Fuel UI


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
Infrastructure impact
--------------------------------

None.


--------------------
Documentation impact
--------------------

Specific mentions of settings should be change according to the new structure.
Also plugins and developers documentation should be updated to mention this new
field.


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
  Vitaly Kramskikh, vkramskikh (vkramskikh@mirantis.com),
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
* https://github.com/openstack/fuel-web/blob/master/nailgun/nailgun/fixtures/openstack.yaml
