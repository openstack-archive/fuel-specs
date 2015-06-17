..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Fuel Multiple Hypervisor Networking
==========================================

https://blueprints.launchpad.net/fuel/+spec/TBD

Multiple hypervisor support and Nova Network removal require to
redesign the Fuel create cluster wizard. There will be possibility
to select multiple Neutron ML2 drivers for different hypervisors.

Problem description
===================

Multiple hypervisors can use different network backends (ML2 drivers).
As Nova Network is to be removed, the Fuel cluster wizard have to 
be changed to support multiple hypervisors and multiple network backends

Proposed change
===============


1. Modify Compute wizard pane to support multiple hypervisors 
2. Modify Network wizard pane to support multiple network backends

Alternatives
------------

Make a single hypervisor deploy only.

Data model impact
-----------------

openstack.yaml wizard metadata should be updated to define new wizard
pane design.

REST API impact
---------------

/api/releases Nailgun API is affected, will return new wizard metadata

Upgrade impact
--------------

No extrnal dependencies added

Security impact
---------------

No impact

Notifications impact
--------------------

No impact

Other end user impact
---------------------

End user will see the new wizard's Compute and Network panes in Fuel UI.
No command-line client impact.

Performance Impact
------------------

Not applicable

Plugin impact
-------------

Plugins can add new network backends and hypervisors.
Nailgun should merge plugins data with openstack.yaml

Other deployer impact
---------------------

No impact

Developer impact
----------------

No impact

Infrastructure impact
---------------------

No impact

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  
  Anton Zemlyanov - azemlyanov

Other contributors:

Work Items
----------

- update wizard's Compute Pane to use checkboxes
- update wizard's Network Pane to use Neutron and ML2 drivers


Dependencies
============

none

Testing
=======

- manual testing
- UI wizard functional tests update

Documentation Impact
====================

Fuel Users Guide should be updated, Create cluster wizard section

References
==========

http://storage4.static.itmages.com/i/15/0617/h_1434550933_8693687_954fa15ccf.png
http://storage4.static.itmages.com/i/15/0617/h_1434551033_4332075_8e85a8fe7d.png

