..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==================================================
Use Packetary for downloading MOS rpm/deb packages
==================================================

https://blueprints.launchpad.net/fuel/+spec/use-packetary-in-fuel

The current scheme of working with repositories in Fuel is quite messy,
rigid, and incompatible with upcoming architectural changes. We are
going to rework the whole approach to downloading rpm/deb packages
and handling of local/remote mirrors by introducing the packetary
tool both in the ISO build process and on the Fuel Admin node side.

--------------------
Problem description
--------------------

Currently we use yumdownloader/reposync and debmirror for downloading
rpm and deb packages while building an ISO, respectively. To mix packages
from different RPM repos on the Fuel Admin node we use the EXTRA_RPM_REPOS
variable.

The corresponding functionality for mixing DEB packages during the cluster
deployment is described in the following specification. [1]_

List of upstream RPM packages is generated as a result of processing of the
requirements-rpm.txt file by yumdownloader. The RPM packages are fetched with
wget, then a repository from these packages is created with createrepo utility.
The resulting repository is copied to a Fuel Admin node during base OS
provisioning, and added to the local Yum configuration.

Base MOS RPM repository, as well as one or multiple RPM repositories specified
in the EXTRA_RPM_REPOS variable are fetched to an ISO with reposync as is,
then copied to a Fuel Admin node during base OS provisioning, and added to the
local Yum configuration.

The base MOS DEB repository is fetched to an ISO, then copied to a Fuel Admin
node during base OS provisioning.

The existing approach has the following disadvantages:

* The code for fetching RPM/DEB repositories is strictly tied to the set of
  internal configuration values.
* In some cases, the code for creating local repositories can override metadata
  of already downloaded DEB repository (suite).
* The code for creation of local repositories structure on a Fuel Admin node
  does not support having multiple OpenStack releases within an ISO.
* There is no possibility to include a set of user-defined extra DEB
  repositories to a product ISO, and automatically add them to Nailgun.

----------------
Proposed changes
----------------

We propose to replace the tools mentioned above with a data-driven application
which will process a user-defined list of RPM/DEB repositories and perform the
following actions.

During an ISO build:

* download specified RPM/DEB repositories (and, if required, create new
  repositories based on the list of packages) using packetary [2]_
* put these repositories to an ISO, along with the user-defined config file

During Fuel Admin node base OS provisioning stage:

* put these repositories from an ISO to a user-defined target paths on a Fuel
  Admin node

During Fuel Admin node deployment stage:

* add appropriate RPM repositories to the local Yum configuration on a Fuel
  Admin node
* add repositories to Naigun, using fuelclient

The best way to define a set of repos is to use the same data structure like
we have in fuel-menu or fuel-web. It is a flat prioritized set of repos.
Packetary allows to download packages from many repos using this flat data
structure. [3]_


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

None

Orchestration
=============

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

Provide repositories for different OpenStack versions as "pluggable" build
artifacts (RPMs) which include:

* a repository itself (packages + metadata)
* local yum/apt configuration (if required)
* post-install script to add repository to Nailgun (if needed)

However, this approach imposes significant impact on CI systems, and does not
solve extra repos issue.

--------------
Upgrade impact
--------------

Proposed changes allow to simplify the upgrade procedure by unifying the Fuel
repositories workflow.

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

Users will be required to create or modify the yaml configuration file to
include their own set of RPM/DEB repositories.

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

---------------------
Infrastructure impact
---------------------

Using packetary allows us to cover such cases as:

* mix upstream and testing repos on deployment stage
* use custom repos (and custom packages)

Fuel 9.0+ ISO build environments should have packetary and all its
dependencies installed.

--------------------
Documentation impact
--------------------

None

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  <launchpad-id or None>

Other contributors:
  <launchpad-id or None>

Mandatory design review:
  <launchpad-id or None>


Work Items
==========

<TBD>

Dependencies
============

<TBD>

------------
Testing, QA
------------

Please discuss how the change will be tested. It is assumed that unit test
coverage will be added so that doesn't need to be mentioned explicitly.

This should include changes / enhancements to any of the integration
testing. Most often you need to indicate how you will test so that you can
prove that you did not adversely effect any of impacts sections above.

If there are firm reasons not to add any other tests, please indicate them.

After reading this section, it should be clear how you intend to confirm that
you change was implemented successfully and meets it's acceptance criteria
with minimal regressions.

Acceptance criteria
===================

1. Build script should use packetary as a tool to download packages during ISO build.
2. ISO build when using packetary should not be longer than it is now.
3. It should be possible to define repos during ISO build using a flat prioritized list.
4. It should be possible to use several custom repos at the same time.

----------
References
----------

.. [1] `Consume External Ubuntu <https://github.com/openstack/fuel-specs/blob/master/specs/6.1/consume-external-ubuntu.rst>`_
.. [2] `Packetary <https://github.com/openstack/packetary>`_
.. [3] `Unify the input data <https://github.com/openstack/fuel-specs/blob/master/specs/9.0/unify-the-input-data.rst>`_

