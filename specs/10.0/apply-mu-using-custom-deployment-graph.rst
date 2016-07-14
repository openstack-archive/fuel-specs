..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

======================================================================
Apply maintenance updates on slave nodes using custom deployment graph
======================================================================

With new Fuel capability [0]_ to execute custom deployment graphs we could
improve process of applying maintenance updates on the slave nodes of already
deployed OpenStack environment. We can use parallelization and cross-node
dependencies features that will allow us to apply updates on the slave nodes
faster and in more automated way.

-------------------
Problem description
-------------------

Currently we recommend to install maintenance updates on the slave nodes using
the `mos_apply_mu.py` [1]_ script on Fuel master node and manually restarting
all affected services on all slave nodes. This process is manual and error
prone. Custom deployment graphs feature could be used to improve and automate
this process.

----------------
Proposed changes
----------------

Maintenance update installation could be performed by executing predefined
custom graph instead of using the `mos_apply_mu.py` [1]_ script and restarting
services manually. This custom graph needs to be developed, included into some
Fuel package and delivered to master node together with some maintenance
update.
Limitation: this spec covers only installation of the latest available
maintenance update (installation of specific maintenance update requires
more work and is out of scope of this spec).


Web UI
======

None.


Nailgun
=======

None.

Data model
----------

None.


REST API
--------

None.

Orchestration
=============

None.


RPC Protocol
------------

None.


Fuel Client
===========

Add the following commands to the Fuel CLI::

    fuel -> updates --env env_id --> check --> installed
                           |           |
                           |           +----> available
                           |
                           +-------> install

The Fuel CLI command ``updates --env env_id check installed`` will check the version of the
Maintenance Update applied (if any) by checking the file
`/etc/fuel/mu-version.json` which is delivered as a part of the `fuel-misc`
package to every node in the particular environment.

The command ``updates --env env_id check available`` will parse the contents of the
file `mu-version.json` in the appropriate sub-folder in `/mcv/mos/` on the
official Fuel mirror `mirror.fuel-infra.org` [3]_, then check its contents
against the local file `/etc/fuel/mu-version.json` and show the user if there
are new updates available. If there is no local information to compare with,
the case should be treated as no Maintenance Update is currently installed.

Having this information the user may decide whether to apply a new update
using the command ``updates --env env_id install`` or it already has the needed Maintenance
Update installed. In case of successful installation of the Maintenance
Update its version and timestamp will be stored on each node locally as
`/etc/fuel/mu-version.json` to make further checks against the Fuel mirror
possible.


Plugins
=======

None.


Fuel Library
============

Before publishing each Maintenance Update the file `mu-version.json` should be
updated in the fuel-library `files/fuel-misc` folder. This file will be
delivered to all nodes as an update of the `fuel-misc` package.


------------
Alternatives
------------

Alternative way of installing maintenance updates on slave nodes is to use
current method with the `mos_apply_mu.py` [1]_ script and restarting services
manually. This case described here at [2]_.
Also we can install maintenance updates manually using package management
system on every slave node, but this method works for small environments as it
requires lots of manual actions and is error prone.

--------------
Upgrade impact
--------------

None.

---------------
Security impact
---------------

None.


--------------------
Notifications impact
--------------------

None.


---------------
End user impact
---------------

User experience for installing maintenance updates on slave nodes nodes changes
significantly. Instead of executing mos_apply_mu.py script on Fuel master node
and manually restarting services on all Fuel slave nodes user shall upload
custom graph and execute it. Also custom graph engine allows us to see the
history with the statuses of every particular task in the each execution of the
graph.


------------------
Performance impact
------------------

None.


-----------------
Deployment impact
-----------------

None. This spec affects only post-deployment process.


----------------
Developer impact
----------------

None.


---------------------
Infrastructure impact
---------------------

A custom graph for applying MU should be added to fuel-misc package and stored
on a mirror.

For each MOS release should be created a file, which will contain information
about the latest MU available. These files should be published in the
`/mcv/mos/$mos_version/` folders on the `mirror.fuel-infra.org` [3]_ server and
named as `mu-version.json`. The publishing of a file will serve as a signal
that new MU is available.
The contents of files is a JSON-formatted data.
For example `/mcv/mos/8.0/mu-version.json`::

    {
        "id": 3,
        "title": "8.0-MU-3",
        "timestamp": 1467647277,
        "doc_link": "https://docs.mirantis.com/openstack/fuel/fuel-8.0/maintenance-updates.html"
    }

The fields ``id``, ``title`` and ``timestamp`` are mandatory, others are
optional. The ``timestamp`` field has the Epoch time-format. The ``id`` field
represents the number of the update in a sequence.

Such a file will be generated for every Maintenance Update when it will be
published allowing end-users to keep themselves informed. The creation of
files should be implemented as part of the MU-publisher job.

--------------------
Documentation impact
--------------------

New maintenance updates workflow shall be documented in respective section
of MOS documentation.

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:

| Sergii Rizvan <srizvan@mirantis.com>

Other contributors:

|  None.

Mandatory design review:

| Vitaly Sedelnik <vsedelnik@mirantis.com>
| Denis Meltsaykin <dmeltsaykin@mirantis.com>
| Oleg Gelbukh <ogelbukh@mirantis.com>
| Ilya Kharin <ikharin@mirantis.com>
| Alexey Shtokolov <ashtokolov@mirantis.com>
| Vladimir Kuklin <vkuklin@mirantis.com>
| Sergii Golovatiuk <sgolovatiuk@mirantis.com>
| Alex Schultz <aschultz@mirantis.com>


Work Items
==========

* Write a custom graph for MU.
* Add the custom graph into the `fuel-misc` package and place the packet
  on a mirror.
* Implement the ``updates check installed``, ``updates check available``
  and ``updates install`` commands in `python-fuelclient`.
* Implement updates installation with a custom graph in the `fuel-qa`
  framework.


Dependencies
============

None.

-----------
Testing, QA
-----------

Applying updates in the QA frameworks should be used with executing
this custom graph.


Acceptance criteria
===================

Maintenance updates could be installed using custom deployment graph
via executing Fuel CLI commands.


----------
References
----------

.. [0] https://docs.mirantis.com/openstack/fuel/fuel-master/reference-architecture.html#task-based-deployment
.. [1] https://raw.githubusercontent.com/Mirantis/tools-sustaining/master/scripts/mos_apply_mu.py
.. [2] https://docs.mirantis.com/openstack/fuel/fuel-8.0/maintenance-updates.html#mu8-0-how-to-update
.. [3] http://mirror.fuel-infra.org/
