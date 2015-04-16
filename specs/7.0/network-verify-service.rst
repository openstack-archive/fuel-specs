..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Network verification service
==========================================

https://blueprints.launchpad.net/fuel/+spec/network-verify-service

Current network verification architecture has strong integration
with nailgun which performs another function such as deployment
configuration service. In future scaling network verification
functionality like adding new tasks for verify can be hard implemented
and support. Also now it has very pure output information like what’s
going behind the scene for client. Base on SOP it wiil be logically to
move network verification functionality into separate service.


Problem description
===================

* Network verification feature is independent enough to stop keeping
  the code in Nailgun/Astute and complicating them with it.

* It not so easy to extend verification with new checking task.

* Future scale of curent implementation will be hard to support.

* It doesn't support bonds checking.

* Results of tests in case of failures are discouraging now. It
  doesn't try to collapse the results somehow (a single foreign DHCP
  server produces a separate message for each node in cloud).


Proposed change
===============

* Create separate service to run tasks with different kind of network
  checks.

* Provide an easy way to understand which checks are available to a
  cluster, which is running right now, and what are the results of
  checks in past.

* Implement functionality to run not all of them but certain checks
  only.

* Service should have pluggable architecture for adding new extensions
  with checking tasks.

* Provide more informative response on UI side.

* Network verify should has basic validation for input parameters.

Alternatives
------------

Make network verify as part of OSTF.
Keep and support functionality in nailgun.


Data model impact
-----------------

None


REST API impact
---------------

GET /api/network_verify/cluster/:id/tests

returns tests descriptions as array of objects

response:

.. code-block:: json

    {
        [
            {
                "id": 123,
                "name": 'Foreign DHCP'
                "description": 'Check for foreign DHCP Servers in network'
            }
        ]
    }

PUT /api/network_verify/cluster/:id/run

starts the network check with specified tests

request:
.. code-block:: json

    {
        [123, 234]
    }

response:
.. code-block:: json

    {
        "status": "running",
        "name": "verify_networks",
        "cluster": 1,
        "uuid": "02335959-d79c-4d2d-a007-6288890cfca9"
    }

uuid is id of main task

GET /api/network_verify/cluster/:id/tasks

return all the tasks associated with the check. Returns finished,
running and waiting tasks.

response:
.. code-block:: json

    {
        [
            {
                "id": 123
                "status": "running",
                "name": "DHCP Check",
                "cluster": 1,
                "result": [],
                "progress": 18,
                "message": null,
                "uuid": "02335959-d79c-4d2d-a007-6288890cfca9"
            },
            {
                "id": 234
                "status": "wait",
                "name": "Connectivity Test",
                "cluster": 1,
                "result": [],
                "progress": 0,
                "message": null,
                "uuid": "02335959-d79c-4d2d-a007-6288890cfca9"
            }
        ]
    }

Upgrade impact
--------------

None

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

None

Plugin impact
-------------

When Fuel plugin is installed it also install a Python module to a
container which provides stevedore endpoints for network verificatoin
service. Fuel plugin also publish some executable entities (shell
scripts, python stuff, etc) via web server (like it does now for
plugin’s Puppet modules).


Other deployer impact
---------------------

None

Developer impact
----------------

None

Infrastructure impact
---------------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  * Andrey Danin (gcon-monolake)
  * Andriy Popovich (popovych-andrey)
  * Anton Zemlyanov (azemlyanov)


Work Items
----------

* Implement REST API task service for running diffrent checks. Due to
  openstack community propose pecan web framework will be used. [3]
* Describe protocol for communication with nailgun and UI services.
* Provide pluggable architecture using stevedore library [4]


Dependencies
============

None

Testing
=======

None

Documentation Impact
====================

None

References
==========

[1] L2/L3 Network checking
  (https://blueprints.launchpad.net/fuel/+spec/l23-net-checker)
[2] Extandble verification handler for nailgun and commands for cli
  (https://blueprints.launchpad.net/fuel/+spec/extandable-verification-hanlder)
[3] Pecan web framework
  (http://pecan.readthedocs.org)
[4] Stevedore library
  (http://docs.openstack.org/developer/stevedore/index.html)
