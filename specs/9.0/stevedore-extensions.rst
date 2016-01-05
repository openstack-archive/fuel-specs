..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

============================================
Implement nailgun extensions using stevedore
============================================

https://blueprints.launchpad.net/fuel/+spec/stevedore-extensions


--------------------
Problem description
--------------------

Nailgun has a possibility to extend its behaviour thanks to extensions system.
There are methods called on events like node create, node update, cluster
delete etc. which can be used to inject some logic. The problem is
that currently all extensions must be placed inside `extensions` module in
Nailgun's source code. Also in order to make extension visible for Fuel, it
must be imported and explicitly added to global `extensions` list.

It means that there is no elegant way for User to use extensions system
capabilities.


----------------
Proposed changes
----------------

The extensions system must be refactored to meet the following conditions:

* It must be pluggable - User is able to write an extension, place it in
  separate package and add it to available extensions list just by running
  :code:`pip install <extension-name>`

* It must implement auto-discovery of extensions.

* Extension has `description` field which briefly describes its features.

* Extensions can be enabled from Fuel CLI for specific cluster or release and
  because of that we also need:

* Additional API handlers to deal with extensions. More details in `REST API`_
  section.

The best solution here is to use stevedore - a manager for dynamic plugins in
Python.

Stevedore uses namespaces to load the extensions so the proposed
namespace for nailgun extensions is `nailgun.extensions`.


Web UI
======

Web UI must be prepared to consume new API handlers for enabling/disabling
extensions for specific release/cluster.


Nailgun
=======

Data model
----------

None


REST API
--------


.. http:get:: /extensions/

  Returns list of all available extensions

  **Response format:**

  .. sourcecode:: http

    [
        {
          "name": "extension1",
          "version": "1.0.0",
          "description": "Lorem ipsum dolor sit amet"
        },
        {
          "name": "extension2",
          "version": "2.1.0",
          "description": "Lorem ipsum dolor sit amet"
        },
        ...
    ]

  :statuscode 200: Returns list of extensions or empty list


.. http:get:: /clusters/(cluster_id)/extensions

  Returns list of all enabled extensions in cluster with id `cluster_id`

  **Response format:**

  .. sourcecode:: http

    [
        "extension1",
        "extension2",
        "extension3",
        ...
    ]

  :statuscode 200: Returns list of extensions or empty list
  :statuscode 404: No such cluster


.. http:put:: /clusters/(cluster_id)/extensions

  Enable/disable extensions

  **Example request**:

  .. sourcecode:: http

    [
        "extension1",
        "extension2",
        "extension3",
        ...
    ]

  :statuscode 200: extensions has been enabled for release
  :statuscode 400: there is no such extension available
  :statuscode 404: No such cluster



.. http:get:: /releases/(release_id)/extensions

  Returns list of all enabled extensions in release with id `release_id`

  **Response format:**

  .. sourcecode:: http

    [
        "extension1",
        "extension2",
        "extension3",
        ...
    ]

  :statuscode 200: Returns list of extensions or empty list
  :statuscode 404: No such release


.. http:put:: /releases/(release_id)/extensions

  Enable/disable extensions

  **Example request**:

  .. sourcecode:: http

    [
        "extension1",
        "extension2",
        "extension3",
        ...
    ]

  :statuscode 200: extensions has been enabled for release
  :statuscode 400: there is no such extension available
  :statuscode 404: No such release


Orchestration
=============


RPC Protocol
------------

None


Fuel Client
===========

* End User is able to see the list and details of all available
  extensions:

  :code:`fuel extensions`

* End User is able enable/disable extensions for specific cluster/release

  :code:`fuel --env 1 env set --extensions extension1 extension2 ...`

  :code:`fuel --rel 1 release set --extensions extension1 extension2 ...`


Plugins
=======

None


Fuel Library
============

None

------------
Alternatives
------------

* We could write our own plugin system instead of using Stevedore. But:

  * In most cases it is not good to reinvent the wheel. It also applies for
    this one, since current extensions system doesn't need a lot of work to
    port it to Stevedore.

* We could use some other plugin system like `baseplugin` [#baseplugin]_. But:

  * As an OpenStack project we should reuse other OpenStack projects

  * Stevedore is already in global requirements.


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

* Notification when extension is enabled/disabled for cluster/release.


---------------
End user impact
---------------

User is able to extend Nailgun features by writing own extension which uses
Nailgun's extensions base class and namespace which is `nailgun.extensions`.

It will be placed in separate package and the installation is simple as
:code:`pip install <extension_name>`. Nailgun will detect new extension
automatically.


------------------
Performance impact
------------------

None


-----------------
Deployment impact
-----------------

The change is nailgun specific, so there's no Deployment impact.


----------------
Developer impact
----------------

All new extensions should be placed in separate packages. The `extensions`
module in nailgun should be not extended anymore.


---------------------
Infrastructure impact
---------------------

None


--------------------
Documentation impact
--------------------

Extensions mechanism should be described:

* How to write extension:

  * Where is the base class for extension

  * What is the minimal working extension (required properties etc.)

* What are the possibilities

* Nailgun namespace which is `nailgun.extensions`

* Example of simple extension with `logging` which logs appropriate message
  on every event like `on_node_create`, `on_node_update` etc.


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee: Sylwester Brzeczkowski <sbrzeczkowski@mirantis.com>

Other contributors:

  * Evgeny Li <eli@mirantis.com>

Mandatory design review:

  * Evgeny Li <eli@mirantis.com>


Work Items
==========

* Setup Nailgun with Stevedore. Add possibility to install extensions in
  separate packages

* Nailgun API changes for clusters and releases.

* Possibility to change extensions in cluster/releases from WebUI

* Possibility to change extensions in cluster/releases from Fuel CLI



Dependencies
============

* Fuel integration with Bareon service [#bp_bareon_integration]_.

* Stevedore module [#stevedore_docs]_.


------------
Testing, QA
------------


* Install extension from separate package and check if it's available
  in Nailgun

* Check if after enabling/disabling extensions the notification appear.


Acceptance criteria
===================

* After extension installation from separate python package it should be
  available in Nailgun

* After enabling/disabling extension in release/cluster the notification
  should appear in the database


----------
References
----------

.. [#baseplugin] http://pluginbase.pocoo.org/
.. [#bp_bareon_integration] https://blueprints.launchpad.net/fuel/+spec/fuel-bareon-api-integration
.. [#stevedore_docs] http://docs.openstack.org/developer/stevedore/index.html
