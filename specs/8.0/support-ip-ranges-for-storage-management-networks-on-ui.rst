..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===================================================================
Provide the ability to specify IP ranges for all the networks on UI
===================================================================

https://blueprints.launchpad.net/fuel/+spec/support-ip-ranges-for-storage-management-networks-on-ui

It's often needed to specify ip ranges for storage and management network to
use ip ranges with some omitted addresses which are reserved or already in use.

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

The change affects Fuel UI only. On Fuel UI on Networks tab it will be possible
to specify ip ranges for all networks.

The proposed change to Networks tab:

 .. image:: ../../images/8.0/
 support-ip-ranges-for-storage-management-networks-on-ui/ip_ranges_networks.png

So that existing Networks tab will be extended with new controls, adding ip
ranges.


Nailgun
=======

None


Data model
----------

None


REST API
--------

None


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

Just after merge this change will let user to set ip ranges for all the
networks provided.


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


Who is leading the writing of the code? Or is this a blueprint where you're
throwing it out there to see who picks it up?

If more than one person is working on the implementation, please designate the
primary author and contact.

Primary assignee:
  * Aleksandra Morozova (astepanchuk@mirantis.com)

Mandatory design review:
   * Vitaly Kramskikh (vkramskikh@mirantis.com)


Work Items
==========

* Add ip range controls to Storage and Management networks


Dependencies
============

None


------------
Testing, QA
------------

* Create a cluster and open Networks tab. It should be possible to provide ip
ranges for all networks.


Acceptance criteria
===================

* Every network for which Fuel may allocate IP addresses must be in the ranges
  annotation so multiple range start and end points may be set

----------
References
----------
 None
