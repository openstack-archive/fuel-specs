..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=================================================================
Separate deployment of Fuel Master Node from base OS provisioning
=================================================================

https://blueprints.launchpad.net/fuel/+spec/separate-fuel-node-provisioning

Split the Fuel Master Node installation process into base OS provisioning and
Fuel Master Node deployment parts.

--------------------
Problem description
--------------------

Currently, the setup of Fuel Master Node is provided by monolithic combination
of Anaconda kickstart with custom preinstall/postinstall scripts, and the
mixed set of upstream and MOS packages. The entire process is tied to
the installation media (ISO or USB stick). There is no possibility to install
Fuel on a pre-provisioned system which contains base OS packages only.

By separating the Fuel Master Node deployment from provisioning we will:

* support the modularization trend in Fuel
* simplify the use of light-weight tests on Fuel CI

----------------
Proposed changes
----------------

Changes to Fuel Master Node installation
========================================

Fuel Master Node should be provisioned using the upstream OS packages only.
To guarantee that, the Fuel Master Node kickstart should contain no `repo`_
entries other than the upstream OS ones. The %packages section should contain
only the "@Core" packages group.

There could be cases when upstream OS packages used during provisioning could
overlap with the MOS packages required for Fuel Master Node deployment. The
deployment script should guarantee that overlapping MOS packages will be
installed during deployment stage, replacing the respective upstream OS
packages.

The following changes are proposed to the post-install scripts in the Fuel
Master Node kickstart:

* `additional configuration`_ for various system services - will be moved to
  the Fuel Master Node deployment script (bootstrap_admin_node.sh)
* `installation of the bootstrap_admin_node.sh script`_ - will be moved to the
  separate RPM package named "fuel-deploy"
* one-time `autologon`_ service configuration - will include installation of
  the "fuel-deploy" RPM package before running the bootstrap_admin_node.sh
  script

Web UI
======

No changes required.

Nailgun
=======

No changes required.

Data model
----------

No changes required.

REST API
--------

No changes required.

Orchestration
=============

No changes required.

RPC Protocol
------------

No changes required.

Fuel Client
===========

No changes required.

Plugins
=======

No changes required.

Fuel Library
============

No changes required.

------------
Alternatives
------------

Implementation of this feature has no altrenatives.

--------------
Upgrade impact
--------------

No changes required.

---------------
Security impact
---------------

No changes required.

--------------------
Notifications impact
--------------------

No changes required.

---------------
End user impact
---------------

Implementing this feature does not change the UX and deployment parts.

------------------
Performance impact
------------------

No changes required.

-----------------
Deployment impact
-----------------

Changes described in this document only affect Fuel Master Node installation.

----------------
Developer impact
----------------

No changes required.

---------------------
Infrastructure impact
---------------------

Implementing this feature could greatly affect the CI systems by minimizing
the efforts needed to deploy Fuel Master Node on top of an existing base OS
environment.

--------------------
Documentation impact
--------------------

Possibility to deploy the Fuel Admin node on a pre-provisioned system should
be reflected in the Fuel User guide.

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  `Vitaly Parakhin`_

Mandatory design review:
  `Oleg Gelbukh`_
  `Roman Vyalov`_
  `Vladimir Kozhukalov`_

QA:
  <TBD>

Work Items
==========

* Modify kickstart to separate base OS provisioning from Fuel deployment
* Prepare package for automatic configuration of the MOS repositories in yum
* Package the Fuel installation script

Dependencies
============

None

------------
Testing, QA
------------

Integration Tests
=================

As long as the feature introduces the ability to install Fuel separately from
product ISO, there should be a test that implements that feature.

Acceptance criteria
===================

* Installation of Fuel Master Node is clearly separated between base OS
  provisioning (upstream OS packages) and Fuel Master Node deployment (MOS
  packages)
* Fuel Master Node can be deployed on an pre-provisioned CentOS 7 server using
  either online repositories (Internet access is required), or MOS ISO (Internet
  access is optional)

----------
References
----------

.. _`repo`: https://github.com/rhinstaller/pykickstart/blob/master/docs/kickstart-docs.rst#repo
.. _`additional configuration`: https://github.com/openstack/fuel-main/blob/10b609078e81b3fc704ac8aa39f41c463c56af76/iso/ks.template#L510-L614
.. _`installation of the bootstrap_admin_node.sh script`: https://github.com/openstack/fuel-main/blob/10b609078e81b3fc704ac8aa39f41c463c56af76/iso/ks.template#L547-L549
.. _`autologon`: https://github.com/openstack/fuel-main/blob/10b609078e81b3fc704ac8aa39f41c463c56af76/iso/ks.template#L620-L642
.. _`Oleg Gelbukh`: https://launchpad.net/~gelbuhos
.. _`Roman Vyalov`: https://launchpad.net/~r0mikiam
.. _`Vladimir Kozhukalov`: https://launchpad.net/~kozhukalov
.. _`Vitaly Parakhin`: https://launchpad.net/~vparakhin