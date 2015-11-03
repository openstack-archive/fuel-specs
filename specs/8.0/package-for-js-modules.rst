..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Package for nodejs modules for nailgun
==========================================

https://blueprints.launchpad.net/fuel/+spec/package-for-js-modules


--------------------
Problem description
--------------------

For building nailgun package we made about 50 packages with js libraries. But every package included about 100 js libraries. For latest update nailgun we should rebuild more 20 packages with new js modules. This workflow is very long.


----------------
Proposed changes
----------------

Need to prepare 1 package with all JS libraries. All js libraries will be automatically downloading when building nailgun package. For update all js libraries maintainer should update version of new package in spec file

Web UI
======

None


Nailgun
=======

TODO

Data model
----------
None

REST API
--------

Each API method which is either added or changed should have the following

* Specification for the method

  * A description of what the method does suitable for use in
    user documentation

  * Method type (POST/PUT/GET/DELETE)

  * Normal HTTP response code(s)

  * Expected error HTTP response code(s)

    * A description for each possible error code should be included
      describing semantic errors which can cause it such as
      inconsistent parameters supplied to the method, or when an
      instance is not in an appropriate state for the request to
      succeed. Errors caused by syntactic problems covered by the JSON
      schema definition do not need to be included.

  * URL for the resource

  * Parameters which can be passed via the URL

  * JSON schema definition for the body data if allowed

  * JSON schema definition for the response data if any

* Example use case including typical API samples for both data supplied
  by the caller and the response

* Discuss any policy changes, and discuss what things a deploy engineer needs
  to think about when defining their policy.


Orchestration
=============

General changes to the logic of orchestration should be described in details
in this section.


RPC Protocol
------------

RPC protocol is another crucial part of inter-component communication in Fuel.
Thus it's very important to describe in details at least the following:

* How messaging between Nailgun and Astute will be changed in order to
  implement this specification.

* What input data is required and what format of results should be expected

* If changes assume performing operations of nodes, a description of messaging
  protocol, input and output data should be also described.


Fuel Client
===========

Fuel Client is a tiny but important part of the ecosystem. The most important
is that it is used by other people as a CLI tool and as a library.

This section should describe whether there are any changes to:

* HTTP client and library

* CLI parser, commands and renderer

* Environment

It's important to describe the above-mentioned in details so it can be fit
into both user's and developer's manuals.


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

None

------------------
Performance impact
------------------

None


-----------------
Deployment impact
-----------------

Mone


----------------
Developer impact
----------------

Todo

---------------------
Infrastructure impact
---------------------

Explain what changes in project infrastructure will be required to support the
proposed change. Consider the following:

* Will it increase the load on CI infrastructure by making build or test jobs
  consume more CPU, network, or storage capacity? Will it increase the number
  of scheduled jobs?

* Will it require new workflows or changes in existing workflows implemented in
  CI, packaging, source code management, code review, or software artifact
  publishing tools?

  * Will it require new or upgraded tools or services to be deployed on project
    infrastructure?

  * Will it require new types of Jenkins jobs?

  * Will it affect git branch management strategies?

  * Will it introduce new release artifacts?

  * Will it require changes to package dependencies: new packages, updated
    package versions?

  * Will it require changes to the structure of any package repositories?

* Will it require changes in build environments of any existing CI jobs? Would
  such changes be backwards compatible with previous Fuel releases currently
  supported by project infrastructure?


--------------------
Documentation impact
--------------------

ToDO


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  `Sergey Kulanov`_

Build-team:
  `Alexander Evseev`_


Mandatory Design Reviewers:
  - `Alexander Evseev`_
  - `Dmitry Burmistrov`_
  - `Roman Vyalov`_
  - `Vladimir Kozhukalov`_
  - `Vitaly Parakhin`_


Work Items
==========

Work items or tasks -- break the feature up into the things that need to be
done to implement it. Those parts might end up being done by different people,
but we're mostly trying to understand the timeline for implementation.


Dependencies
============




------------
Testing, QA
------------

None


Acceptance criteria
===================

Please specify clearly defined acceptance criteria for proposed changes.


----------
References
----------

.. _`Dmitry Burmistrov`: https://launchpad.net/~dburmistrov
.. _`Roman Vyalov`: https://launchpad.net/~r0mikiam
.. _`Sergey Kulanov`: https://launchpad.net/~skulanov
.. _`Vladimir Kozhukalov`: https://launchpad.net/~kozhukalov
.. _`Vitaly Parakhin`: https://launchpad.net/~vparakhin

