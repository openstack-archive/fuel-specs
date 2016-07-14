..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=======================================================================
Apply maintenance updates on slave nodes using default deployment graph
=======================================================================

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

Maintenance update installation could be performed by executing the predefined
default graph instead of using the `mos_apply_mu.py` [1]_ script and restarting
services manually.

Limitations: this spec covers only installation of the latest available
maintenance update (installation of specific maintenance update requires
more work and is out of scope of this spec).
Installation of the MU on custom, patched, unpredictable cluster configurations
and states is not supported. Fuel client should check these unsupported states
and configurations of a cluster with the `noop run of Fuel tasks` graph [5]_
and inform user that any customization may be lost during update and user
may apply installation of the MU on his own risk.


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

    fuel2 -> updates --env env_id ---> check
                                  |
                                  +--> install

The Fuel CLI command ``updates --env env_id check`` runs external tool `cudet`
that will check the version of the Maintenance Update applied (if any) by
checking the file `/etc/fuel/mu-version.json` which is delivered as a part of
the `fuel-misc` package to every node in the particular environment. In case of
absence `/etc/fuel/mu-version.json` file Fuel CLI will provide output that no MU
installed on the node. Also this command will check integrity of codebase of
a cluster and provide output with information about such customization.
The external utility will parse the contents of the file `mu-version.json`
in the appropriate sub-folder in `/mcv/mos/` on the official Fuel mirror
`mirror.fuel-infra.org` [4]_, then check its contents against the local file
`/etc/fuel/mu-version.json` on every node and show the user if there are new
updates available. If there is no local information to compare with, the case
should be treated as no Maintenance Update is currently installed. The tool
`cudet` will produce an extensive report in textual form.

Having this information the user may decide whether to apply a new update
using the command ``updates --env env_id install`` or it already has the needed
Maintenance Update installed.
The command ``updates --env env_id install`` will run the default deployment
graph for the selected environment using the latest versions of packages.
In case of successful installation of the Maintenance
Update its version and timestamp will be stored on each node locally as
`/etc/fuel/mu-version.json` to make further checks against the Fuel mirror
possible.

In case of failed installation operator should inspect logs and manually fix
all issues. Information about the states of every run of the MU installation
is stored in Nailgun database and operator can give access to this information
via Fuel CLI. Documentation about accessing such information via Fuel CLI
located here [6]_.


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
manually. This case described here at [3]_.
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

User experience for installing maintenance updates on slave nodes changes
significantly. Instead of executing `mos_apply_mu.py` [1]_ script
on Fuel master node and manually restarting services on all Fuel slave nodes
user can use Fuel CLI command ``updates --env env_id install`` for installation
of the MU. Additionally before installation user will be able to check
information about installed MU and available updates via the
``updates --env env_id check`` Fuel CLI command.
Also custom graph engine allows us to see the history with the statuses
of every particular task in the each execution of the graph.
Documentation about accessing such information via Fuel CLI located here [6]_.


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

For each MOS release should be created a file, which will contain information
about the latest MU available. These files should be published in the
`/mcv/mos/$mos_version/` folders on the `mirror.fuel-infra.org` [4]_ server and
named as `mu-version.json`. The publishing of a file will serve as a signal
that new MU is available.
The contents of files is a JSON-formatted data.
For example `http://mirror.fuel-infra.org/mcv/mos/9.0/mu-version.json`::

    {
        "id": 1,
        "title": "9.1",
        "timestamp": 1467647277,
        "doc_link": "https://docs.mirantis.com/openstack/fuel/fuel-9.0/maintenance-updates.html"
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

QA assignee:

| Artem Grechanichenko <agrechanichenko@mirantis.com>

Work Items
==========

* Implement the ``fuel2 updates --env env_id check`` and
  ``fuel2 updates --env env_id install`` commands in `python-fuelclient`.
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
.. [2] https://review.openstack.org/#/c/346119
.. [3] https://docs.mirantis.com/openstack/fuel/fuel-8.0/maintenance-updates.html#mu8-0-how-to-update
.. [4] http://mirror.fuel-infra.org/
.. [5] https://blueprints.launchpad.net/fuel/+spec/puppet-noop-run
.. [6] http://docs.openstack.org/developer/fuel-docs/userdocs/fuel-user-guide/maintain-environment/deployment-history.html
