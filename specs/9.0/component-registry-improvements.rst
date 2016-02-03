..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===============================
Component registry improvements
===============================

https://blueprints.launchpad.net/fuel/+spec/component-registry-improvements

Improve current Fuel component registry functionality with possibility of
describing complex rules in incompatible/requires relations and restrict plugins
on `Settings` and `Network` tabs.

--------------------
Problem description
--------------------

Currently plugin which provide components for wizard can be enabled\disabled
bypassing wizard configuration. For example: if DVS is disabled option on
wizard, user still can turn-on it in settings without vmware hypervisor.
Also current components DSL model can't cover complex logical cases. For
instance: vmware requires one of network backends: NSXv or DVS, but current
`requires` relation handle items only with `AND` operator.


----------------
Proposed changes
----------------

* Provide restrictions for plugin sections on `Settings` and `Network` tabs.
* Implement `expression` logic for incompatible\requires relations. It should
  work in same way as for restrictions.


Web UI
======

Need to be changed accordingly to support plugin restrictions on Settings and
Network tabs.


Nailgun
=======

Data model
----------

Remove old wizard_metadata field based on  [1]_


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
environment_config.yaml file. For example:



Fuel Library
============

N/A


------------
Alternatives
------------

* Restrictions for plugin sections can be generated based on compatibility
matrix, but it's much more complicated implmentation.


--------------
Upgrade impact
--------------

N/A


---------------
Security impact
---------------

Expressions has limited set of operators (or, and, not, ()) and shouldn't
have impact on security.


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
for components incompatible\requires relations.


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
