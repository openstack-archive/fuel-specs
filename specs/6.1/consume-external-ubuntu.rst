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

   Once users have created an environment on Ubuntu, they SHOULD be able to
   provide both Ubuntu and OpenStack repos as well as additional repos on
   the "Settings" tab. By default, Canonical repo for Ubuntu and Fuel repo
   for OpenStack SHOULD be used.

   The repos SHOULD be specified using Debian format:

   .. code::

       deb http://archive.ubuntu.com/ubuntu/ trusty main universe
       deb-src http://pl.archive.ubuntu.com/ubuntu/ trusty main multiverse

   All Ubuntu packages SHOULD be removed from the Fuel ISO and provided
   mirrors SHOULD be used for environment deployment.

   .. note:: It'd be great to have format validation for provided repos
             on both backend and UI.

   .. note:: We SHOULD NOT use ``mirror://`` protocol for default repos,
             because we won't know which repos were used and hence
             debugging will be painful.

   See "Data model impact", "UX impact" and "Developer impact" for details.

#. **OPTIONAL**: Check that provided repos contain all required packages.

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
             container HAVE TO be ready for doing this.

#. Generate provisioning images per cluster.

   Since we're going to specify mirrors per cluster, different clusters may
   have different set of mirrors. Therefore, we SHOULD generate provisioning
   images per cluster.

   Provisioning images SHOULD be generated once users start deployment.
   The task for generating images HAVE TO be started before others deployment
   tasks. If users don't use image-based provisioning, the task SHOULD NOT
   be sent to Astute.

   Provisioning images SHOULD NOT be regenerated if they are already exists.

   .. note:: Consider to reuse existing images if there are ones with
             suitable packages.

   See "Data model impact" and "RPC impact" for details.

#. Check that there is connectivity to provided repos.

   We SHOULD check whether repos are reachable or not, and in case it's not
   we HAVE TO warn user about it. The check SHOULD be implemented as
   asynchronous task and SHOULD be performed in two cases:

   * once the environment is created (check defaults)
   * on demand on "Settings" tab (check custom repos)

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
        repo_setup:
          metadata:
            label: "Repos Configuration"
            weight: 123
          repos:
            type: "custom_repo_configuration"
            value:
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
        repo_setup:
          metadata:
            label: "Repos Configuration"
            weight: 123
          repos:
            type: "custom_repo_configuration"
            value:
              - type: "rpm"
                name: "OS"
                uri: "http://mirror.centos.org/centos-6/6/os/x86_64/"
                priority: 1

              - type: "rpm"
                name: "Fuel"
                uri: "http://mirror.fuel-infra.org/fwm/6.1/centos/os/x86_64/"
                priority: 2

We also SHOULD implement the ``check_connectivity`` task.


UX impact
---------

* Once users have created an environment on Ubuntu, they SHOULD be able to
  provide both Ubuntu and OpenStack repos as well as additional repos on
  the "Settings" tab. By default, UI controls SHOULD be pre populated
  with defaults.

  .. note:: Users SHOULD NOT be able to provide custom repos for CentOS
            environemnts.

  Additional repos (extra repos) SHOULD be added on demand by pressing
  some button (for example, "+"/ "add more").

  There SHOULD BE no way to set repos priorities via Fuel UI. Let's
  keep this functionality for RESTful API and python-fueclient. If
  user change some repo on UI the priority SHOULD NOT be changed.

  .. note:: For both Ubuntu and Fuel repos the priorities SHOULD be
            kept as they specified in ``openstack.yaml``. For each
            extra repo the priority SHOULD be the same and SHOULD
            be retrieved from ``settings.yaml``.

* Once an Ubuntu environment is created a ``check_connectivity`` task
  SHOULD be sent to Astute. If provided repos are reachable from the
  master node - it reports success and the environment becomes ready for
  deployment. Otherwise - a banner SHOULD be shown on Fuel UI that
  there's no connectivity to repos and deployment SHOULD NOT be allowed.
  The request for starting a ``check_connectivity`` task SHOULD be
  performed by Fuel UI. The API call for creating cluster SHOULD NOT
  do it implicitly for us.

  .. note:: The task SHOULD NOT be used for Cent OS environments.

* If the ``check_connectivity`` task was failed and deployment isn't allowed,
  the user SHOULD be able either provide custom (reachable) repos or fix
  connectivity issues, and restart the check through the "Settings" tab.

  .. note:: The task SHOULD NOT be restarted automatically by saving
            settings. It SHOULD be restarted on demand by pressing
            a special button on UI.

* If the check is passed the environment SHOULD become ready for deployment.

* Once an environment is deployed users SHOULD NOT be able to change repos.


RPC impact
----------

The ``check_connectivity`` task SHOULD be executed by Astute, and its
SHOULD be declarative. Here's the example of the RPC message:

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
          container, so the container MUST be ready to do this and MUST
          pre install all required stuff.

Since the task is executed via RPC, the Nailgun's receiver SHOULD implement
some ``check_connectivity_resp`` method in order to handle task's result.

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

Fuel DevOps impact
------------------

#. Fuel DevOps team HAVE TO prepare a local Ubuntu mirror.

   * We SHOULD use the local mirror in tests in order to speed up their
     passing.

   * The local mirror SHOULD NOT change in time, since it may lead to
     accidental deployment fails. All new Ubuntu's mirrors SHOULD BE saved
     as separate mirrors. In other words, we SHOULD NOT update mirror in
     place. Instead, each sync with upstream SHOULD create a new version
     of the mirror.

     .. note:: Consider to re-use scripts from IT guys.

   * All mirror's versions SHOULD live at least a week in order to get debug
     easy.

   * The latest mirror version SHOULD be available in Fuel CI through
     environment variable.

#. Fuel DevOps team HAVE TO reflect changes in Jenkins.

   * There will be no packages for Ubuntu on the Fuel ISO, so "Custom ISO" job
     SHOULD NOT receive extra DEB repos. If someone just wants to test custom
     DEB packages, he (she) SHOULD just run "Custom BVT" job with extra DEB
     repos.

   * The "Custom BVT" job SHOULD be able to receive a list of extra DEB
     repos and pass them directly to system tests. The system tests SHOULD
     receive and use them in cluster creation API call.

Fuel QA impact
--------------

#. Fuel QA team HAVE TO pass mirrors to cluster in system tests.

   * The system tests SHOULD retrieve a link to the latest Ubuntu replica
     from the environment variable and use that mirror in cluster creation
     API call.

   * The system tests HAVE TO also pass a link to OpenStack mirror (Fuel)
     in cluster creation API call. It SHOULD be retrieved from Jenkins
     job, since different Fuel releases have different mirrors.


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

* Pawel Brzozowski <pbrzozowski@mirantis.com>
* Mateusz Matuszkowiak <mmatuszkowiak@mirantis.com>


Work Items
----------

* Provide possibility to specify custom Ubuntu and OpenStack repos with
  custom priorities.

* Add controls for specifying custom repos on Fuel UI.

* Add options for specifying custom repos in python-fuelclient.

* Implement the ``check_connectivity`` task.


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
