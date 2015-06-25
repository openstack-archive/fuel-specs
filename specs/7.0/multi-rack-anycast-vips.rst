..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

============================================
Anycast VIPs for multi-rack deployment cases
============================================

For an multi-rack deployment cases we need alternative VIP implementation,
based on anycast OSFP announcements.

Problem description
===================

Anycast announced VIPs not implemented.

Proposed change
===============

VIPs should be assigned in its own network namespace on each
controller. Local route to each VIP should be announced by ospfd.

 .. image:: ../../images/7.0/multirack/anycast_vip.svg
    :width: 25 %

Local brodge used in this case for ability place amount of VIPs to different
network namespaces. This may be required in the future, e.g. when some service
placed into container and required VIP.

VIP assigments, local routing to VIP, bridge and veth-pairs existence should
be managed by Pacemaker.


Alternatives
------------

None, because anycast-based implementation requested by Principal Architect.

Data model impact
-----------------

...in progress...


REST API impact
---------------

...in progress...


UI impact
--------------

...in progress...



Upgrade impact
--------------

...in progress...


Security impact
---------------

...in progress...



Notifications impact
--------------------

N/A.


Other end user impact
---------------------

N/A.


Performance Impact
------------------

N/A


Other deployer impact
---------------------

N/A


Developer impact
----------------

N/A


Implementation
==============

Assignee(s)
-----------

Feature Lead: Sergey Vasilenko

Mandatory Design Reviewers: Andrew Woodward, Chris Clason

Developers: Aleksey Kasatkin, Ivan Kliuk, Sergey Vasilenko, Vitaly Kramskikh

QA: Anastasiia Urlapova


Work Items
----------

...in progress...


Dependencies
============

N/A


Testing
=======

...in progress...

Acceptance Criteria
-------------------

...in progress...


Documentation Impact
====================

The documentation should describe new networking architecture of Fuel,
changes and new features in networking configuration process in UI.


References
==========

N/A