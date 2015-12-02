..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==============================================================
Naming policy for deb packages must be similar as used for RPM
==============================================================



-------------------
Problem description
-------------------

Old versioning scheme does not represents proper meta-data for *deb*
packages. For *rpm* packages we have agreed scheme (`separate-mos-from-centos`_)
wich is representing proper meta-data at package suffix part and know *deb*
packages need to be renamed with the account of specific of distribution.


----------------
Proposed changes
----------------

Need to introduce into CI/Build new naming and version policy for *deb*
packages instead of using elaborated previously `old scheme`_.


-------------------------------
Package versioning requirements
-------------------------------
Package version string, as well as package metadata for a *MOS specific* or
*divergent* package must not include registered trademarks of base distro
vendors, and should include "mos" keyword.


-----------------------
DEB packages versioning
-----------------------

Package name constructs from::

    <name>-<version><deb-revision>~<base-distro-release>+mos<subrevision>

For example::

    python-nova-12.0.0-1~u14.04+mos8.0.5

Where:

- python-nova - name
- 12.0.0 - code version
- 1 - debian package revision
- u14.04 - base Linux distribution
- mos8.0.5 - mos<subversion>

  Where:

  - mos8 - major MOS release version
  - 0 - minor MOS release version
  - 5 - amount of commits into code since last tag change in current code branch

At present moment *MOS subversion* part represented as amount of commits into
code since code brach was created.

**Version in changelog file should be modified by CI/Build:**

CI/Build system should modify deb *changelog* value before build
process to ensure that package version and release represents truth:

Example::

    was:    nova (2:12.0.0-1~u14.04+mos823) mos8.0; urgency=medium
    became: nova (2:12.0.0-1~u14.04+mos8.0.5) mos8.0; urgency=medium

This modification leads to transformations as follows::

    python-nova-12.0.0-1~u14.04+mos823 -> python-nova-12.0.0-1~u14.04+mos8.0.5

**Subversion:**

This number represents amount of commits into code since last tag change in
current code branch and must be added after **mosX.X**.

Example::

    python-nova-12.0.0-1~u14.04+mos8.0.5 -> python-nova-12.0.0-1~u14.04+mos8.0.6

**Structure of Subversion for packages maintained by Mirantis:**

python-nova-12.0.0-1~u14.04+mos8.0.5
Where:

- + separator from base Linux distribution.
- mosX.X - X.X represents major and minor version of MOS release.
- 3rd X - represents commits number since last tag/branch update in code.

For example we have python-nova package with code version = *12.0.0*

- debian package revision = *1*,
- Linux distro short name(Ubuntu 14.04) = *u14.04*,
- MOS release = *mos8.0*,
- commits number into code within code version 12.0.0 = *5*.

Only packages from *security* repository should have security update
bundle number at the very end!

Regular packages should only have commits number for the very last
value in version string.


--------
Backport
--------

If package needs to be backported by any reason - name and version must be
kept. Modification required for *subversion* part, initial revision of debian
package also should be preserved. Any further modifications of package will be
represented in commits number which follows after *mosX.X*. By default this
value will be always set to 1 and will be increased in case of package
modification.

Example::

    python-zzzeeksphinx_1.0.17-1~u14.04+mos8.0.1 -> python-zzzeeksphinx_1.0.17-1~u14.04+mos8.0.2
    python-zzzeeksphinx_1.0.17-1~u14.04+mos8.0.3 -> python-zzzeeksphinx_1.0.17-1~u14.04+mos8.0.3


--------------
Package update
--------------

If required to update package build manifests (debian/ folder) or add patch or
make any other modifications not related to code version update, debian package
revision number must be increased. If a major change (new version of the
software being packaged) occurs, the version number is changed to reflect the
new software version, and debian package release number is reset to 1. In case
of packages maintained by MOS this is **valid for OpenStack** projects.

For **non OpenStack** projects, like dependencies and back-ported packages all
updates will be represented in commits number part of release. After code
version update Commits number value resets to 1 and will be increased in cases
of further modifications of a package.

Update of dependencies within one code version(*non OpenStack*)::

    python-zzzeeksphinx_1.0.17-1~u14.04+mos8.0.1 -> python-zzzeeksphinx_1.0.17-1~u14.04+mos8.0.2

Update of dependencies in case of code version update(*non OpenStack*)::

    python-zzzeeksphinx_1.0.17-1~u14.04+mos8.0.2 -> python-zzzeeksphinx_1.0.19-1~u14.04+mos8.0.1

Update of OpenStack project - debian/ changed::

    python-nova-12.0.0-1~u14.04+mos8.0.5 -> python-nova-12.0.0-2~u14.04+mos8.0.5

Update of OpenStack project - code tag/branch changed::

    python-nova-12.0.0-2~u14.04+mos8.0.5 -> python-nova-13.0.0-1~u14.04+mos8.0.1


----------------------------------------------
Versioning of packages in post-release updates
----------------------------------------------

**Updates:**

Since MOS reaches GA status, ie officially released, all updated packages will
be published into separate *updates* repository. Updated package will have
higher commit number value in the release part then package from stable
repository.

Example::

    python-zzzeeksphinx_1.0.17-1~u14.04+mos8.0.20 -> python-zzzeeksphinx_1.0.17-1~u14.04+mos8.0.21
    python-nova-12.0.0-1~u14.04+mos8.0.15 -> python-nova-12.0.0-1~u14.04+mos8.0.16


**Security updates:**

Security updates will also be published in a separate repository and based on
package from *updates* repository. Additional subsequent digit will be added to
the version of a package which represents security bundle number.

Example::

    python-zzzeeksphinx_1.0.17-1~u14.04+mos8.0.21 -> python-zzzeeksphinx_1.0.17-1~u14.04+mos8.0.21.1
    python-nova-12.0.0-1~u14.04+mos8.0.16 -> python-nova-12.0.0-1~u14.04+mos8.0.16.1


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

None


---------------------
Infrastructure impact
---------------------

None


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
  `Dmitry Burmistrov`_
  `Alexander Tsamutali`_

Build-team:
  `Dmitry Burmistrov`_


Mandatory Design Reviewers:
  - `Dmitry Burmistrov`_
  - `Roman Vyalov`_
  - `Dmitry Borodaenko`_


Work Items
==========

- Update CI/Build jenkins jobs.
- Rebuild ded packages according to this policy.


Dependencies
============

- `separate-mos-from-centos`_

------------
Testing, QA
------------

None


Acceptance criteria
===================

* Packages at MOS repository has **mos8.0.X** in their names.


----------
References
----------

.. _`Alexander Tsamutali`: https://launchpad.net/~astsmtl
.. _`Dmitry Borodaenko`: https://launchpad.net/~angdraug
.. _`Dmitry Burmistrov`: https://launchpad.net/~dburmistrov
.. _`Igor Yozhikov`: https://launchpad.net/~iyozhikov
.. _`Roman Vyalov`: https://launchpad.net/~r0mikiam
.. _`separate-mos-from-centos`: https://github.com/openstack/fuel-specs/blob/master/specs/8.0/separate-mos-from-centos.rst
.. _`old scheme`: https://github.com/openstack/fuel-specs/blob/master/specs/6.1/separate-mos-from-linux.rst
