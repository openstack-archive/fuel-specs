..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==================================================
Values for pool placement groups number parameters
==================================================

https://blueprints.launchpad.net/fuel/+spec/ceph-osd-pool-default-pg-num

Currently Fuel creates Ceph clusters with overestimated number of
placement groups, which causes issues both on deployment steps and
when the cluster is used. This should be fixed.

Problem description
===================

Fuel sets the following placement group parameters in ceph.conf

  osd_pool_default_pg_num
  osd_pool_default_pgp_num

using the formula:

  Nearest power of 2 (num_of_OSDs * 100 / num_of_replica)

This values are used:

* by puppet when creating openstack pools (images, volumes, compute,
  backups);
* by rados gateway, when creating rgw pools (.rgw.root, .rgw.control,
  .rgw, .rgw.gc, .users.uid).

This formula is correct only for clusters with one pool. For clusters
with many pools it overestimate the number of placement groups by the
number of the pools times (the goal is to have 100 placement groups
per osd or a little high).

As it is unknown how the user plans to use the cluster, it is not
possible to calculate the value correctly. Still we need to change the
current calculations, because large amount of placement groups per osd
leads to long peering times after any changes to the cluster, during
this period operations that need data from peering placement groups
hang.

Example of 6.1 cluster::

    # ceph -s
    cluster 94c5c093-b867-4611-9d61-1729f2b7f502
     health HEALTH_WARN noout flag(s) set
     monmap e1: 1 mons at {node-1=192.168.0.4:6789/0}, election epoch 2,
     quorum 0 node-1
     osdmap e113: 21 osds: 21 up, 21 in
            flags noout
      pgmap v188192: 9714 pgs, 12 pools, 202 GB data, 52002 objects
            652 GB used, 3447 GB / 4099 GB avail
                9714 active+clean
    client io 23314 B/s rd, 0 B/s wr, 37 op/s

    9714 / 21 * 3 == 1388 PG copy per OSD

Proposed change
===============

The code shold have a flag to simulate current behaviour.

Calculate pg number parameters taking into consideration number of
pools that are going to be created and their typical usage. Use
different pg_num parameters for openstack and rgw pools.

The nailgan should calculate and provide to deploy (puppet) the
following parameters:

* storage[pg_num] (already exists, but should be calculated using the
  new formula)
* storage[per_pool_pg_nums] - dictionary, which maps pool name to PG
  count for those pools, which uses PG count, different from storage[pg_num]

When creating openstack pools, instead of osd_pool_default_pg_num, use
storage[per_pool_pg_nums][${pool}] parameters, if set.

The rados gateway will continue to use osd_pool_default_pg_num
parameters taken from storage[pg_num] and stored in ceph.conf, but
calculated using the new formula, except for .rgw pool.

In fuel-library the following changes are supposed:

In deployment/puppet/osnailyfacter/modular/ceph/ceph_pools.pp: use
storage[per_pool_pg_nums][${pool}] parameter instead of storage[pg_num].

PG calculation formula:

Next requirements should be met for calculated PG counts (lower rules have
less power):

* PG per OSD shold be less than 300
* No pool should gets less PG, that some preselected amount (64 for now),
  also each pool shold have not less that one PG copy on each OSD
* As cluster may grows algorithm should takes value near to upper bound
* results should be close to ceph.com/pgcalc/
* PG count for pool should be proportional to IO activity and data size in
  selected pool. Writes generate pool_sz more activity than reads.
* cinder-volumes get the most load with a lot of writes
* cinder-backup, .rgw.buckets and glance-images get read-only load most of the
  time
* ephemeral-vms get some load as well, but mostly reads
* rest pools require minimal amount of PG

Algorithm:

* Estimated total amount of PG copies calculated as (OSD * PG_COPY_PER_OSD),
  where PG_COPY_PER_OSD == 200 for now
* Each small pool get one PG copy per OSD. Means (OSD / pool_sz) groups
* All the rest PG are devided between rest pools, proportional to their
  weights. By default next weights are used:::

    volumes - 16
    compute - 8
    backups - 4
    .rgw - 4
    images - 1

* Each PG count is rounded to next power of 2

