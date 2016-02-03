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

--------------------
Problem description
--------------------

Currently plugin which provide components can be enabled/disabled after
bypassing wizard configuration. For example: if DVS is disabled option on
wizard, user still can turn-on it in settings without vmware hypervisor [2]_.
Also current components DSL model can't cover complex logical cases. Some of
them:

  * How to check that component exist in system (`requires` relation checks
    that components from list have been enabled).
  * How automatically enabled some components if they are required for option
    was chosen by user.
  * Check components are mutually exclusive or not.

----------------
Proposed changes
----------------

* Provide restrictions for plugin sections on `Settings` and `Network` tabs.
* Extend components DSL model with additional semantic:
  `one_of` - checks that only one element from list should be processed
  `all_of` - checks that all elements from list are processed
  `any_of` - checks that any element from list can be processed
  `not` - checks that element from list shouldn't e processed. Can be combined
  with `one_of`|`all_of`|`any_of`. Concepts are taken from [4]
  `needs` - list of components which should be present in system for using
  current component.
  `required` - means that component is required in any case for current
  component and will be automatically checked.
  `is_group` - describe specific type of component which groups not mutually
  exclusive components.

Example:

  .. code-block:: yaml

    components:
      - name: hypervisor:libvirt:qemu
      - name: hypervisor:vmware
        compatible:
            - name: libvirt:*
        requires:
          hypervisors:
            any_of:
              items:
                - name: hypervisor:libvirt:*
              message: 'QEMU or KVM should be enabled'
        needs:
          networks:
            one_of:
              items:
                - name: network:neutron:backend:NSX
                - name: network:neutron:backend:DVS
              message: 'NSX or DVS should to be present'
      - name: network:neutron:ml2
        is_group: true
      - name: network:neutron:backend:DVS
        group: network:neutron:ml2
        requires:
          hypervisors:
            - name: vmware
          networks:
            - name: neutron:ml2:vlan
      - name: additional_service:mongo
      - name: additional_service:ceilometer
        required:
          - name: additional_service:mongo


Web UI
======

Need to be changed accordingly to support plugin restrictions on Settings and
Network tabs.


Nailgun
=======

Data model
----------

**Release**

Remove old `wizard_metadat` field in based on [1]_
Rename `components_metadata` field into `core_components`
Add `all_component_metadata` field which combine core components and
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

Plugin developer should clearly describe restriction with other plugin in
environment_config.yaml file.


Fuel Library
============

N/A


------------
Alternatives
------------

* Restrictions for plugin sections can be generated based on compatibility
  matrix, but it's much more complicated implmentation.
* Implement `expression` logic for incompatible\requires relations. It should
  work in same way as for restrictions. Example:

    .. code-block:: yaml

      components:
        - name: 'hypervisor:vmware'
          compatible:
            - name: 'hypervisor:libvirt:*'
          restrictions:
            - condition: "components:hypervisor:libvirt:quemu == false or
                          components:hypervisor:libvirt:kvm == false"
              message: "One of QEMU or KVM options required"
            - condition: "not (network:neutron:backend:NSX in components) or
                          not (network:neutron:backend:DVS in components)"
              message: "NSX or DVS components should be present in system"

  In this case we leave `compatible` relation for marking tested components and
  `restrictions` are replacing for `incompatible`/`requires`. Statement `in`
  is introduced to handle case when plugin provides incomplite set of components
  which are not working without other plugins. For instance: vmware plugin will
  provide only hypervisor which not makes many sense without one of network
  backends (DVS/NSX).


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
in plugin environment DSL model and about possability to write expressions
for components incompatible/requires relations.


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  * Andriy Popovych <apopovych@mirantis.com>

Other contributors:
  * Anton Zemlyanov <azemlyanov@mirantis.com>

Mandatory design review:
  * Vitaly Kramskikh (vkramskikh@mirantis.com)
  * Igor Kalnitsky <ikalnitsky@mirantis.com>


Work Items
==========

* Provide restrictions handling for plugin section on UI
* Provide expressions handling for incompatible/requires relations for
  validation in Nailgun.
* Provide expressions handling for incompatible/requires relations in UI
  for better UX on wizard tab.


Dependencies
============

* Component registry [0]_.


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

.. [0] https://blueprints.launchpad.net/fuel/+spec/component-registry
.. [1] https://bugs.launchpad.net/fuel/+bug/1533765
.. [2] https://bugs.launchpad.net/fuel/+bug/1527312
.. [3] https://bugs.launchpad.net/fuel-plugins/+bug/1537998
.. [4] https://github.com/json-schema/json-schema/wiki/anyOf,-allOf,-oneOf,-not
