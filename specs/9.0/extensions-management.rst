..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=============================
Nailgun extensions management
=============================

https://blueprints.launchpad.net/fuel/+spec/extensions-management


--------------------
Problem description
--------------------

Nailgun has a possibility to extend its behaviour thanks to extensions system.
However we do not have any way which would allow End User to manage the
extensions for specific cluster or release.

----------------
Proposed changes
----------------

The extensions management should have the following features:

* Extensions can be enabled from Fuel CLI for specific cluster or release.

* Additional API handlers to deal with extensions. More details in `REST API`_
  section.


Web UI
======

None


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

* Fuel Developer is able to see the list and details of all available
  extensions:

  :code:`fuel extensions`

* Fuel Developer is able to see the list and details of all enabled extensions
  for specific cluster/release

  :code:`fuel env --env 1 --extensions`

  :code:`fuel release --rel 1 --extensions`

* Fuel Developer is able to enable/disable extensions for specific
  cluster/release

  :code:`fuel env --env 1 --extensions extension1 extension2 ...`

  :code:`fuel release --rel 1 --extensions extension1 extension2 ...`


Plugins
=======

None


Fuel Library
============

None

------------
Alternatives
------------

None

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

None


---------------
End user impact
---------------

End User will have the ability to manage the available extensions.

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

None

---------------------
Infrastructure impact
---------------------

None


--------------------
Documentation impact
--------------------

* new API endpoints should be described

* new Fuel CLI commands should be described


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
  * Igor Kalnitsky <igor@kalnitsky.org>


Work Items
==========


* Nailgun API changes for clusters and releases.

* Possibility to change extensions in cluster/releases from Fuel CLI


Dependencies
============

The change depends on [#stevedore_extensions_discovery]_

------------
Testing, QA
------------

Acceptance criteria
===================

* End User should be able to manage available extensions and enable/disable
  them for specific cluster or release.


----------
References
----------

.. [#stevedore_extensions_discovery] https://blueprints.launchpad.net/
    fuel/+spec/stevedore-extensions-discovery
