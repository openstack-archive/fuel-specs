..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

========================================
Nailgun API to download serialized facts
========================================

https://blueprints.launchpad.net/fuel/+spec/serialized-facts-nailgun-api

API for downloading serilized deployment facts. It shall be used for
the following scenarios:

* create data resources in Solar
* access facts directly from Puppet agent via Hiera HTTP backend
* access facts from 3rd party applications

This spec is focused on the second use case.

--------------------
Problem description
--------------------

Currently, the serialized facts are upload to target nodes as an
``astute.yaml`` file, and Puppet agents access it via Hiera's standard
``yaml`` backend.

This makes it difficult to update the facts on the node. It also
doesn't allow for keeping track of changed settings. Revert to the
original facts is also not possible.

----------------
Proposed changes
----------------

The proposed change will allow the new way to access the already
existing serialization functionality. New API handle shall respond
to GET requests with the result of serialization of deployment
facts from Fuel settings. The context of the serialization shall
be provided with the parameter in GET request.

Web UI
======

No changes to UI are proposed in this spec.

Nailgun
=======

New API call and corresponding handlers shall be introduced to
provide access to results of serialization of deployment facts
for a node.

Data model
----------

No changes to data model.

REST API
--------

* Download serialized deployment facts for a node by ID.

* Method type: GET

* Normal HTTP response code(s): 200 OK

* Expected error HTTP response code(s):

  * 404 Not Found
    Cannot found a node with the given ID.

* ``/api/v1/node/<:id>/facts``

* Parameters which can be passed via the URL

  * ``id`` is an ID of node being queried

* JSON schema definition for the body data if allowed

* JSON schema definition for the response data if any

Orchestration
=============

General changes to the logic of orchestration should be described in details
in this section.

RPC Protocol
------------

No specific changes to orchestration or RPC protocol are proposed
by this particular specification. However, in future it might allow to
exclude serialized deployment facts data from the RPC exchange between
Astute and Nailgun.

Fuel Client
===========

Fuel client should be augumented with the support for the described
API calls. This command should yield a serialized facts data in selected
format (``json`` or ``yaml``) to the ``stdout`` stream.

CLI Parameters
^^^^^^^^^^^^^^

* ``--node-id <INT>`` is the ID of node being queried. Mandatory parameter.

* ``--format [json|yaml]`` defines a format of output. Default is ``json``.

Plugins
=======

Plugins data shall be included in the serialization. No specific changes
to the plugin framework shall be made.

Fuel Library
============

None.

------------
Alternatives
------------

What are other ways of achieving the same results? Why aren't they followed?
This doesn't have to be a full literature review, but it should demonstrate
that thought has been put into why the proposed solution is an appropriate one.

The alternative approach would be to create a dedicated service to facilitate
the exchange of the serialized data between different components of the Fuel
installer (i.e. `ConfigDB`_). However, this requires significant changes to
the architecture of the system. This path shall be pursued in the following
major releases of Fuel software. 

--------------
Upgrade impact
--------------

With the upgrade of the Fuel Admin node, the serialized facts data will be
reset. No tracking of changes in facts shall be available between upgrades.

---------------
Security impact
---------------

The serialized deployment facts contain sensitive data such as access
credentials to different components in the system.

The access to the endpoint must follow the same conventions as other
API endpoints in Nailgun. The endpoint must support Keystone-based
authentication and Basic HTTP Auth. The endpoint must provide SSL
connection.

--------------------
Notifications impact
--------------------

None.

---------------
End user impact
---------------

None.

------------------
Performance impact
------------------

None.

-----------------
Deployment impact
-----------------

None.

----------------
Developer impact
----------------

None.

---------------------
Infrastructure impact
---------------------

None.

--------------------
Documentation impact
--------------------

None.

--------------
Implementation
--------------

Assignee(s)
===========

Who is leading the writing of the code? Or is this a blueprint where you're
throwing it out there to see who picks it up?

If more than one person is working on the implementation, please designate the
primary author and contact.

Primary assignee:
  <gelbuhos> Oleg S. Gelbukh

Other contributors:
  <sabramov> Sergey Abramov
  <sryabin>  Sergey Ryabin

Mandatory design review:
  <sbrimhall> Scott Brimhall
  <ikalnitsky> Igor Kalnitskiy


Work Items
==========

* Implement an API handler and supplementary logic in Nailgun source code
  tree.
* Update documentation to reflect changes in the Nailgun API.

Dependencies
============

None.

------------
Testing, QA
------------

TBD

Acceptance criteria
===================

* API handler responds with the serialized deployment facts according to
  the specification.

----------
References
----------

.. ConfigDB: https://review.openstack.org/#/c/281331/
.. Hiera HTTP backend: https://github.com/crayfishx/hiera-http/blob/master/README.md
.. Hiera HTTP lookup: https://github.com/crayfishx/lookup_http
