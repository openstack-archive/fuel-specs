..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

========================================
Collecting OpenStack Workload statistics
========================================

https://blueprints.launchpad.net/fuel/+spec/openstack-workload-statistics

We want to know how customers are using OpenStack, figure out behaviour
templates of customers.

Problem description
===================

We should collect OpenStack Workload (OSWL) statistics from the installed
environments, gather it and analyse. We should get not only the state of
the cloud/environments but also the way they change.
For example we should register adding, removing, modification of Virtual
Machines, Images, Volumes, etc.

We shouldn’t collect any private customer info, like image names,
volume names, IP addresses, user names, passwords, authentication and
authorization keys.

We should be able to extract and analyse collected info.

Proposed change
===============

OSWLs is split by the resource type:

- Virtual Machines
- Flavors
- Volumes
- Images
- Tenants

For collecting OSWLs, we should introduce fetchers for getting statistics from
the installed environment. Each fetcher gathers statistics for the specified
resource type. The statistics is saved into Nailgun DB. Collected
statistics is transmitted to the statistics collector only if sending of
statistics is enabled. OSWLs older than 2 weeks will be removed from the
Nailgun DB.

Fuel-stats servers perform receiving, saving and export to CSV of OSWLs.

Table 'oswl_stats' in the 'collector' database is used as OSWLs storage.
Fields of 'oswl_stats' are:

- id - identifier
- cluster_id - id of cluster object in the Naligun DD
- created_date - date of creation row in table
- resource_type - type of resource (vm, flavor, e.t.c)
- resource_data - JSON field for saving resource content:

    - current - list of current resources data
    - added - dict of added resources ids
    - modified - dict of modified resources ids
    - removed - dict of removed resources data

- resource_checksum - checksum of resource_data['current']
- is_sent - is info sent to collector or not

Strategy of saving OSWLs into Nailgun DB
----------------------------------------

- for each environment (cluster_id) and resource type we have single
  row per day
- on each fetch info from OpenStack we check if the resource is added,
  removed or modified:

    - in case of adding, resource details are stored into JSON field
      resource_data['current'] and resource uid is added to
      resource_data['added'] with time of adding
    - in case of deletion, resource should be moved from
      resource_data['current'] to resource_data['removed']
      with time of removal
    - in case of modification, new resource will be saved into the
      resource_data['current'], only diff of modified and old data,
      resource uid and modification time will be added into
      resource_data['modified']
    - resource_checksum - checksum of the serialized resource_data['current']
    - resource_checksum is changed on resource_data['current'] modification
    - if resource_checksum for cluster_id, resource_type is not changed at the
      next day - new row is not added into DB table.

Set of collected data
---------------------

