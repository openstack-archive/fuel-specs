..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===========================
Downloadable Ubuntu Release
===========================

https://blueprints.launchpad.net/fuel/+spec/downloadable-ubuntu-release

Before using Ubuntu release a cloud operator should download an Ubuntu ISO
from the official site and upload it to Fuel.


Problem description
===================

None


Proposed change
===============

* Remove vanilla Ubuntu packages from the ISO.

  All vanilla Ubuntu packages MUST be removed from the ISO. All those
  packages that are required for OpenStack installation could be kept
  on the ISO.

* Mark Ubuntu as unavailable release.

  Ubuntu release may appear on UI, but it MUST be unavailable for creating
  new environments. All attempts to do so SHOULD lead cloud operators to
  a page with instructions how to make it available.

* Provide an API call for uploading official Ubuntu ISO.

  The provided API call SHOULD be used by both Fuel UI and Fuel CLI in order
  to upload Ubuntu ISO and make Ubuntu release available for deployment.

  See "REST API impact" section for details.

* Provide state mechanism for release model.

  In order to distinguish releases which are ready for deployment and which
  are not, a set of possible states SHOULD be added.

  See "Data model impact" for details.

Alternatives
------------

None


Data model impact
-----------------

Currently, there is a ``.state`` attribute in the release model which was
introduced for similar purpose a time ago. It's unused now, so it could be
fully reworked to fit our needs.

There will be two possible states:

* ``available`` (general usecase, available for deployment)
* ``unavailable`` (present on ui, but can't be chosen for new envs)

Initial ``.state`` should be loaded from the ``openstack.yaml``.

Database migration should set ``.state = available`` for previous releases.

REST API impact
---------------

The Nailgun should provide a new API handler for uploading ISO. The
uploading could be performed by POST method to the following URI::

    /releases/<id>/upload/iso/

where ``<id>`` is a release id for which the ISO will be uploaded.

Uploaded ISO should be verified by SHA1 checksum. In case of success -
the release should change its state from ``unavailable`` to ``available``;
otherwise ``400 Bad Request`` should be returned.

The API handler should return ``405 Method Not Allowed`` for releases
where ``.state != unavailable``.

Upgrade impact
--------------

None

Security impact
---------------

None

Notifications impact
--------------------

When Ubuntu ISO was successfully uploaded, the notification should be sent
that Ubuntu release became available now.

Other end user impact
---------------------

Before deploying OpenStack cluster on Ubuntu, end users should manually
download official Ubuntu ISO and upload it using either Fuel UI or Fuel CLI.

The workflow would look like::

    User             Ubuntu.com    Fuel
     +                  +           +
     |   download iso   |           |
     | +--------------> |           |
     |       done       |           |
     | <--------------+ |           |
     |                  |           |
     |                  |           |
     |    upload iso    |           |
     | +--------------------------> |
     |       done       |           |
     | <--------------------------+ |
     |                  |           |
     |                  |           |
     |    create env    |           |
     | +--------------------------> |
     |       done       |           |
     | <--------------------------+ |
     |                  |           |
     +                  +           +


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

* Igor Kalnitsky <ikalnitsky@mirantis.com>

Other contributors:

* Fuel UI
* Fuel QA

Work Items
----------

* Change release's ``.state`` attribute to cover our case
  (see Data model impact for details).

* Implement Nailgun handler for uploading ISO.


Dependencies
============

None

Testing
=======

Generally, the tests are the same. If we can deploy OSt on Ubuntu and it
pases our tests then all works fine.

Still, since Ubuntu isn't available by default, we have to change our
tests to upload Ubuntu ISO before tests.


Documentation Impact
====================

The documentation should have a section that covers how to enable
Ubuntu release for deployment.


References
==========

* #fuel-dev on freenode
