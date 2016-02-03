..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=================================
Remove CentOS bootstrap from Fuel
=================================

https://blueprints.launchpad.net/fuel/+spec/remove-centos-bootstrap-from-fuel


--------------------
Problem description
--------------------

At the moment we build Centos bootstrap OS image together with ISO and then
package it into rpm. Since Fuel 8.0 we switched to Ubuntu bootstrap image
usage [1]_ and CentOS one became deprecated, so in Fuel 9.0 we can freely
remove it [2]_.

By removing fuel-bootstrap-image [2]_ we:

* simplify patching/update story, since we don't need to rebuild/deliver this
  package on changes in dependent packages [3]_.

* speed-up ISO build process, since building centos bootstrap image takes ~ 20%
  of build-iso time.


----------------
Proposed changes
----------------

Remove CentOS bootstrap image usage from Fuel projects.


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

* CentOS cobbler profiles should be removed from fuel-library code
* The default `bootstrap_profile` should be set to `ubuntu_bootstrap`


------------
Alternatives
------------

Currently we build Ubuntu bootstrap OS image on the master node using
Fuel Agent. Although Fuel Agent does not support building Centos images
we can implement such functionality.

We need to implement build image utilities for Centos and modify Fuel Agent
build image manager method and probably input data driver so as to make it
possible to use Fuel Agent to build Centos images.


--------------
Upgrade impact
--------------

We no longer need to deliver/update fuel-bootstrap-image package [2], this will
simplify patching/update story, since we don't need to rebuild this package on
each changes in any dependent packages [3]_:

  * fuel-agent;
  * nailgun-agent;
  * nailgun-mcagents;
  * network-checker;
  * rubygem-ffi-yajl;
  * rubygem-ffi;
  * rubygem-mime-types;
  * rubygem-mixlib-shellout;
  * rubygem-wmi-lite.


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

* ISO build time decreased at least for ~20%

* The OpenStack nodes themselves are not affected in any way


-----------------
Deployment impact
-----------------

* CentOS bootstrap image profile should be removed from cobbler
* CentOS flavour should be removed from fuel-menu


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

Changes should be reflected in documentation.


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  `Sergey Kulanov`_


Work Items
==========

* Remove CentOS bootstrap image selection from `fuel-menu <https://github.com/openstack/fuel-menu>`_
* Switch to Ubuntu bootstrap in `fuel-library <https://github.com/openstack/fuel-library>`_
* Remove fuel-bootstrap-image [2]_
* Remove related code from `fuel-qa <https://github.com/openstack/fuel-qa>`_ and
  `fuel-devops <https://github.com/openstack/fuel-devops>`_


Dependencies
============

None


------------
Testing, QA
------------

Related changes should be made in `fuel-devops <https://github.com/openstack/fuel-devops>`_
and `fuel-qa <https://github.com/openstack/fuel-qa>`_ since `bootstrap.rsa`
key file will no longer exist


Acceptance criteria
===================

  * ISO should pass QA acceptance criteria (SWARM % pass)
  * User should not ba able to use CentOS bootstrap image

----------
References
----------

.. _`Sergey Kulanov`: https://launchpad.net/~skulanov

.. [1] `Use Ubuntu as an operating system of Fuel bootstrap nodes <https://blueprints.launchpad.net/fuel/+spec/fuel-bootstrap-on-ubuntu>`_
.. [2] `fuel-bootstrap-image RPM package spec <https://github.com/openstack/fuel-main/blob/master/packages/rpm/specs/fuel-bootstrap-image.spec>`_
.. [3] `fuel-bootstrap-image dependencies <https://github.com/openstack/fuel-main/blob/master/bootstrap/module.mk#L12-L50>`_
