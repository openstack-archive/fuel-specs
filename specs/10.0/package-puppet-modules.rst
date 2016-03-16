..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

================================
Deploy fuel-library via packages
================================

https://blueprints.launchpad.net/fuel/+spec/package-puppet-modules

Replace the current method of consuming and delivering of Puppet modules
and manifests to the Fuel nodes with more generic package based one.

--------------------
Problem description
--------------------

Currently we have following workflow for consuming puppet modules and
manifests on Fuel slave nodes:

* Both fuel-library and required upstream Puppet modules are packaged
  as a single RPM.
* Upstream modules are sourced from stable tags defined as refs inside
  the following `Puppetfile`_ using `librarian-puppet-simple`_
* Openstack Puppet modules are sourced from stable tags defined as refs
  inside the following `OpenStack Puppetfile`_ using `librarian-puppet-simple`_
* The fuel-library RPM package tagged with Fuel release is installed on
  Fuel Master node as /etc/puppet/${openstack_release}-${fuel_version}
* /etc/puppet/manifests and /etc/puppet/modules symlinks are pointed to
  the respective folders inside
  the /etc/puppet/${openstack_release}-${fuel-version} hierarchy
* On Fuel slave nodes Astute uses the puppetsync agent to synchronize
  Puppet modules and manifests. This agent runs an rsync process that
  connects to the rsyncd server on the Fuel Master node and downloads
  the latest version of Puppet modules and manifests.
* Fuel installs the puppet-pull script. Developers can use it to manually
  synchronize manifests from the Fuel Master node and run the Puppet
  process on the Fuel slave node again.

The major downside of the current approach is the complicated integration
between system components, which, in its turn, creates `difficulties`_ in
running CI for Puppet modules.

----------------
Proposed changes
----------------

The proposals:

* Package the Puppet modules and manifests used on Fuel nodes using
  target base OS package format.
* Deploy fuel-library on Fuel nodes using these packages instead of
  rsync'ing Puppet modules and manifests from the Fuel Master node.

Benefits from using packaged Puppet modules and manifests:

* generic way of installing/updating system components
* the version of Puppet stuff always matches the target environments version,
  because it would be stored in a corresponding packages repository
* no need to specify Puppet stuff location in openstack.yaml
* no need to rsync manifests from the Fuel Master node, all updates to modules
  and manifests are distributed via packages
* packaged versions of Puppet modules could be reused by other community
  projects

Packaging of Puppet modules (upstream)
======================================

Packaging of Puppet modules in Fuel upstream should be done by the means of
`rpm-packaging`_ and `deb-packaging`_ projects. Please refer to the description
of these projects.

Packaging of Puppet OpenStack modules in downstream
===================================================

OpenStack Puppet modules listed in `OpenStack Puppetfile`_ should be packaged
according to the OpenStack packages workflow on Packaging CI:

* code and specs are taken from separate Gerrit repositories in puppet-modules
  and puppet-modules-build namespaces, accordingly)
* packages are rebuilt automatically on a daily basis, in case if there were
  changes to the code of a 'master' branch in a respective Puppet OpenStack
  project.

Packaging of other Puppet modules in downstream
===============================================

Upstream Puppet modules listed in `Puppetfile`_ should be packaged according to
the dependencies packages workflow on Packaging CI:

* code and specs are stored in the same Gerrit project inside the 'packages'
  namespace
* code is taken from stable tag specified as git reference in the `Puppetfile`_

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

Astute task to rsync Puppet modules from the Fuel Master node should
be replaced with installation of fuel-library package.

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

Changes to fuel-library packaging:

* 'fuel-library' package should include Fuel modules and manifests only
* each of required upstream Puppet modules should be packaged separately as
  'puppet-module-${MODULE-NAME}' using the code in the respective git
  reference specified in `Puppetfile`_
* fuel-library package should include runtime dependencies for all
  required upstream Puppet modules

------------
Alternatives
------------

We could package the Puppet modules and manifests as a bundle. However,
this will defeat the purpose of making packaged modules available to other
community projects. Also, bundling of shared 3rd party libraries is considered
bad practice in packaging policies, i.e. `Debian Policy`_

--------------
Upgrade impact
--------------

This change simplifies the upgrade procedure by providing more generic way
to install/update Puppet modules and manifests.

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

None

----------------
Developer impact
----------------

Developers should be able to work with their changes to the upstream
Puppet modules and manifests using rsync workflow. All modules and
manifests installed on slave nodes, should be accessible under the
/etc/puppet folders hierarchy.

---------------------
Infrastructure impact
---------------------

None

--------------------
Documentation impact
--------------------

Related parts of `Fuel Architecture`_ guide should be updated.

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  `Vitaly Parakhin`_

Mandatory design review:
  `Roman Vyalov`_
  `Sergii Golovatiuk`_
  `Vladimir Kozhukalov`_

Work Items
==========

* Create fuel-library DEB package
* Create RPM and DEB packages for upstream Puppet modules and manifests
* Replace puppetsync stuff in Astute and fuel-library with package
  installation
* Update related parts in Fuel documentation

Dependencies
============

None

------------
Testing, QA
------------

No additional tests is required to verify switching to package based deployment
of fuel-library, as standard set of tests already covers all cases.

Acceptance criteria
===================

* Puppet modules and manifests from fuel-library are packaged as DEB
* each of upstream Puppet modules and manifests is packaged as separate
  RPM and DEB
* Fuel Master node can be deployed using packaged versions of fuel-library
  and upstream Puppet modules
* fuel-library can be deployed on a Fuel slave nodes using fuel-library
  and upstream DEB packages

----------
References
----------

.. _`Puppetfile`: https://github.com/openstack/fuel-library/blob/master/deployment/Puppetfile
.. _`OpenStack Puppetfile`: https://github.com/openstack/fuel-library/blob/master/deployment/puppet/openstack_tasks/Puppetfile
.. _`librarian-puppet-simple`: https://github.com/bodepd/librarian-puppet-simple
.. _`difficulties`: http://lists.openstack.org/pipermail/openstack-dev/2016-February/087620.html
.. _`rpm-packaging`: https://github.com/openstack/rpm-packaging
.. _`deb-packaging`: https://wiki.openstack.org/wiki/Packaging/Debian
.. _`Fuel Architecture`: https://github.com/openstack/fuel-web/blob/master/docs/develop/architecture.rst
.. _`Debian Policy`: https://wiki.debian.org/UpstreamGuide#No_inclusion_of_third_party_code
.. _`Roman Vyalov`: https://launchpad.net/~r0mikiam
.. _`Sergii Golovatiuk`: https://launchpad.net/~sgolovatiuk
.. _`Vladimir Kozhukalov`: https://launchpad.net/~kozhukalov
.. _`Vitaly Parakhin`: https://launchpad.net/~vparakhin