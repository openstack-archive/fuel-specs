..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Add http connection tracking to fuel-agent
==========================================

https://blueprints.launchpad.net/fuel/+spec/ibp-reconnect [1]_

Currently, fuel-agent uses very simple and silly approach of downloading
images. Also it lacks proper http connection tracking procedure. More reliable
and less error prone mechanism of dealing with received data should be
implemented for it.

Problem description
===================

For now, fuel agent doesn't:

* handle any of connection error

* handle any of HTTP error

* handle any possible ways of http connection failures during the image data
  retriving (eg.: the connection being closed/lost or got stuck)

* https://bugs.launchpad.net/fuel/+bug/1389120 [2]_


Proposed change
===============

Proper connection tracking and data retrival procedure to be implemented. It
should handle at least with:

* http errors (4xx and other possible).

* connection errors. (dns lookup/name resolution error, timeouts, etc.)

* reconnect if something goes wrong, eg.: the connection got stuck and no new
  data can't be retrevied. Dealing with unexpectedly closed connection.


In order to implement all that stuff, all changed will be concentrated in
fuel-agent's side in HttpUrl class from utils/artifact_utils.py.

Alternatives
------------

Use another application transport layer which has already built-in data
integrity mechanism and is ready to deal with real world networking issues
such as bittorrent and the similar one based on p2p networking approaches. But
it's completely out of scope for 6.1.

Data model impact
-----------------

None

REST API impact
---------------

None

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
  <agordeev@mirantis.com>

Work Items
----------

- *implement connection tracking for fuel-agent*

Dependencies
============

None

Testing
=======

Testing approach

- Deploy master node
- Start slave VM and boot it to bootstrap ramdisk
- Wait for slave node is being discovered
- Start deployment with image based provision while emulating various network
  connectivity issues:
  image downloading could be detected by fuel-agent log or image
  hosting service log analyzing;
  to emulate various issues iptables could be used;
- The deployment has to be successful

Documentation Impact
====================

None

References
==========

.. [1] https://blueprints.launchpad.net/fuel/+spec/ibp-reconnect
.. [2] https://bugs.launchpad.net/fuel/+bug/1389120
