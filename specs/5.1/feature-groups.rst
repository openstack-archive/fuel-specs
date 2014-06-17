==============
Feature Groups
==============

https://blueprints.launchpad.net/fuel/+spec/feature-groups

We need a mechanism to build Fuel ISOs with different "flavors". Currently,
it is only possible to specify MIRANTIS=yes flag to create an ISO with
Mirantis logo, but we need to configure ISO build in a more flexible way.

Problem description
===================

For now, we need have two options for ISO build:

* Whether or not to put Mirantis logo to the footer

* Whether or not to allow usage of experimental features

The resulting ISO may have both or none of them. It is also be good if any of
these options could be changed on a working master node.

Proposed change
===============

A key "feature_groups" needs to be added to "VERSION" section of settings.yaml.
It should contain a list of strings, which presence in this list should be
checked in a few places such as footer, settings tab, role list, wizard, etc.
These checks also can be written as restrictions in configs::

    values:
      - data: "kernel_lt"
        label: "EXPERIMENTAL: Use Fedora longterm kernel"
        description: "Install the Fedora 3.10 longterm kernel"
        restrictions:
          - "'experimental' in version:feature_groups"

ISO build scripts should be modified to use FEATURE_GROUPS environment
variable. Its value should contain a list of feature groups separated by comma
to put into settings.yaml. Example::

    make FEATURE_GROUPS=mirantis,experimental iso

If FEATURE_GROUPS is undefined, only "experimental" feature group should be
enabled. Handling of MIRANTIS environment variable should be removed.

Alternatives
------------

This can also be achieved by implementing these features as plugins, so this
approach should probably be considered as a temporary solution until plugin
system is implemented properly.

Data model impact
-----------------

None

REST API impact
---------------

A new field "feature_groups" should be added to /api/version response. Field
"mirantis" should be removed.

Security impact
---------------

None

Notifications impact
--------------------

None

Other end user impact
---------------------

None

Performance Impact
------------------

Minimal. UI should perform checks whether or not to show settings/roles/other
controls dependent on feature groups.

Other deployer impact
---------------------

None

Developer impact
----------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  vkramskikh

Other contributors:
  dpyzhov

Work Items
----------



Dependencies
============

None

Testing
=======

Should be tested manually. Acceptance criteria:

* ISO built with "mirantis" group should have the logo in the footer
* ISO built with "experimental" group should have Zabbix role

Documentation Impact
====================

Processes of specifying feature groups for ISO build and modifiying them on
deployed master node should be documented.

References
==========

None
