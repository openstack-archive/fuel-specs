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

   Users SHOULD be prompted to provide both Ubuntu and OpenStack repos
   in cluster creation wizard. By default, Canonical repo for Ubuntu
   and Fuel repo for OpenStack SHOULD be used.

   The repos SHOULD be specified using Debian format:

   .. code::

       deb http://archive.ubuntu.com/ubuntu/ trusty main universe
       deb-src http://pl.archive.ubuntu.com/ubuntu/ trusty main multiverse

   All Ubuntu packages SHOULD be removed from the Fuel ISO and provided
   mirrors SHOULD be used for cluster deployment.

   .. note:: We SHOULD NOT use mirror:// protocol for default repos,
             because we won't know which repos were used and hence
             debugging will be painful.

   See "Data model impact", "UX impact" and "Developer impact" for details.

#. **OPTIONAL**: Check that provided repos contain all required packages

   We SHOULD check that all required packages are available and therefore
   successful deployment is possible.

   Since Nailgun knows nothing about required packages and this information
   SHOULD NOT be hardcoded (it's a dynamic), we obviously HAVE TO do it
   by executing some asynchronous task. The task SHOULD:

   * retrieve a list of required packages;
   * check their availability;
   * report result back to Nailgun.

   .. note:: Since we're moving toward declarative tasks, the task
             will be executed inside MCollective container. So the
             container SHOULD be ready for doing this.

#. Generate provisioning images per cluster.

   Since we're going to specify mirrors per cluster, different clusters may
   have different set of mirrors. Therefore, we need to generate provisioning
   images per cluster.

   Provisioning images SHOULD be generated in background by sending a task
   to Astute. When it's done the cluster SHOULD be ready for deployment.

   See "Data model impact" and "RPC impact" for details.


Alternatives
------------

None

Data model impact
-----------------

Release model SHOULD have a new set of *editable* attributes that allows
us to specify a set of repos and their options (e.g. priority).

Here's the proposed format for Debian-based distributives:

.. code:: yaml

    attributes_metadata:
      # ...
      editable:
        # ...
        repo:
          repo_metadata:
            - type: "deb"
              name: "OS"
              uri: "http://archive.ubuntu.com/ubuntu/"
              suite: "trusty"
              section: "main"
              priority: 1001

            - type: "deb"
              name: "Fuel"
              uri: "http://mirror.fuel-infra.org/fwm/6.1/ubuntu/"
              suite: "mos6.1"
              section: "main"
              priority: 1002

Here's the proposed format for RHEL-based distributives:

.. code:: yaml

    attributes_metadata:
      # ...
      editable:
        # ...
        repo:
          repo_metadata:
            - type: "rpm"
              name: "OS"
              uri: "http://mirror.centos.org/centos-6/6/os/x86_64/"
              priority: 1

            - type: "rpm"
              name: "Fuel"
              uri: "http://mirror.fuel-infra.org/fwm/6.1/centos/os/x86_64/"
              priority: 2

We also SHOULD implement two new tasks:

* ``check_connectivity`` - the task will check whether repos reachable or not
* ``build_images`` - the task will generate the provisioning images

UX impact
---------

* When users create a cluster using Fuel UI they will be asked for specifying
  both Ubuntu and OpenStack repos. The inputs SHOULD be pre populated with
  default values so user may skip this step and go on.

* When it's done and the cluster is created, a task for building provisioning
  images will be sent to Astute.

* Users are unable to start cluster deploying until provisioning images are
  built successful.

  .. note:: It'd be nice to have rough ETA here if it's easy to implement.

* If users use preseed installation way they are not required to build
  provisioning images and therefore they can run deploying at any time.

* Users are required to have Internet connection on Master Node. If they
  want to have offline mode, they need to create local mirrors and
  specify them in cluster creation wizard.

* When the cluster is created, a task for checking connectivity will be
  sent to Astute. If provided repos are reachable from the master node -
  it reports success and cluster became ready for deployment. Otherwise -
  the banner will be shown on Fuel UI that there's no connectivity to
  repos.


RPC impact
----------

The new tasks SHOULD be executed by Astute, and they SHOULD be declarative.
Here's the example of the RPC message for both tasks:

.. code:: json

    {
        "api_version": "1",
        "method": "execute_tasks",
        "respond_to": "_respond_to_",
        "args": {
            "task_uuid": "_task_uuid4_",
            "tasks": [
                {
                    "id": "_command_id_",
                    "uids": ["master"],
                    "type": "shell",
                    "parameters": {
                        "cmd": "_command_to_execute_",
                        "timeout": 180
                    }
                }
            ]
        }
    }

.. note:: The ``_command_to_execute_`` will be executed inside mcollective
          container, so the container should be ready to do this and must
          pre install all required stuff.

Since both tasks will send an RPC call we have to implement two methods
in Nailgun's receiver if we want to get their results. Here's they are:

* ``build_images_resp``
* ``check_connectivity_resp``

and in order to receive its result the ``build_images_resp`` SHOULD
be implemented in Nailgun's receiver daemon.

REST API impact
---------------

None.

Upgrade impact
--------------

* Since we have a "Data model impact" we HAVE TO prepare an Alembic
  migration that SHOULD update existing releases and clusters to
  fit the new format.

* Both old clusters and old releases WILL continue use packages from
  the master node. They WON'T use on-line repos.

* The ``fuel_upgrade`` script SHOULD do not try to install repos
  for Ubuntu release.

Plugins impact
--------------

Since we're going to introduce priorities for repos, the priority of
plugins' repos SHOULD be higher than priority of Ubuntu/Fuel repos.
Why? Because plugin developer MAY want to override some package
from the core distro.

Security impact
---------------

* Cloud security will be improved, since cloud will get all latest security
  updates directly from upstream.

* Cloud security will be decreased, since cloud will have access to Internet.

Notifications impact
--------------------

A notification SHOULD be sent when provisioning images were built.

Other end user impact
---------------------

None.

Performance Impact
------------------

Ubuntu deployment time MAY be increased due to the fact that the packages
will be retrieved directly from the third-party servers. But when the
packages get cached the time should be the same.

.. hint:: The word "MAY" is used because modern DCs may have network
          connection faster than HDD.

Other deployer impact
---------------------

None

Developer impact
----------------

* Developers won't be able to build ISO with custom packages anymore.
  Instead, they SHOULD use a regular ISO and specify custom repo
  with higher priority in cluster creation wizard.

Fuel infra impact
-----------------

#. Fuel DevOps team HAVE TO prepare a local Ubuntu mirror.

   * We SHOULD use the local mirror in tests in order to speed up their
     passing.

   * The local mirror SHOULD NOT change in time, since it may lead to
     accidental deployment fails. All new Ubuntu's replicas SHOULD BE saved
     as separate mirrors. In other words, we SHOULD NOT update mirror in
     place. Instead, each sync with upstream SHOULD create a new replica.

   * All replicas SHOULD live at least a week in order to get debug
     easy.

   * The latest mirror replica SHOULD be available in Fuel CI through
     environment variable.

#. Fuel QA team HAVE TO pass mirrors to cluster in system tests.

   * The system tests SHOULD retrieve a link to the latest Ubuntu replica
     from the environment variable and use that mirror in cluster creation
     API call.

   * The system tests SHOULD also pass a link to OpenStack mirror (Fuel)
     in cluster creation API call. It SHOULD be retrieved from Jenkins
     job, since different Fuel releases have different mirrors.

#. Fuel DevOps team SHOULD reflect changes in Jenkins.

   * There will be no packages for Ubuntu on the Fuel ISO, so "Custom ISO" job
     SHOULD NOT receive extra DEB repos. If someone just wants to test custom
     DEB packages, he (she) SHOULD just run "Custom BVT" job with extra DEB
     repos.

   * The "Custom BVT" job SHOULD be able to receive a list of extra DEB
     repos and pass them directly to system tests. The system tests SHOULD
     receive and use them in cluster creation API call.


Implementation
==============

Assignee(s)
-----------

Primary assignee:

* Igor Kalnitsky <ikalnitsky@mirantis.com>

Developers:

* Vladimir Kozhukalov <vkozhukalov@mirantis.com>
* Yulia Aranovich <jkirnosova@mirantis.com>

Mandatory Design Reviewers:

* Sergii Golovatiuk <sgolovatiuk@mirantis.com>
* Tomasz Napierala <tnapierala@mirantis.com>

QA:

* Denis Dmitriev <ddmitriev@mirantis.com>
* Dmytro Tyzhnenko <dtyzhnenko@mirantis.com>

DevOps:

* (to be decided)


Work Items
----------

* Provide possibility to specify custom Ubuntu and OpenStack repos with
  custom priorities.

* Add controls for specifying custom repos on Fuel UI.

* Add options for specifying custom repos in python-fuelclient.

* Implement the ``check_connectivity`` task.

* Implement the ``build_images`` task.


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

* The slaves MUST use repos which are specified in cluster's attributes.

* The slaves MUST use priority pinning that are specified in cluster's
  attributes.


Documentation Impact
====================

The documentation SHOULD cover how the end user workflow has been changed
for deploying clusters on Ubuntu.


References
==========

* #fuel-dev on freenode
