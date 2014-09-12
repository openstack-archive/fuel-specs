..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Support user-defined DNS and NTP
==========================================

https://blueprints.launchpad.net/fuel/+spec/external-dns-ntp-support

Nodes that deployed by Fuel should support user-defined DNS and NTP settings.

Problem description
===================

After deployment today we have hard-coded DNS and NTP fields on all nodes that
referred to master node. So if master node will not have internet access to NTP
servers that ships by default with ISO or if master node will disabled after
deployment then all nodes can have wrong time. It's right for DNS also.
Moreover, usually companies have internal NTP servers to sync over and internal
DNS to work over, but now user can't provide them to Fuel for slave nodes.

Proposed change
===============

Provide ability to change NTP and DNS servers for nodes through Fuel UI.
We can do it relatively simply by adding appropriate fields for external
DNS and NTP servers, then forward data from that fields to astute.yaml,
transfer it to nodes and apply data on nodes.

Scheme how it works today:

    ::

                            Fuel Master

                            +----------+
                            |NTP Client|
        Custom              +----------+            Fuel node
                                  ^
     +----------+           +-----+----+           +----------+
     |NTP Server+---------->|NTP Server+---------->|NTP Client|
     +----------+           +----------+           +----------+

     +----------+           +----------+           +----------+
     |DNS server+---------->|DNS server+---------->|DNS Client|
     +----------+           +-----+----+           +----------+
                                  v
                            +----------+
                            |DNS Client|
                            +----------+

Scheme how it can work after:

    ::

           Fuel Master
           +----------+
           |NTP Client|
           +----------+         Custom
                 ^
           +-----+----+      +----------+
           |NTP Server|<-----+NTP Server+--+
           +----------+      +----------+  |
                                           +------------+
           +----------+      +----------+  |            |
           |DNS server|<-----+DNS server+--+            |
           +-----+----+      +----------+               |
                 v                                      |
           +----------+                                 |
           |DNS Client|                                 |
           +----------+                                 |
                                                        |
                                        Controllers     |
                           +-----------+----------+-----v-----+
            Fuel node      |           |Controller|           |
           +----------+    |           |          |           |
           |NTP Client|<-+ |           |NTP Server|           |
           +----------+  | |VIP-Router |          | VIP-Router|
                         +-+Management |          |   Public  |
           +----------+  | |           |          |           |
           |DNS Client|<-+ |           |DNS server|           |
           +----------+    |           |          |           |
                           |           |          |           |
                           +-----------+----------+-----------+

Alternatives
------------

User can do all stuff about adding NTP and DNS records on all nodes
himself (manually).

  Pros:
    * We don't need to change any code at all.
  Cons:
    * It inconvinient, can lead to typo errors and, as result, to
      delay in work of all system.
    * If customer's ntp server will N/A for long time, time synchronization
      between controllers and computes will be lost. After this Nova will
      mark nodes with different time as failed. Openstack env starts spoiling

Data model impact
-----------------

Support to store external DNS&NTP fields in database required.

REST API impact
---------------

None

Upgrade impact
--------------

So as we don't have any implementation of major environments upgrade, we will
not support upgrade from old environments where we hadn't vrouter for external
DNS&NTP to new environment where we have one. Downgrade also will not support.

Security impact
---------------

None

Notifications impact
--------------------

None

Other end user impact
---------------------

None

Performance Impact
------------------

All DNS&NTP queries may be addressed to external servers, so how long they
will do right answer to that queries will depend from this servers settings.

Other deployer impact
---------------------

None

Developer impact
----------------

UI team will be affected, cause new UI options needed.
Maybe nailgun-related team is going to be affected to correctly put new values
from UI to database and from database to yaml

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  sbogatkin

Work Items
----------

#. Sync upstream puppet-ntp module

#. Adapt upstream module to Fuel

#. Write puppet manifest to provide ability change NTP and DNS adresses on
controllers

#. Write puppet manifest to provide ability change NTP and DNS adresses on
nodes

#. Add changes to UI and database

Dependencies
============

* https://blueprints.launchpad.net/fuel/+spec/virtual-router-for-env-nodes

Testing
=======

#. We need to build new fuel ISO and test if deployment work as expected.

#. We need to test how DNS&NTP will work with upstream external DNS&NTP
servers.

#. We need to test how NTP will work when upstream external NTP will disabled.
Nodes should sync with controller NTP anyway in that case.

Documentation Impact
====================

It should be described how to change DNS and NTP servers on nodes to external
and what exactly will be changed by this settings.

References
==========

None
