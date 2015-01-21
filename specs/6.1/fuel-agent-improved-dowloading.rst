..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Improving image downloading in fuel-agent
==========================================

https://blueprints.launchpad.net/fuel/+spec/fuel-agent-improved-dowloading [1]_

Currently, fuel-agent uses very simple and silly approach of downloading
images. It doesn't ensure received data integrity by checksumming. Also it
lacks proper http connection tracking procedure. More reliable and more error
prone mechanism of dealing with received data should be implemented for it.

Problem description
===================

For now, fuel agent doesn't:

* handle any errors or connection issues when trying to download images. If any
  error appear, then the provision will be failed. If the connection will get
  stuck, then the provision will be failed even.

* ensure received image's data integrity. If any portion of data will be
  corrupted in any way which transport layer (TCP) can't recognise, then the
  image to be deployed will be corrupted.

* https://bugs.launchpad.net/fuel/+bug/1389120

Proposed change
===============

Proper connection tracking and data retrival procedure to be implemented. It
should handle at least with:

* http errors (4xx and other possible).

* connection errors. (dns lookup/name resolution error, timeouts, etc.)

* reconnect if something goes wrong, eg.: the connection got stuck and no new
  data can't be retrevied. Dealing with unexpectedly closed connection.

* digesting to ensure data integrity of received chunks of data.

In orger to implement all that stuff, most changed will be concetraced in
fuel-agent's side. Only images digests will be added to build script.

So the proposed changes:

* List of image chunk digests will be added to image metadata rigth after
  image's building to profile.yaml. Chunk size is questionable and TBD.

* Connection tracking procedure will be implemented for HttpUrl class from
utils/artifact_utils.py.

* Data integrity checks will be implemented for HttpUrl too.

MD5 hash digest algorithm will be used as it's very fast and quiet enough for
our case.

Alternatives
------------

Use another application transport layer which has already built-in data
integrity mechanism and ready to deal with real world connection issues such as
bittorrent and the similar based on p2p networking approaches. But it's
completely out of scope for 6.1.

Data model impact
-----------------

Adding list of image's chunck digests to images metadata file to profile.yaml.
No impact otherwise.

REST API impact
---------------

None

Upgrade impact
--------------

Target images metadata should be upgraded and consits of chunks digests

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

Calculating hash digest for chunks takes very small amount of time. MD5 is very
fast, so it doesn't has any potential performance impact on the system.

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
  <vkozhukalov@mirantis.com>

Work Items
----------

- *Connection tracking*
- *Data integrity checks*
- *Upgrade script*
 
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
  connectivity issues
- The deployment has to be successful

Documentation Impact
====================

None

References
==========

.. [1] https://blueprints.launchpad.net/fuel/+spec/fuel-agent-improved-dowloading

