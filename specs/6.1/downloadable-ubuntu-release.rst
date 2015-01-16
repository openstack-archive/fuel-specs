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

As a cloud deployment engineer, I want to provide an Ubuntu ISO and
Ubuntu repositories when I deploy OpenStack.


Proposed change
===============

* Remove vanilla Ubuntu packages from the ISO.

  All vanilla Ubuntu packages MUST be removed from the ISO. All those
  packages that are required for OpenStack installation could be kept
  on the ISO.

* Mark Ubuntu as unavailable release.

  All attempts to create environment based on Ubuntu release SHOULD warn
  user that he's trying to create undeployable environment. User should
  be able to skip this warning and continue environment creation.

  All attempts to start provisioning/deployment MUST fail for unavailable
  releases.

  See "Other end user impact" for details.

* Provide an API call for uploading official Ubuntu ISO.

  The provided API call SHOULD be used by both Fuel UI and Fuel CLI in order
  to upload Ubuntu ISO and make Ubuntu release available for deployment.

  See "REST API impact" section for details.

* Provide state mechanism for release model.

  In order to distinguish releases which are ready for deployment and which
  are not, a set of possible states SHOULD be added.

  See "Data model impact" for details.

* Provide mechanism to execute a set of tasks in Astute.

  Astute SHOULD be able to receive a set of tasks and execute them on
  Fuel Master in the MCollective container.

  See "Astute impact" for details.


Alternatives
------------

None


Data model impact
-----------------

Release
```````

Currently, there is a ``.state`` attribute in the release model which was
introduced for similar purpose a time ago. It's unused now, so it could be
fully reworked to fit our needs.

There will be two possible states:

* ``available`` (could be deployed)
* ``processing`` (couldn't be deployed)
* ``unavailable`` (couldn't be deployed)

Initial ``.state`` should be loaded from the ``openstack.yaml``. By default,
the release model has ``.state = unavailable``.

Database migration should set ``.state = available`` for previous releases.

Also, the release model should have a field to store ISO's SHA1 checksum.

Task
````

Since we're going to have tasks that are bound to releases, the following
changes are required:

* the ``.release_id`` column should be introduced in Task model
* the ``prepare_release`` task name should be added


REST API impact
---------------

Input
`````

The Nailgun should provide a new API handler for uploading ISO. The
uploading could be performed by POST method to the following URI::

    POST /api/v1/releases/<:id>/upload/iso HTTP/1.1
    Host: host address
    Content-Type: application/octet-stream
    Content-Length: size of request's body

    raw binary data of the uploaded image

where ``<:id>`` is a release id for which the ISO will be uploaded.

Business Logic
``````````````

* On first request the handler should try to acquire release and
  set ``.state = processing``.

* The HTTP status ``405 Method Not Allowed`` should be returned for
  releases where ``.state == available``.

* The HTTP status ``409 Conflict`` should be returned for releases
  where ``.state == processing``.

* Uploaded data should be read by chunks in order to do not keep
  entire (huge) image in memory.

* Uploaded ISO should be verified by SHA1 checksum. In case of success -
  new task should be created, request for execution should be sent to
  Astute and HTTP status ``202 Accepted`` should be returned. Otherwise -
  HTTP status ``400 Bad Request`` should be returned.

* Astute should receive the task and execute a set of tasks within
  that task.

* If task were completed successfully, the release should change its
  state from ``processing`` to ``available``. Otherwise - it should
  change its state to ``unavailable``.


Astute impact
-------------

Astute MUST be able the handle the following RPC call::

    {
        "api_version": "...",
        "method": "execute_tasks",
        "respond_to": "execute_tasks_resp",
        "args": {
            "task_uuid": "_task_uuid4_",
            "tasks": [
                {
                    "id": "extract_repo",
                    "uids": ["master"],
                    "type": "shell",
                    "parameters": {
                        "cmd": "_command_for_repo_extracting_",
                        "timeout": 180
                    }
                },
                {
                    "id": "build_images",
                    "uids": ["master"],
                    "type": "shell",
                    "parameters": {
                        "cmd": "_command_for_image_building_",
                        "timeout": 180
                    }
                }
            ]
        }
    }

