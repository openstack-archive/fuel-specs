..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=========================================
Unify the input data
=========================================

https://blueprints.launchpad.net/packetary/+spec/unify-input-data

We need to unify the Packetary input data format for the command that copies a
repository.

--------------------
Problem description
--------------------

Both Nailgun and Fuel-mirror use the same single format to describe parameters
of the repository. Unlike these, Packetary uses a plain text string, which is
inconvenient. We need to unify the data format for all commands and operations.

----------------
Proposed changes
----------------

We propose to use in Packetary the same data format used in Nailgun and
Fuel-mirror. The proposed data format is the following:

1. Repositories input data format:

  * name field - A single word identifying the repository name

  * uri field - Uniform Resource Identifier for repository root. Describe in
    rfc3986

  * type field - single word. It can be "rpm" or "deb", depending to the
    packages format which used in the repository

  * suite field - Describe repositories types ($release, $release-security,
    $release-updates, $release-backports). This is applicable only for DEB
    repositories.

  * section field - a list of areas separated by a whitespace. This is
    applicable only for DEB repositories.

  * path field - This field can be absolute or relative path pointing to
    directory where repository is copied.

  * priority field - Integer field that allows changing the behaviour of
    selecting a package. In general, the format depends on the repository
    driver. For example: DEB repository expects general values from 0 to 1000. 0
    to have lowest priority and 1000 -- the highest. Note that a priority above
    1000 will allow even downgrades no matter the version of the prioritary
    package. RPM repository expects values in the range of 1 to 99 inclusive.
    A priority of 1 is the highest setting, and 99 is the lowest. If this field
    is not specified, the driver will setup the default priority is the lowest
    priority(0 for DEB and 99 for RPM)

Required fields are: name, uri, type.

As an example for RPM repositories, the input data format will have the
following yaml format:

.. code-block:: yaml

  repos:
    -   name: "centos"
        uri: "http://mirror.centos.org/centos/6/os/x86_64"
        type: "rpm"
        path: "/root/repo"
        priority: 1

    -   name: "centos-updates"
        uri: "http://mirror.centos.org/centos/6/updates/x86_64"
        type: "rpm"
        path: "/root/repo"
        priority: 99

And for DEB repositories:

.. code-block:: yaml

  repos:
    -   name: "ubuntu"
        uri: "http://localhost/ubuntu/updates"
        suite: "trusty"
        section: "main multiverse restricted universe"
        type: "deb"
        path: "/root/repo"
        priority: 1000

    -   name: "ubuntu-updates"
        uri: "http://localhost/ubuntu/updates"
        suite: "trusty-updates"
        section: "main multiverse restricted universe"
        type: "deb"
        path: "/root/repo"
        priority: 500

If the section filed is not specified, we have flat repository format [1]_ and
the input data for DEB repositories will be as follows:

.. code-block:: yaml

  repos:
    -   name: "ubuntu"
        uri: "http://localhost/ubuntu"
        type: "deb"
        suite: "/some/path"
        path: "/root/repo"

2. To use the following fields for the packages input data format:

  * name field - A single word identifying the package name

  * versions field - An optional parameter that specifies versions of the
    package. It is usually a sequence of integers separated by a dot. Before it
    can be a relational operator (eq, gt, lt, ge, le). When specifying two or
    more versions in the package, it is necessary to use logic AND operator
    between versions. This means that the engine will select the package that
    satisfies all the specified versions.

For example:

.. code-block:: yaml

   packages:
    -   name: openssl
        versions:
        - ">= 1.0.1"
        - "< 1.0.2e-1ubuntu1"

3. Removes dependencies logic between the repositories and adds priority to the
   repositories.


4. Packages search in the repositories according to the building repositories
   list order. The list is built according to the sorting algorithm that is
   individual for each repositories driver.

Web UI
======

None

Nailgun
=======

None

Data model
----------

None

REST API
--------

None

Orchestration
=============

None

RPC Protocol
------------

None

Fuel Client
===========

None

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

Improved user-experience due to the unified format.

------------------
Performance impact
------------------

None

-----------------
Deployment impact
-----------------

None

----------------
Developer impact
----------------

Removing packages dependencies will cause changes in the API. Developers must be
updated on the changes.


---------------------
Infrastructure impact
---------------------

None

--------------------
Documentation impact
--------------------

None

--------------
Implementation
--------------

Assignee(s)
===========

None

Work Items
==========

* Add input data validation scheme

* Implement repositories sorting in Packetary drivers

* Implement search by priority

------------
Testing, QA
------------

None

Acceptance criteria
===================

The tests described above need to be passed.

----------
References
----------

.. [1] https://wiki.debian.org/RepositoryFormat#Flat_Repository_Format
