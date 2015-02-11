..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=======================
Consume External Ubuntu
=======================

https://blueprints.launchpad.net/fuel/+spec/consume-external-ubuntu

Before using Ubuntu release a cloud operator should specify both
Ubuntu and OpenStack mirrors.


Problem description
===================

Currently, it's hard to provide Ubuntu's upstream updates, since we don't
fetch them from official mirrors. Therefore, users are vulnerable for
security issues for a long time.

This spec provides a detail plan how to solve this problem.


Proposed change
===============

#. Set both Ubuntu and OpenStack mirrors per cluster.

   Users SHOULD be prompted to provide both Ubuntu and OpenStack mirrors
   in cluster creation wizard. By default, Canonical mirror for Ubuntu
   and Fuel mirror for OpenStack SHOULD be used.

   All Ubuntu packages SHOULD be removed from the Fuel ISO and provided
   mirrors SHOULD be used for cluster deploying.

   See "Data model impact" and "UX impact" for details.

#. Generate provisioning images per cluster.

   Since we're going to specify mirrors per cluster, different clusters may
   have different set of mirrors. Therefore, we need to generate provisioning
   images per cluster.

   Provisioning images SHOULD be generated in background by sending a task
   to Astute. When it's done the cluster SHOULD be ready for deployment.

   See "Data model impact" and "RPC impact" for details.

#. Provide advances settings in "DEBUG" mode.

   In DEBUG mode, Fuel UI SHOULD ask users to specify additional mirrors
   and set priorities for them.


Alternatives
------------

None

Data model impact
-----------------

Ubuntu release SHOULD have a new set of *editable* attributes that allows
us to specify a set of repos and their options (e.g. priority).

Here's the example and proposed format:

.. code:: yaml

    attributes_metadata:
      # ...
      editable:
        # ...
        repo_metadata:
          - type: "deb"
            uri: "http://archive.ubuntu.com/ubuntu/"
            flavour: "trusty"
            space: "main"
            priority: 1001

          - type: "deb"
            uri: "http://mirror.fuel-infra.org/fwm/6.1/ubuntu/"
            flavour: "trusty"
            space: "main"
            priority: 1002

Since we're going to generate provisioning images, we also need to introduce
a new task - *build_ibp_images*.

UX impact
---------

* When users create a cluster using Fuel UI they will be asked for specifying
  both Ubuntu and OpenStack mirrors.

* When it's done and the cluster is created, a task for building provisioning
  images will be sent to Astute.

* Users are unable to start cluster deploying until provisioning images are
  built successful.

* If users use preseed installation way they are not required to build
  provisioning images and therefore they can run deploying at any time.

* Users are required to have Internet connection on Master Node. If they
  want to have offline mode, they need to create local mirrors and
  specify them in cluster creation wizard.


RPC impact
----------

In order to run building provisioning images the following RPC call
SHOULD be sent to Astute:

.. code:: json

    {
        "api_version": "1",
        "method": "execute_tasks",
        "respond_to": "build_ipb_images_resp",
        "args": {
            "task_uuid": "_task_uuid4_",
            "tasks": [
                {
                    "id": "extract_repo",
                    "uids": ["master"],
                    "type": "shell",
                    "parameters": {
                        "cmd": "_command_for_building_images_",
                        "timeout": 180
                    }
                }
            ]
        }
    }

.. note::

    the ``_command_for_building_images_`` will be executed inside
    mcollective container, so we need to make sure that we have
    all required stuff

and in order to receive its result the ``build_ipb_images_resp`` SHOULD
be implemented in Nailgun's receiver daemon.

REST API impact
---------------

None.

Upgrade impact
--------------

There's no upgrade impact. Old releases are kept "As Is", while the new
one will follow workflow defined in this spec (just like after fresh
master node installation).

Security impact
---------------

Cloud security will be improved, since cloud will get all latest security
updates directly from upstream.

Notifications impact
--------------------

A notification SHOULD be sent when provisioning images were built.

Other end user impact
---------------------

None.

Performance Impact
------------------

Ubuntu deployment time will be increased due to the fact that the packages
will be retrieved directly from the third-party servers. But when the
packages get cached the time should be the same.

Other deployer impact
---------------------

* Some caching mechanism SHOULD be used in order to reduce deployment
  time. It may be ``squid``, ``approx``, whatever.

Developer impact
----------------

* Developers won't be able to build ISO with custom packages anymore.
  Instead, they SHOULD use a regular ISO and specify custom mirror
  with higher priority in cluster creation wizard.

Implementation
==============

Assignee(s)
-----------

Primary assignee:

* Igor Kalnitsky <ikalnitsky@mirantis.com>

Developers:

* Vladimir Kozhukalov <vkozhukalov@mirantis.com>
* Yulia Aranovich <jkirnosova@mirantis.com>

Work Items
----------

* Provide possibility to specify custom Ubuntu and OpenStack mirrors with
  custom priorities.

* Add controls for specifying custom mirrors on Fuel UI.

* Add options for specifying custom mirrors in python-fuelclient.

* Implement the ``build_ibp_images`` task.

* Consider to use a caching mechanism.


Dependencies
============

* `Ubuntu 14.04 support
  <https://blueprints.launchpad.net/fuel/+spec/support-ubuntu-trusty>`_

* `Separate MOS from Linux repos
  <https://blueprints.launchpad.net/fuel/+spec/separate-mos-from-linux>`_

* `Building target images with Ubuntu on master node
  <https://blueprints.launchpad.net/fuel/+spec/ibp-build-ubuntu-images>`_


Testing
=======


.. important::

    Need to be discusses with QA. Seems like CI infra changes are required.


Documentation Impact
====================

The documentation SHOULD cover how the end user workflow has been changed
for deploying clusters on Ubuntu.


References
==========

* #fuel-dev on freenode
