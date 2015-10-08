..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==============================
refactor create mirror scripts
==============================

https://blueprints.launchpad.net/fuel/+spec/refactor-local-mirror-scripts

The blueprint describes the existing problem with scripts
to manage local mirrors for repositories.

-------------------
Problem description
-------------------

The fuel-createmirror[1] was written as a bash script.
Utility is capable to create Ubuntu mirrors only.
Yum repositories are not supported currently.

----------------
Proposed changes
----------------

It is proposed to create separate library - packetary which implements
following functionality:

- Read the list of packages the repository.
- Create new repository based on the list of packages.
- Build a dependency tree for a package.
- Search for a package based on dependencies.

In order to implement the main feature of the utility – an ability to copy
only part of packages from a repository that is required to install
the openstack, a mechanism for building the dependencies tree between
the packages is needed. Since that functionality is common for all
types of repositories, it should not depend on the specific
repository or package format. To meet this requirement we need to elaborate
a separate substance “Package” that will be abstracted from
the physical format of the package and providing all the necessary
interfaces for search and resolving dependency basing on the
version and name of the package.
The dependency tree itself will be implemented based on the red-black[2] tree,
where the keys are the name and version of the package.

When searching for a package it`s needed to consider information about
obsolete and virtual packages, hence there will be three trees instead of one:
- tree of package
- tree of obsolete packages
- tree of virtual packages

During the search for a package, these trees will be following
in a certain order:
- main tree (e.g. tree of package)
- tree of obsolete packages
- tree of virtual packages

When a suitable package is found, the search stops.
If there is no suitable package -
utility only warns about unresolved relation.

It is assumed to support multiple repository formats, hence it is needed
to distinguish the code to work with specific repository formats
into the separate classes - drivers. In this case, to maintain the desired
repository format it is needed to implement an appropriate driver,
the business logic works with the data provided by the driver.
Since creating a mirror implies download packages, then a separate
layer of abstraction over the transport is required.
Due to the fact that the rsync mechanism is slower on partial mirrors;
it is proposed to support only HTTP-transport with possibility
of resuming downloads and multiple threads download
(which will make it possible to use the entire network bandwidth).

It is proposed to use the thread pool and the network connections pool
to implement that functionality. There should be a check if a package needs
to be downloaded. The check mechanism will be divided into two stages
just to make that simpler:
- Full check, that checks the checksum of packages on demand.
- Fast check, that checks file size only when copying a package.

The pool of threads allows running file checks in parallel,
and network connections pool allows controlling the number of
concurrent network connections.
The eventlet.greenpool[3] will be used as pool of threads.

Createmirror utility will depend on the packetary and python-client libraries.
The first library will be used for creation and synchronization of the mirrors,
the second one to update meta-information on the Fuel-backend.

::

    +----------------------------------------------------+
    |                 fuel-create-mirror                 |
    |                                                    |
    +-----------+--------------------------+-------------+
                |                          |
          API   |                          | API
                |                          |
    +-----------v----------+    +----------v-------------+
    |   fuel+pythonclient  |    |      packetary         |
    |                      |    |       library          |
    +-----------+----------+    +----------+-------------+
                |                          |
    +-----------v----------+    +----------v-------------+
    |      Environments    |    |   Dependency resolver  |
    |                      |    |                        |
    +-----------+----------+    +----------+-------------+
                |                          |
    +-----------v----------+    +----------v-------------+
    |     Action-Update    |    |    RepositoryManager   |
    |                      |    |                        |
    +----------------------+    +----+---------------+---+
                                     |               |
                                +----v---+      +----v---+
                                |  RPM+  |      |  DEB+  |
                                | driver |      | driver |
                                |        |      |        |
                                +--------+      +--------+


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

We can continue to use the current version of the utility but:
  - Adding support for CentOS requires the amount of the efforts that
      is comparable with recreation of the whole existing code in Python;
  - Reusing of the existing code in other projects will be difficult.

--------------
Upgrade impact
--------------

The upgrade process is used fuel_package_updates[4] utility,
that also will be re-written by using packetary.
That means the upgade process should be re-tested.

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

The end-users will get launch options:

.. code-block:: bash

    --config            Path to the configuration file
    --fuel-url          The URL of the Fuel Master node API.
    --partial           Create a partial copy of the mirror
                        (only the packages required to install OpenStack)
    --mos               Create mirror for MOS repositories.
    --base              Create mirror for System repositories.
    --centos            Create mirror with base package for CentOS
    --ubuntu            Create mirror with base package for Ubuntu

Examples:
.. code-block:: bash

    fuel-create-mirror help
    fuel-create-mirror clone --base --ubuntu --partial
    fuel-create-mirror clone --mos --centos
    fuel-create-mirror clone

The end-users will get the configuration file in yaml-format:

.. code-block:: yaml

    /etc/fuel-createmirror/config.yaml

    ...
        common:
            thread_num: 10,
            connection_count: 8,
            ignore_error_count: 2,
            http_proxy: null,
            https_proxy: null
            fuel_url: "http://localhost:8080"
            destination: "/var/www/nailgun"

        versions:
            centos_version: "6"
            ubuntu_version: "trusty"

        sources:
            -   name: "mos"
                osname: "ubuntu"
                type: "deb"
                baseurl: "http://mirror.fuel.org/ubuntu/mos-{mos_version}"
                repositories:
                     - "mos{mos_version} main restricted"
                     - "mos{mos_version}-updates main restricted"
                     - "mos{mos_version}-security main restricted"
                     - "mos{mos_version}-holdback main restricted"
                requirements:
                     - "ubuntu-standard"

            -   name: "mos"
                osname: "centos"
                type: "yum"
                baseurl: "http://mirror.centos.org/centos/mos-{mos_version}"
                repositories:
                    - "cr"
                    - "holdback"
                    - "os"
                    - "security"
                    - "updates"

            -   name: "ubuntu"
                osname: "ubuntu"
                type: "deb"
                master: "mos"
                baseurl: "http://archive.ubuntu.com/ubuntu"
                repositories:
                    - "{ubuntu_version} main multiverse universe"
                    - "{ubuntu_version}-update main multiverse universe"
                    - "{ubuntu_version}-security main multiverse universe"

            -   name: "centos"
                osname: "centos"
                type: "yum"
                master: "mos"
                baseurl: "http://mirror.centos.org/centos/{centos_version}"
                repositories:
                    - "os"
                    - "updates"

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

The developers will have library to deal with packages.

--------------------------------
Infrastructure impact
--------------------------------

CI and build tasks.
Need to build third-party packages, that will be required.

--------------------
Documentation impact
--------------------

Update documentation for fuel-createmirror and fuel-upgrade-packages utilities.

--------------------
Expected OSCI impact
--------------------

None

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  bgaifullin@mirantis.com

QA:
  akostrikov@mirantis.com

Mandatory design review:
  skulanov@mirantis.com
  vkozhukalov@mirantis.com


Work Items
==========

* Declare library interfaces and methods.

* Implement algorithm for dependency resolving.

* Implement file-transfer layer.

* Implement driver for Debian repositories.

* Implement driver for Yum repositories.

* Implement command-line interface for packetary.

* Rewrite fuel-createmirror interface by using API of packetary.


Dependencies
============

None

-----------
Testing, QA
-----------

We are going to test functionality on 3 levels:
Unit testing - doesn't need to be mentioned explicitly;
Functionl testing;
Integration testing.

Functional testing:
**Precondition**
Prepare repositories A and B, that met the requirements:
* Repository A contains packages that depends on packages from the B.
* Repository B is not depends on other repositories.

**Test cases**

* Copy repository B.
   Checks that all packages can be installed.

* Copy repository A and packages from B that is by A.
   Checks that all packages can be installed.

* Copy repository with network issues.
   Checks that correctly created mirror is done under
   network failures. Or it is failed with message.

* Copy repository via proxy.
   Checks that user can create mirror without full access
   to Internet.

All cases should be checked for Debian and RPM repositories.

Integration testing:
Tests which cover fuel-createmirror in fuel eco-system.
To deploy environment we should add custom packages to create
bootstrap image. So simple mirror copying is not enough to
have a successful deployment.

**Test cases**

* Install environment with 3 controllers, 1 cinder and 1 compute
   with custom mirror.
* Install environment with 3 controllers, 1 ceph and 1 compute
   with custom mirror.


Acceptance criteria
===================

User is able to create local mirror or update existing and
to deploy environment with that mirror.

There is documentation for utility.

----------
References
----------
.. [1] https://github.com/openstack/fuel-mirror/blob/master/fuel-createmirror
.. [2] https://en.wikipedia.org/wiki/Red–black_tree
.. [3] http://eventlet.net/doc/modules/greenpool.html
.. [4] https://github.com/openstack/fuel-web/tree/master/fuel_upgrade_system/fuel_package_updates/fuel_package_updates
