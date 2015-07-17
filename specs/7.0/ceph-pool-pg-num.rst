..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Values for pool placement groups number parameters
==========================================

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

Taking into consideration that it is much easier to increase pg num
values for existing pools (pg splitting is supported) than decreasing
them (currently pg merging is not supported, so the only way is to
recreate the pool and copy data), it is much better if we
underestimate the parameters than overestimate.

Example of 6.1 cluster:

    # ceph -s
    cluster 94c5c093-b867-4611-9d61-1729f2b7f502
     health HEALTH_WARN noout flag(s) set
     monmap e1: 1 mons at {node-1=192.168.0.4:6789/0}, election epoch 2, quorum 0 node-1
     osdmap e113: 21 osds: 21 up, 21 in
            flags noout
      pgmap v188192: 9714 pgs, 12 pools, 202 GB data, 52002 objects
            652 GB used, 3447 GB / 4099 GB avail
                9714 active+clean
    client io 23314 B/s rd, 0 B/s wr, 37 op/s

    9714 / 21 * 3 == 1388 PG copy per OSD

Proposed change
===============

Calculate pg number parameters taking into consideration number of
pools that are going to be created and their typical usage. Use
different pg_num parameters for openstack and rgw pools.

The nailgan should calculate and provide to deploy (puppet) the
following parameters:

 * storage[pg_num] (already exists, but should be calculated using the
   new formula)
 * storage[images_pg_num]
 * storage[volumes_pg_num]
 * storage[compute_pg_num]
 * storage[backups_pg_num]

When creating openstack pools, instead of osd_pool_default_pg_num, us
osd_pool_{images,volumes,compute,backups}_pg_num parameters.

The rados gateway will continue to use osd_pool_default_pg_num
parameters taken from storage[pg_num] and stored in ceph.conf, but
calculated using the new formula.

In fuel-library the following changes are supposed:

In deployment/puppet/osnailyfacter/modular/ceph/ceph_pools.pp: use
storage[${pool}_pg_num] parameter instead of storage[pg_num].

PG calculation formula:

Next requirements shloud be met for calculated PG counts (lower rules has less
power):

* PG per OSD shold be in range [200, 500]
* As cluster may grows algorithm should takes value near to upper bound
* results should be close to ceph.com/pgcalc/
* Each pool shold have not less that one PG copy on each OSD
* PG count for pool should be proportional to IO activity and data size in
  selected pool. Writes generate pool_sz more activity than reads.
* cinder-volumes get the most load with a lot of writes
* cinder-backup, .rgw.buckets and glance-images get read-only load most of the
  time
* ephemeral-vms get some load as well, but mostly reads
* rest pools requires minimal amount of PG

Algorithm:

* Estimated total amount of PG copyes calculated as (OSD * PG_COPY_PER_OSD),
  where PG_COPY_PER_OSD == 400 for now
* Each small pool get one PG copy per OSD. Means (OSD / pool_sz) groups
* All the rest PG are devided between rest pools, proportional to it's
  weights. By default next weights is used:

    POOL_WEIGHT = {
        'cinder-volumes': 16,
        'cinder-backup': 4,
        '.rgw.buckets': 4,
        'ephemeral-vms': 2,
        'glance-images': 1
    }

* Each PG count is rounded to next power of 2 value


Pseudocode:

    PG_COPY_PER_OSD = 400
    POOL_WEIGHT = {
        'cinder-volumes': 16,
        'cinder-backup': 4,
        '.rgw.buckets': 4,
        'ephemeral-vms': 2,
        'glance-images': 1
    }

    def to_upper_power_two(val, threshold=1E-2):
        val_log2_f = math.log(val, 2)
        val_log2 = int(val_log2_f)
        if val_log2_f - val_log2 > threshold:
            val_log2 += 1
        return 2 ** val_log2

    def get_pool_pg_count(osd_count, pool_sz, use_rgw, use_ephemeral, use_glance):
        osd_count = float(osd_count)
        TOTAL_PG_COUNT = float(PG_COPY_PER_OSD) / pool_sz * osd_count

        large_pools = ['cinder-volumes', 'cinder-backup']

        if use_rgw:
            small_pool_count = 14
            large_pools.append('.rgw.buckets')
        else:
            small_pool_count = 0

        if use_ephemeral:
            large_pools.append('ephemeral-vms')

        if use_glance:
            large_pools.append('glance-images')

        default_size = to_upper_power_two(osd_count / pool_sz)

        total_w = sum(POOL_WEIGHT[pool] for pool in large_pools)
        pg_per_weight = (TOTAL_PG_COUNT
                         - default_size * small_pool_count) / total_w

        res = {'default': default_size}
        for pool in large_pools:
            res[pool] = to_upper_power_two(POOL_WEIGHT[pool] * pg_per_weight)

        return res

Calc examples:
  osd_count=20.0, pool_sz=3, use_rgw=True, use_ephemeral=True, use_glance=True
  {'.rgw.buckets': 512,
   'cinder-backup': 512,
   'cinder-volumes': 2048,
   'default': 8,
   'ephemeral-vms': 256,
   'glance-images': 128}
  PG copy per OSD = 529.2 , pool count = 13
  Currently we have >1300.0 PG copy per OSD

  osd_count=200.0, pool_sz=3, use_rgw=True, use_ephemeral=True, use_glance=True
  {'.rgw.buckets': 4096,
   'cinder-backup': 4096,
   'cinder-volumes': 16384,
   'default': 128,
   'ephemeral-vms': 2048,
   'glance-images': 1024}
  PG copy per OSD = 432.0 , pool count = 13
  Currently we have >1300.0 PG copy per OSD

  osd_count=40.0, pool_sz=2, use_rgw=False, use_ephemeral=False, use_glance=False
  {'cinder-backup': 2048, 'cinder-volumes': 8192, 'default': 32}
  PG copy per OSD = 513.6 , pool count = 2
  Currently we have >200.0 PG copy per OSD

  osd_count=100.0, pool_sz=2, use_rgw=True, use_ephemeral=False, use_glance=True
  {'.rgw.buckets': 4096,
   'cinder-backup': 4096,
   'cinder-volumes': 16384,
   'default': 64,
   'glance-images': 1024}
  PG copy per OSD = 523.52 , pool count = 12
  Currently we have >1200.0 PG copy per OSD

  osd_count=21.0, pool_sz=3, use_rgw=True, use_ephemeral=False, use_glance=True
  {'.rgw.buckets': 512,
   'cinder-backup': 512,
   'cinder-volumes': 2048,
   'default': 8,
   'glance-images': 128}
  PG copy per OSD = 467.428571429 , pool count = 12
  Currently we have >1200.0 PG copy per OSD


Fither improvements:
* allow user to setup final cluster size
* allow user to setup weight per main pools


Alternatives
------------

Data model impact
-----------------

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


Dependencies
============

Testing
=======

Acceptance criteria
-------------------

Documentation Impact
====================

References
==========


