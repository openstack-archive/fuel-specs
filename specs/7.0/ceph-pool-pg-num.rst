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
    
    PG_COPY_PER_OSD = 400
    POOL_WEIGHT = {
        'cinder-volumes': 16,
        'cinder-backup': 4,
        '.rgw.buckets': 4,
        'ephemeral-vms': 2,
        'glance-images': 1
    }

    def to_upper_power_two(val):
        val_log2_f = math.log(val) / math.log(2)
        val_log2 = int(val_log2_f)
        if val_log2_f - val_log2 > 1E-2:
            val_log2 += 1
        return 2 ** val_log2
        return 2 ** val_log2

    def get_pool_pg_count(osd_count, pool_sz, use_rgw, use_ephemeral, use_glance):
        TOTAL_PG_COUNT = PG_COPY_PER_OSD / pool_sz * osd_count
        
        large_pools = ['cinder-volumes', 'cinder-backup']
        small_pool_count = 0
        
        if use_rgw:
            small_pool_count = 14
            large_pools.append('.rgw.buckets')
        
        if use_ephemeral:
            large_pools.append('ephemeral-vms')
        
        if use_glance:
            large_pools.append('glance-images')
                
        osd_count = float(osd_count)
        default_size = to_upper_power_two(osd_count)

        total_w = sum(POOL_WEIGHT[pool] for pool in large_pools)
        small_pools_pgs = default_size * small_pool_count
        pg_per_weight = (TOTAL_PG_COUNT - small_pools_pgs) / total_w
        
        res = {'default': default_size}
        for pool in large_pools:
            res[pool] = to_upper_power_two(POOL_WEIGHT[pool] * pg_per_weight)
        
        return res


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