+----------+--------------------------------------------------+---------------+
| Resource | Data                                             | Sync interval |
+==========+==================================================+===============+
| Flavor   | {"id": "dff5", "ram": 512, "vcpus": 1,           | 15 min        |
|          |  "swap": 128, "ephemeral": 0, "disk": 1}         |               |
+----------+--------------------------------------------------+---------------+
| Virtual  | {"id": '95f', "hostId": "6d5", "status": "ACT",  | 15 min        |
| Machine  |  "flavor_id": "f4e", "image_id": "95c",          |               |
|          |  "power_state": 1, "tenant_id": "ef7",           |               |
|          |  "created_at": '2015-01-14T13:22:35Z'}           |               |
+----------+--------------------------------------------------+---------------+
| Image    | {"id": "2de", "minDisk": 2, "minRam": 64,        | 15 min        |
|          |  "size": 13, "created": '2015-01-14T12:53:50Z',  |               |
|          |  "updated": '2015-01-14T12:53:52Z'}              |               |
+----------+--------------------------------------------------+---------------+
| Volume   | {"id": "de3", "availability_zone": "nova",       | 15 min        |
|          |  "encrypted_flag": False, "bootable_flag": True, |               |
|          |  "status": "st", "volume_type": "t", "size": 1,  |               |
|          |  "tenant_id": "fe63", "snapshot_id": "d3e"       |               |
|          |  "attachments": [{"device": "b",                 |               |
|          |   "server_id": "084", "id": "95}]}               |               |
+----------+--------------------------------------------------+---------------+
| Tenant   | {"id": "ge3", "enabled_flag": True}              | 15 min        |
+----------+--------------------------------------------------+---------------+
| Keystone | {"id": "kkt", "enabled_flag": True,              | 15 min        |
| User     |  "tenant_id": "x1_dd"}                           |               |
+----------+--------------------------------------------------+---------------+

Alternatives
------------

None

Data model impact
-----------------

DB tables for storing OSWLs should be added into Nailgun and fuel-stats.
New tables shouldn't affect already existing tables.

REST API impact
---------------

POST method for collecting OSWLs should be added into fuel-stats collector
at /api/v1/oswl_stats address.

Input is validated by JSON schema.
Normal http response codes: 200.
Expected error http response code: 400 - on schema validation error.

CSV export urls mapping:

- export OSWLs to CSV: /api/v1/csv/{resource_type},
- export clusters info: /api/v1/csv/clusters,
- export plugins info: /api/v1/csv/plugins,
- export all CSVs as zip archive: /api/v1/csv/all

All CSV export urls handle filtering parameters from_date, to_date in
format 'YYYY-MM-DD'.

Upgrade impact
--------------

None

Security impact
---------------

None

Notifications impact
--------------------

None


Other end user impact
---------------------

Performance Impact
------------------

Nailgun:

- Increases load on the Fuel Master node - OSWLs fetchers
  processes will be added
- Increases sending statistics duration to collector.
- Slightly increases DB size.

Fuel-stats:

- Increases load of fuel-stats collector.
- Increases load of fuel-stats analytics.
- Increases DB size.

Other deployer impact
---------------------

None


Developer impact
----------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:

- Aleksey Kasatkin (akasatkin@mirantis.com)
- Artem Roma (aroma@mirantis.com)
- Alexander Kislitsky (akislitsky@mirantis.com)

Other contributors:

- Nathan Trueblood <ntrueblood@mirantis.com> PM
- Andrey Sledzinskiy <asledzinskiy@mirantis.com> QA
- Anastasia Palkina <apalkina@mirantis.com> QA
- Maksym Strukov <mstrukov@mirantis.com> QA
- Alexander Charykov <acharykov@mirantis.com> DevOps
- Dmitry Kaiharodsev <dkaiharodsev@mirantis.com> OSCI
- Evgeny Konstantinov <evkonstantinov@mirantis.com> TW

Work Items
----------

- Nailgun OSWLs fetchers. OSWLs should be split by resource types.
- Saving OSWLs to the DB. Saving should be efficient in terms of disk space.
- Sending OSWLs to the fuel-stats collector. Sending should send only
  new or modified records.
- Saving OSWLs at fuel-stats collector side.
- Export OSWLs to the CSV.
- Backup of fuel-stats DB.

Dependencies
============

None

Testing
=======

Check items:

- OSWLs are stored in the Nailgun DB.
- All required OSWLs items are stored in the Nailgun DB.
- OSWLs sent to the fuel-stats only if sending enabled.
- OSWLs stored in the fuel-stats DB.
- All required OSWLs items are stored in the fuel-stats DB.
- OSWLs is exported to CSV.
- All required OSWLs items are exported into the CSV.
- System test for check collecting of resources, sending and saving them
  into collector DB will be created.

Performance testing:

- Check Nailgun performance shouldn't affected by OSWLs processing.
- Measure fuel-stats collector degradation after OSWLs will be introduced.
- Measure growth of DB.

Documentation Impact
====================

- Nailgun part of OSWLs collecting, storing, sending.
- Fuel-stats part of OSWLs collecting, storing, exporting.

References
==========

None
