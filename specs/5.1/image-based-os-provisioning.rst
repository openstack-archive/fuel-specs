..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

================================================================
Substitution native OS installation process with image based one
================================================================

https://blueprints.launchpad.net/fuel/+spec/image-based-provisioning [0]_


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
Canonical [1]_ and RedHat [2]_. It is again much more
effective to use a tool which is actively developed and supported by Openstack
community. However, as a zero step implementation we are not planning to
customize OS images at all. Those images already contain cloud-init and we
suggest to use cloud-init built-in capabilities to install and configure
puppet and mcollective after first reboot. DIB elements usually install
packages, but currently one can customize only apt based repositories.
Yum based repositories are still non-customizable. Source-repository element
allows one to choose between source repositories and packages by setting
corresponding environment variables. At the moment using vanilla images seems
to be appropriate.

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

::

  Nailgun       Astute        Agent        Cobbler
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

Our suggestion is to put all agent related code into fuel-web/fuel_agent
python package and implement discovery and provisioning parts independently as
two executable python scripts:

- /opt/nailgun/bin/agent (discovery part)
- /opt/nailgun/bin/provision

Discovery agent is supposed to be run periodically by crond daemon (exactly
as it works now). The format of discovery data is supposed not to be changed.

Provision script will be run using two mcollective agents uploadfile and
execute_shell_command. Uploadfile will prepare config file containing all those
data that are necessary for provisioning and come from provisioning serializer.
Provision script will make partitions according to configuration, download
OS image, copy it on a hard drive, prepare configdrive and copy
configdrive on a hard drive.

Configdrive is a set of configuration files for cloud-init. We assume puppet
and mcollective will be configured right after first reboot by cloud-init.
So, agent needs to be able to get parameters given in a serialized
provisioning data set and put them into a configdrive in the format that
cloud-init is able to read.

Configdrive is supposed to be put on a separate partition in the end of one of
hard drives on a node during provisioning stage. Configdirve is just a file
system which has at least the following structure

- openstack/latest/meta_data.json
- openstack/latest/user_data

where user_data is supposed to be a multipart mime file [3]_.
This file will contain puppet and mcollective configurations as well as
the executable script implementing all that stuff which now exists
as a set of cobbler snippets.

Cloud-init should be configured so as to have so called NoCloud data source as
it's only data source. Cloud-init config should enable at least the following
list of cloud init modules

- growpart
- resizefs
- TODO

and at least the following list of cloud config modules

- puppet
- mcollective

Cloud-init configuration file example is here [4]_.

Astute provision method will add node records into cobbler, but only to prevent
them to boot in bootstrap mode. Provision method should be re-written so as
to run provision script on nodes and provide this script with serialized
provisioning data generated by nailgun.


Alternatives
------------

Another possible way is to integrate Ironic into Fuel. Why not? Because Ironic
has a very specific scope which is more about cloud environments when a node
is provisioned and leased by a tenant for a while and then it is supposed to
be returned to repeat that cycle again. This very specific use case makes
Ironic tightly limited in its capabilities. For example, Ironic assumes all
partitioning related stuff will be encapsulated either into image itself or
into configuration stage (not provisioning stage). Ironic is not going to
support OS agent based power management (only IPMI, ILO, DRAC, etc.) That is
why it is better to solve those issues Fuel currently has that are related to
provisioning customizations.

Data model impact
-----------------

* Discovery data format won't be changed.
* Serialized provisioning data format won't be changed.


REST API impact
---------------

None

Security impact
---------------

None

Notifications impact
--------------------

None

Other end user impact
---------------------

Probably provisioning progress bar is better to be removed at all as it going
to take as much time as the reboot stage usually takes.

Performance Impact
------------------

Provisioning process is going to take much less time than it usually
takes at the moment.

Other deployer impact
---------------------

As far as we are going to include Ubuntu and Centos OS bare images into ISO,
it is going to become around 700M bigger.

Developer impact
----------------

Probably UI team cooperation will be necessary to remove provisioning
progress bar if it'll be appropriate.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  <vkozhukalov@mirantis.com>
  <agordeev@mirantis.com>


Work Items
----------

- Add DIB based targets into ISO build script for building golden bare
  OS images (Ubuntu and Centos).
- Write discovery agent script.
- Write provisioning agent script.
    * partitioning
    * downloading and copying OS image
    * preparing and copying configdrive


Dependencies
============

None

Testing
=======

Functional testing is supposed to follow these steps

- Create VM or allocate hardware node.
- Deploy tftp + pxelinux and configure pxelinux with bootstrap ramdisk
  as a default item. Bootstrap ramdisk should contain provisioning script.
- Prepare a set of testing provisioning configurations similar to ones
  generated by provisioning serialier in nailgun.
- Run provision script with a set of different configurations one by one,
  comparing obtained state with required one.


Documentation Impact
====================

It will be necessary to re-write those parts of Fuel documentation
which mention cobbler and provisioning.

References
==========

* [0] https://blueprints.launchpad.net/fuel/+spec/image-based-provisioning
* [1] http://cloud-images.ubuntu.com/
* [2] http://openstack.redhat.com/Image_resources
* [3] https://help.ubuntu.com/community/CloudInit
* [4] http://bazaar.launchpad.net/~cloud-init-dev/cloud-init/trunk/view/head:/config/cloud.cfg
