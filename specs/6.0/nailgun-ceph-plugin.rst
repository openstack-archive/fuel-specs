..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===================
Nailgun Ceph Plugin
===================

https://blueprints.launchpad.net/fuel/+spec/nailgun-ceph-plugin

Problem description
===================

We have Ceph support in Fuel core right now. As a first approach, we need
to move current implementation into separate plugin and it will serve as an
example of plugin approach in the future.

From Nailgun side plugin uses `Stevedore <http://stevedore.readthedocs.org/en/latest/>`_..
This package is already used in OpenStack Nova project as hooks providing
mechanism. It uses 'entry points' approach provided by setuptools/distutils,
which basically allows to lookup and execute code from Python packages
known to expose certain functionality.

Proposed change
===============

Plugin provides custom role in Nailgun, allowing to deploy Ceph on selected
nodes.


Alternatives
------------

None

Data model impact
-----------------

Plugin requires SQLAlchemy 0.9.4 to be able to work with PostgreSQL 9.3 and
JSON (those are required for PluginStorage).

PluginStorage is a DB table in PostgreSQL, which will be similar
to key-value storage (using native JSON field). This allows to store
any custom structures, also we won't have a headache with writing migrations.
In current approach, all Ceph-related data is stored in this "storage",
including custom role, volumes/partitions and so on. Nailgun executes code
from plugin through hooks and updates it's data by returned values.

REST API impact
---------------

API Serializers execute hooks while serializing DB model, extending JSON
with data returned from Ceph plugin. Hooks are added to certain fields only,
like "roles", "roles_metadata" and "volumes_metadata".

Previous version of Fuel already had Ceph support, so no real changes in API
will happen (unless plugin is removed, which is out of scope right now).

Ceph role is still in REST API, though it's provided by plugin now. Also
plugin provide custom partitions for both Ceph and Ceph journal (the same
were in core in previous version).

Currently plugin doesn’t extend wizard on UI, so radiobutton for Ceph is
left there as is. Still, plugin stores a flag in PluginStorage that Ceph was
enabled during environment creation.

Upgrade impact
--------------

Ceph plugin as any other Python plugin in closest future depends on new
versions of SQLAlchemy (>=0.9.4) and stevedore (>=0.14).
Ceph plugin itself is a Python package which will be packaged as an RPM
and updated correspondingly.
"Ceph" role will be excluded from list of roles in new release (no data
migration is required).

Plugin has to be tested and approved to work with each upcoming Fuel version.
Backward compatibility should also be provided, meaning code should work with
old environments on new Fuel version, if needed.

Security impact
---------------

None

Notifications impact
--------------------

None

Performance Impact
------------------

Performance might be decreased a little, but not really noticeable.
There is almost nothing we can do about that.

Other end user impact
---------------------

None

Other deployer impact
---------------------

Minimal size for Ceph partition equals to 3 Gb, for Ceph journal it defaults
to 0. Also, volume with id=‘image’ is removed on controllers and
'image_cache_max_size' parameter in node attributes is being set to 0.
Value of 'pg_num' for 'storage' section in environment attributes
is calculated from the number of Ceph partitions allocated on nodes
and 'osd_pool_size' parameter. By default pg_num=128.


Developer impact
----------------

All Nailgun-related data is stored inside config.yaml file, which has the same
format as we already have in openstack.yaml. Existing prototype is already
very close to be Nailgun Plugin. The only thing it requires is custom tab in
UI wizard, allowing to select Ceph as a storage type. Also it should be
packaged into an RPM and installed on Master node together with Nailgun in
the same container.

Implementation
==============

Assignee(s)
-----------

nmarkov@mirantis.com, akislitsky@mirantis.com

Work Items
----------

OSCI: RPM package should be built for Ceph plugin.
Fuel Python Team/UI Team: Plugin should provide custom tab/control in
UI wizard to enable Ceph storage type.
Fuel Python Team: The word "Ceph" shouldn't ever occur in Nailgun core.

Dependencies
============

None

Testing
=======

Ceph plugin includes unit tests written in Python using tox and unittests.
Some of them are inherited from built-in Nailgun classes. Ceph plugin tests
can be run separately from Nailgun tests.

Documentation Impact
====================

This spec describes plugin behavior. It doesn't change REST API or RPC format
and doesn't include additional documentation on these.

References
==========

None