So the following things have to be implemented:

* the ``execute_tasks`` method should be added
* the method should extract and execute tasks from ``args["tasks"]``
* the method should execute tasks on fuel master in case there's
  a ``master`` in task's ``uids`` array
* the progress should be reported back to ``execute_tasks_resp`` method


Upgrade impact
--------------

There's no upgrade impact. Old releases are kept "As Is", while the new
one will follow workflow defined in this spec (just like after fresh
master node installation).

Security impact
---------------

None

Notifications impact
--------------------

When Ubuntu ISO became available the notification should be sent.

Other end user impact
---------------------

Before deploying OpenStack cluster on Ubuntu, end users should manually
download official Ubuntu ISO and upload it using either Fuel UI or Fuel CLI.

The workflow would look like::

    User                    Ubuntu.com    Fuel
     +                          +           +
     |       download iso       |           |
     | +----------------------> |           |
     |           done           |           |
     | <----------------------+ |           |
     |                          |           |
     |                          |           |
     |        upload iso        |           |
     | +----------------------------------> |
     |           done           |           |
     | <----------------------------------+ |
     |                          |           |
     |                          |           |
     |     check task status    |           |
     | +----------------------------------> |
     |           done           |           |
     | <----------------------------------+ |
     |                          |           |
     |                          |           |
     |        deploy env        |           |
     | +----------------------------------> |
     |           done           |           |
     | <----------------------------------+ |
     |                          |           |
     +                          +           +

Fuel UI requires the following changes:

* The *status* column on the *Releases* tab should be an "Upload ISO"
  button for all unavailable releases.

* The "Upload ISO" button has to raise the modal dialog. The dialog
  should:

  - Show instructions where to download official ISO.
  - Provide control elements for choosing and uploading ISO.

  If uploading was successful, the dialog should disappear and the *status*
  column should show the preparation task progress.

  If uploading was failed, the dialog should show the error and provide
  a way to upload it again.

* There should be a way to stop ISO uploading.

* Users are able to create environments using *unavailable* releases.
  Though some changes are necessary:

  - The wizard should have a warning message that additional steps
    are required in order to make a cluster deployable.
  - The warning message should contain a link to releases tab.
  - The next button should be disabled until user checked a checkbox
    that he understands this and wants to create environment anyway.

  The cluster page should show a warning message for those clusters
  that are created for unavailable releases.


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

UI:

* Yulia Aranovich <jkirnosova@mirantis.com>

QA:

* Denis Dmitriev <ddmitriev@mirantis.com>
* Dmytro Tyzhnenko <dtyzhnenko@mirantis.com>
* Yegor Kotko <ykotko@mirantis.com>

DevOps:

* Igor Shishkin <ishishkin@mirantis.com>

Work Items
----------

* Change release's ``.state`` attribute to cover our case
  (see Data model impact for details).

* Implement Nailgun handler for uploading ISO.

* Implement Astute handler for extracting repos and building images for IBP.

* Implement Fuel Web UI for uploading ISO.

* Implement support in Fuel CLI.

* Try to improve file uploading by Nginx.


Dependencies
============

The blueprint implicitly depends on the following ones:

* `Ubuntu 14.04 support
  <https://blueprints.launchpad.net/fuel/+spec/support-ubuntu-trusty>`_

* `Separate MOS from Linux repos
  <https://blueprints.launchpad.net/fuel/+spec/separate-mos-from-linux>`_


Testing
=======

* The repo is successfully extracted from the uploaded ISO.
* The release became available when the task gets done successfully.
* The repo is used during ubuntu deployment.
* The ubuntu is deployed successfully.


Documentation Impact
====================

The documentation should have a section that covers how to enable
Ubuntu release for deployment.


References
==========

* #fuel-dev on freenode