Calc examples:::

  osd_count=3, pool_sz=3, use_volumes=True objects_ceph=True,
  ephemeral_ceph=True, images_ceph=True
  {'.rgw': 64,
   'backups': 64,
   'compute': 64,
   'images': 64,
   'pg_num': 64,
   'volumes': 64}
  PG copy per OSD = 640 , pool count = 9
  Currently we have 1365 PG copy per OSD

  osd_count=20, pool_sz=3, use_volumes=True objects_ceph=True,
  ephemeral_ceph=True, images_ceph=True
  {'.rgw': 256,
   'backups': 256,
   'compute': 512,
   'images': 64,
   'pg_num': 64,
   'volumes': 1024}
  PG copy per OSD = 364 , pool count = 9
  Currently we have 1638 PG copy per OSD

  osd_count=200, pool_sz=3, use_volumes=True objects_ceph=True,
  ephemeral_ceph=True, images_ceph=True
  {'.rgw': 2048,
   'backups': 2048,
   'compute': 4096,
   'images': 512,
   'pg_num': 128,
   'volumes': 8192}
  PG copy per OSD = 263 , pool count = 9
  Currently we have 1310 PG copy per OSD

  osd_count=40, pool_sz=2, use_volumes=True objects_ceph=False,
  ephemeral_ceph=False, images_ceph=False
  {'.rgw': 64,
   'backups': 1024,
   'compute': 64,
   'images': 64,
   'pg_num': 64,
   'volumes': 4096}
  PG copy per OSD = 281 , pool count = 9
  Currently we have 1638 PG copy per OSD

  osd_count=100, pool_sz=2, use_volumes=True objects_ceph=True,
  ephemeral_ceph=False, images_ceph=True
  {'.rgw': 2048,
   'backups': 2048,
   'compute': 64,
   'images': 512,
   'pg_num': 64,
   'volumes': 8192}
  PG copy per OSD = 263 , pool count = 9
  Currently we have 1310 PG copy per OSD

  osd_count=21, pool_sz=3, use_volumes=True objects_ceph=True,
  ephemeral_ceph=False, images_ceph=True
  {'.rgw': 256,
   'backups': 256,
   'compute': 64,
   'images': 64,
   'pg_num': 64,
   'volumes': 1024}
  PG copy per OSD = 283 , pool count = 9
  Currently we have 1560 PG copy per OSD

Futher improvements:
* allow user to setup final cluster size
* allow user to setup weight per main pools


Alternatives
------------

Data model impact
-----------------

Additional dictionary per_pool_pg_nums would be add to astute.yaml to
storage dict::

  attrs['storage']['per_pool_pg_nums'] -- dict {pool_name: pool_pg_count}


REST API impact
---------------

Upgrade impact
--------------

Security impact
---------------

Notifications impact
--------------------

Other end user impact
---------------------

Performance Impact
------------------

This should improve repair and initiall peering speed.
Also resource consumption should be decreased.

In case if PG count for some pool would requires changes this
will rebalance all data in selected pool. Impact depends in
data size in pool.

Plugin impact
-------------

Other deployer impact
---------------------

Developer impact
----------------

Infrastructure impact
---------------------

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  kdanylov

Other contributors:
  mgolub

Mandatory design review:
  dborodanko, awoodwards, ashaposhnikov

Work Items
----------

* update fuel-library to use per-pool pg count instead of default
* update fuel-library to create .rgw pool explicitly, before start radosgw
* update fuel-web calculation algorithm for PG count
* update UI to allow user provide additional settings: final OSD count, pool
  weights

Dependencies
============

Testing
=======

This link 

http://cephnotes.ksperis.com/blog/2015/02/23/
get-the-number-of-placement-groups-per-osd
contains a script, which allows to find PG per pool and per OSD.

After deployment this script need to be run on any OSD node.
PG per OSD should not exceed 300. PG for particular pools should
match rules, described above.

The next check should be made with default PG count and new one:

* Ceph performance test
* Repair speed test
* Deployment test (time for cluster to finish initial peering)

Acceptance criteria
-------------------

Documentation Impact
====================

References
==========


