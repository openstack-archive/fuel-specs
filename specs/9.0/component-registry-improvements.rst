..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===============================
Component registry improvements
===============================

https://blueprints.launchpad.net/fuel/+spec/component-registry-improvements

Improve current Fuel component registry functionality [0]_ with possibility of
describing complex rules in incompatible/requires relations and restrict plugin
sections on `Settings` and `Network` tabs based on it.

-------------------
Problem description
-------------------

Currently plugins which provide components can be enabled/disabled after
bypassing wizard configuration. For example: if DVS is disabled option on
wizard, user still can turn-on it in settings without vmware hypervisor [2]_.
Also current components DSL model can't cover complex logical cases. Some of
them:

  * `requires` functionality process only `enabled` components. In other words
    it declares sufficiency condition: if A requires B then B should be
    enabled (checked or selected on UI). But in case of UI wizard tab when
    DSL defines: vCenter requires DVS or NSXv network backends, it meens that
    they should satisfy only necessity condition: if A requires B then B
    should be present (exist in components list).

  * Logic in compatible/incompatbile/requires relations are very simple and
    can't cover many cases. For example same case with vCenter, DVS and NSXv.

    .. code-block:: yaml

    - name: hypervisor:vmware
        compatible:
          - name: hypervisor:libvirt:*
        requires:
          - name: network:neutron:NSX
          - name: network:neutron:DVS

    In this case both NSX and DVS are required for vmware, but vCenter needs
    only one of them.

  * Components representation for ML2 drivers or storage backends hardcoded
    on UI side [4]_ [5]_. It's not posible to describe new groups for
    components in DSL.

----------------
Proposed changes
----------------

* Provide restrictions for plugin sections on `Settings` and `Network` tabs.
  Current expression logic works out-of-the-box for cheking enabled components
  in cluster.

* Extend components DSL model with additional predicates:
  `one_of` - checks that only one element from list should be processed.
  `all_of` - checks that all elements from list are processed.
  `any_of` - checks that any element from list can be processed.
  `none_of` - checks that none element from list should be processed.

  Each of this predicates can be implmented as function which takes components
  list to check as argument. In case of False specific message can be raised.

  With such changes the first two problems can be solved smth like this:

  .. code-block:: yaml

    components:
      - name: hypervisor:libvirt:qemu
      - name: hypervisor:libvirt:kvm
      - name: hypervisor:vmware
        compatible:
          - name: hypervisor:libvirt:*
        requires:
          -
            any_of:
              items:
                - name: hypervisor:libvirt:qemu
                - name: hypervisor:libvirt:kvm
              message: 'QEMU or KVM should be enabled'
          -
            any_of:
              items:
                - name: network:neutron:NSX
                - name: network:neutron:DVS
              message: 'NSX or DVS should to be present'

* We can give user possablity to describe new groups or attach elements to
  existing. For such case we can add additional semantic in DSL:
  `type` - describe specific type of component which can define component
  as group.
  `group` - list of links on specific groups for which current component
  belongs.

  Example of third problem solving:

  .. code-block:: yaml

    components:
      - name: network:neutron:ml2
        type: group
      - name: network:neutron:DVS
        group: ['network:neutron:ml2']
        requires:
          - all_of:
            items:
              - name: hypervisor:vmware
              - name: network:neutron:ml2:vlan
            message: 'The VMware DVS plugin requires vCenter as
                      the hypervisor option and VLAN network backend.'


Web UI
======

Implement engine for parsing new predicates and other component DSL semantic.


Nailgun
=======

Data model
----------

Compatible/incompatible relations is duplex. So it's enough describe such
relation in one component and it will be duplicated for all related. But
this logic implemented with a bad practice in GET method [6]_ . It should
processed during pugin install/uninstall. Next `release` model changes are
required:

**Release**

Remove old `wizard_metadata` field in based on [1]_
Rename `components_metadata` field into `core_components_metadata`
Add `all_component_metadata` field which combines core components and
plugin components with all needed modifications.


REST API
--------

N/A


Orchestration
=============

N/A


RPC Protocol
------------

N/A


Fuel Client
===========

N/A


Plugins
=======

Plugin developer should clearly describe restriction with core attributes or
components in environment_config.yaml file.


Fuel Library
============

N/A


------------
Alternatives
------------

* Restrictions for plugin sections can be generated based on incompatible and
  requires relations, but it's much more complicated implmentation.
* Another approach is: implement `expression` logic. It should works in same
  way as for restrictions. Example:

  .. code-block:: yaml

    components:
      - name: 'hypervisor:vmware'
        compatible:
          - name: 'hypervisor:libvirt:*'
        restrictions:
          - condition: "components:hypervisor:libvirt:quemu.value == false
                        or components:hypervisor:libvirt:kvm.value == false"
            message: "One of QEMU or KVM options required"
            action: 'disabled'
          - condition: "not (network:neutron:backend:NSX in components) or
                        not (network:neutron:backend:DVS in components)"
            message: "NSX or DVS components should be present in system"
            action: 'disabled'

  In this case we leave `compatible` relation for marking tested components and
  `restrictions` using instead of `incompatible`/`requires`.


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


---------------------
Infrastructure impact
---------------------

N/A


--------------------
Documentation impact
--------------------

There is should be notice in plugin SDK about describing restrictions
in plugin environment DSL model. Documentation how to use new predicates.


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  * Andriy Popovych <apopovych@mirantis.com>
  * Anton Zemlyanov <azemlyanov@mirantis.com>

Mandatory design review:
  * Vitaly Kramskikh (vkramskikh@mirantis.com)
  * Igor Kalnitsky <ikalnitsky@mirantis.com>


Work Items
==========

* [UI] Provide restrictions handling for plugin section based on enabled
  components.
* [UI] Implement engine for any_of|all_of|one_of|none_of predicates.
* [Nailgun] Change DB model to decrease calls for components API
* [Nailgun] Implement engine for predicates for component validation.

Dependencies
============

* Component registry [0]_.


------------
Testing, QA
------------

TBD


Acceptance criteria
===================

* Plugins sections should be locked for enabling/disabling if plugins not
  compatible with enabled components.

* Requires functionality for enabked or existed components can be declarative
  described.

* User can describe complex logical rules for compatible/incompatible/requires
  relations.


----------
References
----------

.. [0] https://blueprints.launchpad.net/fuel/+spec/component-registry
.. [1] https://bugs.launchpad.net/fuel/+bug/1533765
.. [2] https://bugs.launchpad.net/fuel/+bug/1527312
.. [3] https://bugs.launchpad.net/fuel-plugins/+bug/1537998
.. [4] https://github.com/openstack/fuel-web/blob/stable/8.0/nailgun/static/models.js#L1435-L1437
.. [5] https://github.com/openstack/fuel-web/blob/master/nailgun/static/views/wizard.js#L504
.. [6] https://github.com/openstack/fuel-web/blob/stable/8.0/nailgun/nailgun/objects/release.py#L183-L191
