..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===================================================================
Provide the ability to specify IP ranges for all the networks on UI
===================================================================

https://blueprints.launchpad.net/fuel/+spec/support-ip-ranges-for-storage-management-networks-on-ui

It's often needed to specify IP ranges for networks to use them with some
omitted addresses which are reserved or already in use.

--------------------
Problem description
--------------------

When deploying an environment using Fuel it is often necessary to be able to
specify IPs to be excluded from Fuel's auto-provisioning so that the deployment
does not fail due to an IP already being assigned to or reserved for another
resource but in current Fuel UI not all networks allow to do this (storage and
management does not).

With introducing this ability users could omit the IPs that are in use by
setting the range to begin after or end before these IPs - in addition,
multiple IP ranges can be specified, so for users who have an IP in use in the
middle of their range, they can split the range to exclude the IP in use.

----------------
Proposed changes
----------------

Web UI
======

The change affects Fuel UI only. Backend support is already merged in terms of
this bug https://bugs.launchpad.net/fuel/+bug/1365368.
On Fuel UI on Networks tab it will be possible
to specify IP ranges for all networks.

The proposed change to Networks tab:

 .. image:: ../../images/8.0/
 support-ip-ranges-for-storage-management-networks-on-ui/ip_ranges_networks.png

So that existing Networks tab will be extended with new controls, adding IP
ranges.

Default network notation will stay 'cidr' - and ip ranges will be filled in
automatically according to CIDR value. If user specifies IP ranges manually -
network notation should be changed to 'ip_ranges' with appropriate validation
on the fly before saving data (if the value of CIDR is too big or small for
provided IP ranges). In case the user changes the value of CIDR - not
appropriate IP ranges will be highlighted with red and appropriate message will
appear ([tbd] - or another scenario here may be changing ip ranges on the fly
to fit the new CIDR).
All the changes are saved only after user presses 'Save' button.


Nailgun
=======

None


Data model
----------

None


REST API
--------

[TBD]
API description that should be used for saving node network groups choice
should be here.


Orchestration
=============

None


RPC Protocol
------------

None


Fuel Client
===========

None


Plugins
=======

None


Fuel Library
============

None


------------
Alternatives
------------

None

--------------
Upgrade impact
--------------

None


---------------
Security impact
---------------

None


--------------------
Notifications impact
--------------------

None


---------------
End user impact
---------------

None

------------------
Performance impact
------------------

None


-----------------
Deployment impact
-----------------

None


----------------
Developer impact
----------------

None


--------------------------------
Infrastructure/operations impact
--------------------------------

None


--------------------
Documentation impact
--------------------

None


--------------------
Expected OSCI impact
--------------------

None


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  * Aleksandra Morozova, astepanchuk (astepanchuk@mirantis.com)

Mandatory design review:
   * Vitaly Kramskikh, vkramskikh (vkramskikh@mirantis.com)


Work Items
==========

* Add IP range controls to all networks


Dependencies
============

None


------------
Testing, QA
------------

* Manual testing
* UI functional tests should test the presence of ip ranges for networks
* UI unit tests should test the correct data sending to the backend


Acceptance criteria
===================

* It should be possible to provide IP addresses for every network in Fuel UI
* Multiple range start and end points may be set

----------
References
----------
 None
