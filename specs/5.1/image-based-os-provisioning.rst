..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

================================================================
Substitution native OS installation process with image based one
================================================================

https://blueprints.launchpad.net/fuel/+spec/image-based-provisioning [1]_


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

As far as MOS has plenty of customizations even for core CentOS and Ubuntu
packages, we need to implement building bare OS images from scratch using
anaconda and debootstrap.
Those images are supposed to have cloud-init installed and we
suggest to use cloud-init built-in capabilities to install and configure
puppet and mcollective after first reboot.

In the future we'll use diskimage-builder to build custom OS images based on
those which are distributed by Canonical [2]_ and RedHat [3]_.
Openstack diskimage-builder is a community tool which is actively
developed and using this tool is potentially a great advantage.

Openstack Ironic nowadays seems to be mature enough to be used as a
provisioning tool instead of Cobbler. Ironic's scope, however, is strictly
limited to cloud environments. It is not going to support hardware without IPMI
as well as to support disk partitioning and other important stuff. Besides,
Ironic python agent and Ironic agent driver are not
production ready yet. As a result, we suggest to
implement disk image based provisioning process mostly on the agent
side fully independently on Ironic. It means we are going to implement our
own agent partly based on Ironic python agent. We also suggest to use Cobbler
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
  |           Provisioning config          |
  |             |             |            |
  |             | +---------> |            |
  |             |             |            |
  |           Launch provisioning          |
  |             |             |            |
  |             | +---------> |            |
  |             |             |            |
  |             |        Download image    |
  |             |             +            |
  |             |             |            |
  |             |        Partitioning      |
  |             |             +            |
  |             |             |            |
  |             |     Prepare configdrive  |
  |             |             +            |
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

- /opt/nailgun/bin/agent_new (discovery part)
- /opt/nailgun/bin/provision

Discovery part is supposed to be based on the code which is used as a discovery
extension in Ironic python agent. It uses dmidecode and other OS level
tools with no use of any third-party python libraries.

Discovery agent (agent_new) is not supposed to be run periodically by crond
daemon. Despite the fact that format of the discovery
data is not supposed to be changed, we suggest to continue
to use Ruby + Ohai based agent without any changes until we are sure that
new python based discovery agent (agent_new) is stable and works well.
The reason for that is that discovery agent is an extremely crucial part of
Fuel functionality. To make it possible to figure out whether the agent_new
works exactly the same way as the old one, we can organize launching two agents
and comparing their output. If it differs some way, we can report this fact on
the Fuel master node.

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

where user_data is supposed to be a multipart mime file [4]_.
This file will contain puppet and mcollective configurations as well as
the executable script implementing all that stuff which now exists
as a set of cobbler snippets [6]_.

Cloud-init should be configured so as to have so called NoCloud data source as
it's only data source (configdrive). Cloud-init configuration file example
is here [5]_.

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
partitioning related stuff will be encapsulated either into an image itself or
into the configuration stage (not provisioning stage). Ironic also is not going
to support OS agent based power management (only IPMI, ILO, DRAC, etc.) That is
why it is better to adderess those issues Fuel currently has that are related
to provisioning customizations independently on Ironic.

Placing partition table into an OS image is going to be a part of DIB
capabilities. Currently cloud OS image is just an image of root file system.
But what if OS image would be an image of a block device with partition table
inside it. It is possible if you use logical volumes which are unlike plain
primary partitions extendable. During image building you create logical volume
which suits exactly the size of unextended root file system and then after
reboot cloud-init will create other primary partitions, place there physical
volumes, attach those physical volumes to root volume group and then extend
root logical volume and extend root file system.

Data model impact
-----------------

* Discovery data format won't be changed.
* Serialized provisioning data format won't be changed.


REST API impact
---------------

None

Upgrade impact
--------------

This change assumes that in Cobbler bootstrap-2 distro and bootstrap-2 prfile
will be created. bootstrap-2 distro will be bound to initramfs containing
fuel_agent. This bootstrap-2 profile will be used for the default Cobbler
system. It is supposed that upgrade script will also put two bare OS
images to /var/www/nailgun so as to make provision agent able to download them.
It will be possible to use both native provisioning and image based
provisioning and to choose one of those two options by pointing out which
astute provisioning driver (cobbler or image) to use.

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

- Create make scripts for building bare OS images (Centos and Ubuntu)
  from scratch and for putting those images into ISO. (Iteration 1)
- Re-implement in terms of cloud-init all that stuff which is currently
  implemented in terms of Cobbler snippets. (Iteration 1)
- Create provisioning agent script. (Iteration 1)
    * partitioning
    * downloading and copying OS image
    * preparing and copying configdrive
- Testing and debugging. (Iteration 2)


Dependencies
============

None

Testing
=======

Testing approach

- Create VM or allocate hardware node.
- Deploy tftp + pxelinux and configure pxelinux with bootstrap ramdisk
  as a default item. Bootstrap ramdisk should contain provisioning script.
- Prepare a set of testing provisioning configurations similar to ones
  generated by provisioning serialier in nailgun.
- Run provision script with a set of different configurations one by one,
  comparing obtained state with required one.

Testing is supposed to be implemented according to this document [7]_

Acceptance criteria

- Two bare OS images built from scratch using MOS repositories must be
  available via http on Fuel master node
- After master node upgrade Cobbler must have one additional distro
  bootstrap-2 and one additional profile bootstrap-2 which are supposed to
  provide ramdisk with built-in fuel agent.
- It must be possible to choose one of two provisioning options "native" and
  "image based". It supposed to be configured using nailgun configuration file
  settings.yaml. By default "native" driver will be used.
- During image based provisioning fuel agent must make an appropriate
  partitioning scheme on a node according to the partitioning data, which is
  supposed to have the same format as it currently has.
- Once provisioning process is done, cloud-init must perform initial node
  configuration including at least but not limited to network, ssh,
  puppet and mcollective.


Documentation Impact
====================

It will be necessary to re-write those parts of Fuel documentation
which mention cobbler and provisioning.

References
==========

.. [1] https://blueprints.launchpad.net/fuel/+spec/image-based-provisioning
.. [2] http://cloud-images.ubuntu.com/
.. [3] http://openstack.redhat.com/Image_resources
.. [4] https://help.ubuntu.com/community/CloudInit
.. [5] http://bazaar.launchpad.net/~cloud-init-dev/cloud-init/trunk/view/head:/config/cloud.cfg
.. [6] https://etherpad.openstack.org/p/BOwAMY9pqy
.. [7] http://docs.mirantis.com/fuel-dev/devops.html