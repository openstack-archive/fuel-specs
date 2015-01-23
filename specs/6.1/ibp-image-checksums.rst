..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=====================================================
Add image checksums to image downloader in fuel-agent
=====================================================

https://blueprints.launchpad.net/fuel/+spec/ibp-image-checksums [1]_

Problem description
===================

For now, fuel agent doesn't ensure received image's data integrity.
If any portion of data will be corrupted in any way which transport
layer (TCP) can't recognise, then the image to be deployed
will be corrupted. We need Fuel Agent to be able to do compare checksums
so as to make sure target OS will be bootable and will work.


Proposed change
===============

Currently we have a specific data structure for describing images that are
available for installing on a node
::

  image_data:
      /:
          uri: "http://host:port/path/to/root/image"
          format: "ext4"
          container: "gzip"

This data structure is to be extended with 2 fields: `md5` and `size` which we
then can use on the agent side to compare what we put on a hard drive with what
is supposed to be put.
As we are going to support compressed images by default (.gz) we need to know
the actual data size of uncompressed image to be able to verify what was
written to disk during provisioning.
Those two new fields of `image_data` will be set on the final stage of target
image building procedure.

New structure
::

  image_data:
      /:
          uri: "http://host:port/path/to/root/image"
          format: "ext4"
          container: "gzip"
          md5: "cfcd208495d565ef66e7dff9f98764da"
          size: 131021

Fuel Agent is to follow this simple procedure:

* download an image
* put an image on a hard drive
* read what is just written
* calculate md5 sum
* compare two sums

Alternatives
------------

Use another application transport layer which has already built-in data
integrity mechanism and ready to deal with real world networking issues such as
bittorrent and the similar based on p2p networking approaches. But it's
completely out of scope for 6.1.

Data model impact
-----------------

None

REST API impact
---------------

None

Upgrade impact
--------------

MD5 sum should be added into the data structure which describes an image.

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

Calculating hash digest for the 350M image takes even less than 10 secs (only
depending on disk I/O bandwidth). MD5 is very fast, so it doesn't has any
potential performance impact on the provisioning system.

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

* *Modify Fuel Agent to make it able to deal with md5 sums of images*
* *Modify upgrade script to make it able to add md5 fields into data
  that describes target images*

Dependencies
============

None

Testing
=======

Testing approach

- Deploy master node
- Start slave VM and boot it to bootstrap ramdisk
- Wait for slave node is being discovered
- Start deployment with image based provision while emulating md5 mismatch by
  modifying `md5` field of image_data.
- The deployment has to be successful or not depending on whether md5 matches
  an image or not

Documentation Impact
====================

Documentation needs to be changed so as to note this md5 checking mechanism

References
==========

.. [1] https://blueprints.launchpad.net/fuel/+spec/ibp-image-checksums

