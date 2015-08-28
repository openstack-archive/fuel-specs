..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=========================================
Extend wizard tab with options via plugin
=========================================

Include the URL of your launchpad blueprint:

https://blueprints.launchpad.net/fuel/+spec/extend-wizard-via-plugin

Implement possibility to extend or modify Fuel cluster wizard tab in
plugins

--------------------
Problem description
--------------------

Some plugins can extend or replace huge components of deployment
process. For instance, introduce new hypervisor type like Xen or new
network type like Contrail. Currently both hypervisor and network
provider are chosen by user on cluster creation wizard, and there's
no way to change it later. In case of plugins, we are forced to choose
wrong option and then change it implicitly by enabling some plugin on
the Settings tab. This is a poor UX, and makes a lot of confusion.


----------------
Proposed changes
----------------

Plugin should have ability to modify wizard tab like it already done
for settings page and describe new options in format similar to
openstack.yaml


Data model
----------

Unlike usual plugin attributes which related to cluster, plugin wizard
data relates to releases which compatible with plugin. Actually each
release has own wizard metadata so main goal of plugin is proper mixing
Plugins can only add additional options like checkboxes or radiobuttons
and merge it with release in recursive way. For example:

Release wizard networking section looks like:

.. code-block:: yaml

  Network:
    manager:
      type: "radio"
      values:
        - data: "neutron-vlan"
          label: "Neutron VLAN"
          restrictions:
            - "some_restriction_here"
          bind:
            - "cluster:net_provider": "neutron"
            - "cluster:net_segment_type": "vlan"

Plugin provides additional network type like contrail

.. code-block:: yaml

  Network:
    manager:
      type: "radio"
      values:
        - data: "neutron-contrail"
          label: "Neutron with contrail"
          restrictions:
            - "some_restriction_here"
          bind:
            - "cluster:net_provider": "neutron"
            - "cluster:net_segment_type": "vlan"

So on output we should get something like this:

.. code-block:: yaml

  Network:
    manager:
      type: "radio"
      values:
        - data: "neutron-vlan"
          label: "Neutron VLAN"
          restrictions:
            - "some_restriction_here"
          bind:
            - "cluster:net_provider": "neutron"
            - "cluster:net_segment_type": "vlan"
        - data: "neutron-contrail"
          label: "Neutron with contrail"
          restrictions:
            - "some_restriction_here"
          bind:
            - "cluster:net_provider": "neutron"
            - "cluster:net_segment_type": "vlan"
            - "settings:contrail.value": true

In case of concurrent changes: each 'data' attribute in radio values can
be checked during plugin certification to avoid duplication. Such approach
gives unique radio options for each plugin.

If plugin enables in Wizard then it should be enabled on Setting tab also.
This can be achive in next way: default attributes metadata for release can
be extend with all compatible plugins like it done now when we get cluster
releated attributes:

.. code-block:: json

    editable : {
        ...
        'contrail': {'value': false},
        'test_plugin': {'value': false}
    }

And then ``value`` should be changed to true only for some of them which was
chosen on Wizard tab. It can be done by binding as usual:
``settings:contrail.value": true``.

Nailgun DB tables changes:

=========  ====================================================
  Table    Operation
=========  ====================================================
 plugins   Add new column ``wizard_metadata`` of ``JSON`` type
=========  ====================================================


REST API
--------

There will be a new API call for getting mixed wizard metadata for
release and all compatible plugins with it.

===== ========================================= ==============================
HTTP  URL                                       Description
===== ========================================= ==============================
GET   /api/v1/releases/<id>/wizard/             Get mixed with plugins wizard
                                                config for specific release
===== ========================================= ==============================

The response format:

.. code-block:: json

    {
        "mode": {},
        "compute": {},
        ...
        "ready": {}
    }


Web UI
------

UI should support calls for new WizardHandler


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

Plugin build provide optional yaml file called `wizard_metadata` by basic
skeleton generation where All additional options for wizard tab will be
described.


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

Mandatory design review:
  * Igor Kalnitsky <ikalnitsky@mirantis.com>


Work Items
----------

* [Nailgun] Extend the ``Plugin`` database model and plugin sync method
  to store wizard into DB.

* [Nailgun] Implement functionality for proper mixing plugin wizard
  metadata with related release wizard and WizardHandler which returns this
  data.

* [UI] Modify code for supporting new wizard handler.

* [FPB] Change default template skeleton for wizard metadata file
  generation. This file can be optional.


Dependencies
------------

N/A


------------
Testing, QA
------------

TBA


Acceptance criteria
-------------------

* Plugins can add additional settings to existing wizard pages new check
  box, radio or text field.

* Plugins can add additional options to existing radio boxes on wizard
  pages.

* Plugins can add additional bindings to existing radio options.

* Plugins can specify restrictions on what other selections can be made
  in the environment (example: vCenter selected as hypervisor, Juniper
  Contrail radio button is grayed out with error message specifying
  that it cannot be used with vCenter)


----------
References
----------

N/A
