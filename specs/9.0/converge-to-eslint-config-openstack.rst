..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

================================================
Converge to OpenStack Javascript Coding Standart
================================================

https://blueprints.launchpad.net/fuel/+spec/converge-to-eslint-config-openstack

Fuel UI is using independent ESLint config to lint JavaScript code. Since Fuel
in a part of OpenStack, we must use OpenStack coding style.


-------------------
Problem description
-------------------

There is eslint-config-openstack project which contains .eslintrc with
rules for all OpenStack projects. Fuel's .eslintrc is significantly different -
it contains extra rules and different values. Switching to OpenStack style
will make it easier for external contributors to contribute.


----------------
Proposed changes
----------------

Fuel's .eslintrc needs to be rewritten to extend eslint-config-openstack. It's
possible to disable some rules from eslint-config-openstack if there is a valid
reason, but the number of such rules should be minimal. It's ok for extra rules
(which are not present in eslint-config-openstack) to stay. React and ES6 rules
should also stay in .eslintrc.

Fuel UI code should be updated accordingly.


Web UI
======

Fuel UI code needs to be fixed according to the new rules to pass CI.


Nailgun
=======


Data model
----------

None


REST API
--------

None


Orchestration
=============


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

It will take some time for active contributors to adapt to the new coding
style.

For new contributors which are familiar with other OpenStack projects it
will be easier to start contributing.


---------------------
Infrastructure impact
---------------------

None


--------------------
Documentation impact
--------------------

None


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  vkramskikh@mirantis.com

Other contributors:
  astepanchuk@mirantis.com
  jkirnosova@mirantis.com
  kpimenova@mirantis.com

Mandatory design review:
  astepanchuk@mirantis.com
  jkirnosova@mirantis.com
  kpimenova@mirantis.com


Work Items
==========

The rules should be enabled one-by-one. The diffs can be very large, so it's
preferred to finish transition at the beginning of the development cycle to
avoid conflicts.


Dependencies
============

* eslint-config-openstack NPM module should be added to package.json as a
  devDependency.

-----------
Testing, QA
-----------

Fuel CI runs ESLint as a part of verify-fuel-web-ui job, so all the changes
are tested automatically.


Acceptance criteria
===================

The following rules need to be used from eslint-config-openstack (i.e. they
shouldn't be overridden in Fuel's .eslintrc):

* complexity

* eqeqeq

* no-script-url

* indent

* one-var

* max-len

* no-sync


----------
References
----------

http://eslint.org/
http://git.openstack.org/cgit/openstack/eslint-config-openstack
http://git.openstack.org/cgit/openstack/fuel-web/tree/nailgun/.eslintrc?h=stable/8.0
