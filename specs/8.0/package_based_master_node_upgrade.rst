..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=================================
Package based master node upgrade
=================================

https://blueprints.launchpad.net/fuel/+spec/package-master-node-upgrade

--------------------
Problem description
--------------------

Currently, we use tarball based approach for the master node upgrade. It
assumes we package everything we need for upgrade into the tarball including
Centos and Ubuntu mirrors, pip packages for virtual environment, docker
containers, some build related files and upgrade script itself.
However, this tarball approach contradicts with our package
based approach to deliver updates.

----------------
Proposed changes
----------------

We should get rid of upgrade tarball in favor of upgrade rpm package. It is
enough to package upgrade script itself into rpm and then a user is to install
this package and run the script to upgrade the master node.

User experience is to be like the following:

#. User downloads rpm package fuel-release-X.Y.Z.rpm and installs it using
   ``rpm -i fuel-release-X.Y.Z.rpm`` command. This package configures X.Y.Z
   yum repositories.
#. User installs fuel-X.Y.Z.rpm package (meta package) which requires other
   fuel packages like fuel-docker-images-X.Y.Z, fuel-upgrade-X.Y.Z etc.
#. User runs upgrade script ``/usr/bin/fuel-upgrade`` which is an executable
   entry point for upgrade script written in python.
#. This script does everything else including stopping old containers and
   starting new ones, moving some files and creating some links,
   uploading some fixtures, etc.

In order to make this happen we need to change upgrade script itself as well
as the upgrade delivery approach.

#. We don't need to copy package repositories from upgrade tarball to the
   master node any more. We assume all necessary repositories are either
   available online or mirrored locally using fuel-createmirror.
#. Installing fuel-release package will configure new repositories on the
   master node as well as install necessary keys.
#. We don't need version.yaml file any more as it assumes master node is
   installed from ISO and all packages installed on the master node came
   from rpm repository provided by ISO. The majority of parameters set in
   version.yaml can be either packaged into rpm or deprecated/substituted.

Below is an example of the version.yaml file:

::

  VERSION:
    feature_groups:
      - mirantis
    production: "docker"
    release: "7.0"
    openstack_version: "2015.1.0-7.0"
    api: "1.0"
    build_number: "82"
    build_id: "2015-07-23_10-59-34"
    nailgun_sha: "d1087923e45b0e6d946ce48cb05a71733e1ac113"
    python-fuelclient_sha: "471948c26a8c45c091c5593e54e6727405136eca"
    fuel-agent_sha: "bc25d3b728e823e6154bac0442f6b88747ac48e1"
    astute_sha: "b1f37a988e097175cbbd14338286017b46b584c3"
    fuel-library_sha: "58d94955479aee4b09c2b658d90f57083e668ce4"
    fuel-ostf_sha: "94a483c8aba639be3b96616c1396ef290dcc00cd"
    fuelmain_sha: "68871248453b432ecca0cca5a43ef0aad6079c39"

Let's go through this file step by step.

#. feature_groups - It is, in fact, runtime parameter and it should be moved
   into nailgun config.
#. production - It is always equal to "docker" when we build ISO and deploy
   the Fuel master node, but it can be set to other values when we deploy
   fake UI or when we run functional tests for UI and python-fuelclient. So,
   it is seems to be runtime parameter rather than buildtime and it also
   should be moved into nailgun config file.
#. release - It is like /etc/issue and it, in fact, reflects which
   repositories are currently configured. For example in Fedora this
   file /etc/issue is provided by fedora-release package. So, we probably
   can put this value into /etc/fuel-issue and put this file into fuel-release
   package. This value is shown on UI.
#. openstack_version - It is just an extraction from openstack.yaml. There is
   no need to have this value somewhere else.
#. api -  It is 1.0 currently. And we still don't have other versions of API.
   Even more, it contradicts to the common practice to make several different
   versions available at the same time. And a user should be able to ask API
   which versions are currently available. It should be deprecated.
#. build_number - I don't even know if it makes any sense to have this
   information on the master node. Probably, it is only makes it a little bit
   more convenient to troubleshoot issues during development. It is related
   to a particular ISO and can be moved to, say, /etc/fuel-buildstamp.
#. build_id - Same as above.
#. <project>_sha - These are just SHA sums and this list can be easily
   substituted by rpm -qa output.
   One can easily find out SHA from the package version.
   (Perestroika is going to increase the package version every time when
   it re-builds a package.)

Therefore, this file version.yaml should be deprecated and the information
from this file should be partly available from other sources mentioned above.

Upgrade script needs some information from openstack.yaml file as well [1]_.
This file is available in nailgun package, and it seems that it is rational to
put this file also into a separate package, let's say fuel-openstack-metadata.
fuel-upgrade package is to depend on this separate fuel-openstack-metadata
package.


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

Upgrade tarball does not match our recent efforts to move to package based
approach.

--------------
Upgrade impact
--------------

Upgrade experience is going to change significantly according to the spec.

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

Upgrade UX is going to become easier.

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

None

--------------------------------
Infrastructure/operations impact
--------------------------------

* Upgrade tarball is going to be deprecated. So, all related jobs
  should be modified.
* fuel-upgrade package should be built and become a part of MOS repo.
* Other packages like fuel-release and fuel-openstack-metadata should
  be built as a part of version.yaml deprecation plan.

--------------------
Documentation impact
--------------------

The Fuel documentation should be modified so it contains necessary
information about new upgrade flow.

--------------------
Expected OSCI impact
--------------------

Several additional packages should be built (at least):
* fuel-upgrade
* fuel-release
* fuel-openstack-metadata

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  Vladimir Kozhukalov <vkozhukalov@mirantis.com>

Work Items
==========

#. Introduce fuel-release package
#. Deprecate version.yaml
#. Remove ubuntu-versions.yaml and centos-versions.yaml
#. Put openstack.yaml into a separate package.
#. Modify upgrade script according to switching to package based approach.

Dependencies
============

None

------------
Testing, QA
------------

Testing approach is not going to be changed significantly. The only difference
is that instead of downloading upgrade tarball we need to install
fuel-upgrade package and then run upgrade script.

Acceptance criteria
===================

- Upgrade tarball must be deprecated
- Upgrade script should be delivered via fuel-upgrade package
- Upgrade UX should be modified as described above in the specification

----------
References
----------

.. [1] https://github.com/stackforge/fuel-web/blob/master/nailgun/nailgun/fixtures/openstack.yaml
