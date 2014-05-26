..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

================================================================
Substitution native OS installation process with image based one
================================================================

https://blueprints.launchpad.net/fuel/+spec/image-based-provisioning


Problem description
===================

First, we use plenty of customizations of OS installation process. It is not
always possible to customize native OS installers such as debian-installer and
anaconda on that level of customization we need. Besides, supporting
customizations requires engineering resources. If you need to support
just one set of customization scripts instead of two completely different
sets of customizations for anaconda and debian-installer, it requires
2 times less of engineering resources.

Second, assembling root file system from scratch on every node during OS
provisioning takes a lot of time. It is much more effective to build OS root
filesystem just once and then copy it thoughout nodes. It is going to take up
to 10 times faster than installation process using so called native installers.


Proposed change
===============

The first aspect of the issue is going to be addressed by implementing fully
customizable and extremely simple python script which is supposed to be both
a discovery agent (currently written in Ruby) and an installation agent which
will do nothing more than making disk partitions, retrieving OS root filesystem
image and copying it on a hard drive.

On the other hand, it is supposed to use diskimage-builder to build custom OS
images based on those which are distributed by
Canonical (http://cloud-images.ubuntu.com/) and
RedHat (http://openstack.redhat.com/Image_resources). It is again much more
effective to use a tool which is actively developed and supported by Openstack
community.

Openstack Ironic nowadays seems to be mature enough to be used as a
provisioning tool instead of cobbler. Ironic's scope, however, is strictly
limited to cloud environments. It is not going to suppord hardware without IPMI
it is not going to support disk partitioning, etc. Besides, ironic python agent
and ironic agent driver are not production ready yet. As a result, we
suggest to implement disk image based provisioning process mostly on the agent
side fully independently on ironic. It means we are going to implement our
own agent partly based on ironic python agent. We also suggest to use Cobbler
as a tool for managing tftp and dhcp services but not for
templating kickstarts.

As far as we are going to use our own OS installation agent and this agent is
supposed to be extremely simple, we don't need to reboot a node before
provisioning as well as we don't need Cobbler capabilities to boot nodes
with different profiles. Discovery/Installation flow diagram is

Nailgun       Astute       Agent        Cobbler
  +             +             +            +
  |             |             |  PXE boot  |
  |             |             |            |
  |             |             | <--------+ |
  |             |             |            |
  |     Discovery data        |            |
  |             |             |            |
  | <-----------------------+ |            |
  |             |             |            |
  | Provision task            |            |
  |             |             |            |
  | +---------> |             |            |
  |             |             |            |
  |           Launch provisioning          |
  |             |             |            |
  |             | +---------> |            |
  |             |             |            |
  |   Provisioning data       |            |
  |             |             |            |
  | +-----------------------> |            |
  |             |             |            |
  |           Finish provisioning          |
  |             |             |            |
  |             | <---------+ |            |
  |             |             |            |
  |             |   Disable PXE boot       |
  |             |             |            |
  |             | +----------------------> |
  |             |             |            |
  |             |  Reboot     |            |
  |             |             |            |
  |             | +---------> |            |
  |             |             |            |
  | Provisioning task finished|            |
  |             |             |            |
  | <---------+ |             |            |
  +             +             +            +



Images for provisioning will be built during the ISO building stage by
`disk-imagebuilder` and stored somewhere in ISO. Thus, ISO's size increasing is
expected.

Alternatives
------------

None

Data model impact
-----------------

* We need to re-implement nailgun volume manager in order to make it more
 understandable and maintainable. We suggest the following format for
 partitioning data
    [
      {
        "uspec": {
          "DEVNAME": "/dev/sda",
          "ID_SERIAL": "DISKSERIAL",
          "ID_WWN": "DISKWWN",
          "DEVTYPE": "disk",
          "DEVPATH": "/devices/pci0000:00/0000:00:0d.0/host2/target2:0:0/2:0:0:0/block/sda",
          "DEVLINKS": ["/dev/block/8:0", "/dev/disk/by-id/DISKID", "/dev/disk/by-path/DISKPATH"]
        },
        "type": "disk",
        "table": "msdos",
        "scheme_id": 0,
        "partitions": [
          {"size": 1024, "type": "primary", "flags": ["boot"], "scheme_id": 1},
          {"minsize": 10240, "maxsize": 102400, "priority": 20, "type": "primary", "flags": [], "scheme_id": 2},
          {"minsize": 20480, "maxsize": "grow", "priority": 10, "type": "logical", "flags": [], "scheme_id": 3}
        ]
      },
      {
        "uspec": {
          "DEVNAME": "/dev/sdb",
          ...
        },
        "type": "disk",
        "table": "gpt",
        "scheme_id": 4,
        "partitions": [
          {"size": 1024, "type": "primary", "flags": ["boot"], "scheme_id": 5},
          {"minsize": 0, "maxsize": "grow", "priority": 100, "type": "primary", "flags": [], "scheme_id": 6}
        ]
      },
      {
        "uspec": {
          "DEVNAME": "/dev/sdc",
          ...
        }
        "type": "disk",
        "scheme_id": 7
      },
      {
        "type": "md",
        "level": "mirror",
        "devices": [1, 5],
        "spare": [7],
        "scheme_id": 8
      },
      {
        "type": "pv",
        "device": 2
        "scheme_id": 9
      },
      {
        "type": "pv",
        "device": 3,
        "scheme_id": 10
      },
      {
        "type": "vg",
        "name": "myvg"
        "pvs": [9, 10],
        "scheme_id": 11
      },
      {
        "type": "lv",
        "vg": "myvg",
        "size": 4096,
        "scheme_id": 12
      },
      {
        "type": "mount_point",
        "mount_to": "/",
        "device": 12
        "scheme_id": 13
      },
      {
        "type": "mount_point",
        "mount_to": "/var",
        "device": 3
        "scheme_id": 14
      }
    ]





REST API impact
---------------

* Discovery part of the agent is supposed to be implemented so as to send
 data in the same format as they are currently sent by the discovery agent.
 No changes.
* Installation part of the agent needs to be able to get provisioning data
 (image url, partitioning data, other data) from a master node via HTTP.
 Format of the data is as follows

 {
    "cloud-init": {
        "mco": {
            "pskey": "mco_pskey",
            "vhost": "mco_vhost",
            "host": "mco_host",
            "user": "mco_user",
            "password": "mco_password",
            "connector": "mco_connector",
            "enable": 1
        },
        "pappet": {
            "auto_setup": 1,
            "master": "puppet_master_host",
            "enable": 0,
        }
        "ssh": {}
    }
    "partitions":
 }


Security impact
---------------

None

Notifications impact
--------------------

None

Other end user impact
---------------------

The final ISO should contain at least of 2 images with bare system (Ubuntu & CentOS).
So the overall size will be about 500-700 MB bigger than now.
#TODO(agordeev): fill with more precious information about increased size

Performance Impact
------------------

None

Other deployer impact
---------------------

None

Developer impact
----------------

None

Implementation
==============

To the purpose of image based provisioning there's a need of caching images
somewhere in ISO. At least 2 images expected: Ubuntu and CentOS. Image will be
created at ISO building stage by executing `disk-imagebuilder`. Also that
leads to having an additional directory in `fuel-main` repo with Makefile and scripts.

Assignee(s)
-----------

Primary assignee:
  <vkozhukalov@mirantis.com>


Work Items
----------

None

Dependencies
============

`disk-imagebuilder`
'CentOS' bare image
'Ubuntu' bare image

Testing
=======

None

Documentation Impact
====================

None

References
==========

* [1] https://blueprints.launchpad.net/fuel/+spec/image-based-provisioning
