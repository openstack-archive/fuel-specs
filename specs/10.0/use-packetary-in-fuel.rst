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
tool both in the ISO build process and on the Fuel master node side.

--------------------
Problem description
--------------------

When building the ISO there is no need to create full upstream mirror
locally and then put it to the ISO. Instead we have the minimal
list of required packages. Then we can use tools ``yumdownloader``
to recursively resolve package dependencies and
download this minimal consistent tree.

Currently we use ``yumdownloader``/``reposync`` and ``debmirror``
for downloading rpm/deb packages while
building the Fuel ISO image. To mix packages from
different RPM repos on the Fuel master node we use the EXTRA_RPM_REPOS
variable. We are forced to deal with several tools at the same time
that provide user interfaces and functionality which are not
fully compatible with data structures that we currently use in Fuel.

Besides, we still build Fuel packages together with the ISO which
does not scale well. We have a specific service for building packages
not only from merged source code but also from the code that is
currently on review. The idea behind is to use these packages
to run deployment tests before a patch is even merged. Some cases,
however, assume putting these custom packages on a custom ISO,
but our current build code does not allow to download deb
packages from these custom repositories during ISO build.
This EXTRA_RPM_REPOS variable works only in rpm case. Custom
deb repos can only be used during deployment itself.

The existing approach has the following disadvantages:

* The code for fetching RPM/DEB repositories is strictly tied to the set of
  internal configuration values.
* The code for creation of local repositories structure on a Fuel master node
  does not support having multiple OpenStack releases within an ISO.
* There is no possibility to include a set of user-defined extra DEB
  repositories to a product ISO, and automatically add them to Nailgun.

The easiest way to address all these issues is to use Packetary [1]_ for
the ISO build process.

The thing is that neither ``yumdownloader`` nor ``debmirror`` provide the level
of convenience and flexibility that Packetary does. Packetary allows to
download everything that we need running it just once passing
input data (yaml) in exactly the same format that we use for Fuel-menu
and for Nailgun [2]_. By the way, it is a flat list of repositories with their
priorities. All downloaded packages could either be merged into a single
repository or into a set of repositories depending on what one needs.
The process is fully data driven.

So, using Packetary we could make ISO build process really flexible.
One could put into the ISO packages from arbitrary number of custom
repositories. We could even check if this particular set of repositories
is consistent, i.e. there are no conflicting dependencies.

----------------
Proposed changes
----------------

We propose to replace current tools mentioned above with Packetary
which will process a user-defined list of RPM/DEB repositories and perform the
following actions.

At the ISO image build stage:

* download specified RPM/DEB packages/repositories (and, if required, create
  new repositories based on the list of packages)
* put these repositories to the ISO along with the user-defined config file
  (exactly the file that was used while downloading packages)
  to set yum/apt repository configuration so to use locally
  copied repositories.

At the base OS provisioning stage:

* put these repositories from the ISO to a user-defined target paths on the Fuel
  master node

At the master node deployment stage:

* configure yum/apt repositories using this config file that was used on the
  build stage and then was put on the ISO
* configure default repositories in fuel-menu and nailgun using the same
  config file


How are we planning to integrate this new approach into Fuel CI?

* We are planning to remove from fuel-main all those data structures
  that are related to Fuel infrastructure. There won't be variables like
  USE_MIRROR=* that assume having hardcoded mirror urls for various
  locations. Build system is to become fully data driven. We will
  provide just few very basic defaults like current CentOS upstream and
  maybe current MOS urls.
* We will use repository configuration template structure that is to
  reflect the standard repository structure (that is not exact file content).
  This file is to be rendered using environment variables set by Jenkins ISO
  build job. These environment variables could be exposed to the custom job
  web interface.

..

    - name: "os"
      path: "upstream"
      uri: "{{CENTOS_URL}}/os/x86_64"
      priority: 99
    - name: "updates"
      path: "upstream"
      uri: "{{CENTOS_URL}}/updates/x86_64"
      priority: 10
    - name: "extras"
      path: "upstream"
      uri: "{{CENTOS_URL}}/extras/x86_64"
      priority: 99
    - name: "centosplus"
      path: "upstream"
      uri: "{{CENTOS_URL}}/centosplus/x86_64"
      priority: 99
    - name: "mos"
      path: "mos-centos"
      uri: "{{MOS_URL}}/x86_64"
      priority: 5
    - name: "mos-updates"
      path: "mos-centos-updates"
      uri: "{{MOS_UPDATES_URL}}/x86_64"
      priority: 1

* This data structure, however, does not contain custom
  repositories. To cover this case with custom repositories we
  will expose to the Jenkins web interface a form that is to be
  used for uploading custom yaml file. So, a user can prepare
  yaml file using her favorite text editor and probably some
  utilities and use this file to run custom build job.


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
include their own set of RPM/DEB repositories. If one needs just to
change mirror base url, the it is to be possible to use environment
variables.

------------------
Performance impact
------------------

ISO build process should become faster or remain the same.

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
dependencies installed. Packetary could be installed using pip.

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
  Vladimir Kozhukalov <vkozhukalov@mirnatis.com>

Other contributors:
  Bulat Gaifullin <bgaifullin@mirnatis.com>

Mandatory design review:
  Vitaly Parakhin <vparakhin@mirantis.com>
  Alexandra Fedorova <afedorova@mirantis.com>


Work Items
==========

* Add necessary functionality to Packetary
* Create a patch to fuel-main to introduce Packetary to the build process
* Create Jenkins jobs (product and custom)

Dependencies
============

None

------------
Testing, QA
------------

The ISO should pass the same set of system and deployment tests.

Acceptance criteria
===================

1. Build script should use Packetary as a tool to download packages during
   ISO build.
2. ISO build when using Packetary should not be longer than it is now.
3. It should be possible to define repos during ISO build using a flat
   prioritized list.
4. It should be possible to use several custom repos at the same time.

----------
References
----------

.. [1] `Packetary <https://github.com/openstack/packetary>`_
.. [2] `Unify the input data <https://github.com/openstack/fuel-specs/blob/master/specs/9.0/unify-the-input-data.rst>`_
