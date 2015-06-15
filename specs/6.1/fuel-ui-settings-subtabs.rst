..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Fuel UI Settings Subtabs
==========================================

https://blueprints.launchpad.net/fuel/+spec/TBD


Fuel settigs tab is rather big. It has twelwe or more settigs groups 
each having one or more settig fields. As plugins are added, things 
get more complicated.

Problem description
===================

Fuel settings tab is big and has lots of setting groups. In order 
to organize the settigs, the concept of subtabs is proposed.

Proposed change
===============

Every setting group will be placed in a separate subtab, every subtab
can be selected using a single mouse click.

Alternatives
------------

Contunue to use single page with multiple setting groups.

Data model impact
-----------------

None.

REST API impact
---------------

None.

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

End user will see the new Settings tab appearance in Fuel UI.
No command-line client impact.

Performance Impact
------------------

Not applicable

Plugin impact
-------------

Every plugin can add a setting group and thefore, subtab.
Subtabs number is not limited, althouh it may have impact on 
UI usablity

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

- implement UI subtabs


Dependencies
============

none

Testing
=======

- manual testing
- UI regression test for Settings tab

Documentation Impact
====================

Fuel Users Guide should be updated, Settings tab section

References
==========

http://storage4.static.itmages.com/i/15/0527/h_1432730252_5755438_2c1ca87410.png

