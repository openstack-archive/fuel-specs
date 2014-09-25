..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
 DevOps: Create script to reproduce environment for using VMware vCenter and NSX
==========================================

https://blueprints.launchpad.net/fuel/+spec/env-assist.py

We need a script for revert environment (including remotely runned on
virtalbox VMware vCenter and NSX nodes) before system test and making
snapshot after them. Also this script will be used for making enironment
manually.

Problem description
===================

Working with VMware technology (vCenter or NSX) required using two nodes:
one for qemu and one for virtualbox. There is tagged traffic betwen them.
And if we want make (system or manual) test we must do some operations for
revert vCenter node, make tagged interface, configure bridges and so on.
It is not comfortable and we want automatize this.
 
Proposed change
===============

For negotiation this troubles will be writed a script 'env_assist.py' which
will do all works. The script will provide the decorator with_env, which take
a environment as a parameter and revert it around tests. And sytem tests must 
be defined with it:

.. code-block:: python
    @with_env
    def test(env):
	...
	...

and launched with environment-argument:

.. code-block:: python
    env = getenv(env-name)
    test(env)

In this case env-name is a name of environment which described in file
/etc/env_assist.json. It has a structure like this:
.. code-block:: json
    {
        "env_Ubuntu_vcenter_ha": {
		"env-name": "env_Ubuntu_vcenter_ha",
		"nsxbr": {"ip": "172.16.0.1", "br": ""},
		"snp": {
		    "q": ["qemu:///system", 3, "ready_with_3_slaves"],
		    "vb": [
		        [
			"vbox@tpi85.bud.mirantis.net",
			"vcenter",
			"vcentersnap"
			],
			[
			"vbox@tpi85.bud.mirantis.net",
			"nsx",
			"nsxsnap"
			]
		    ]
		},
		"vlanifs": ["eth1.851", "eth1.852"],
		"br_private": "private",
		"br_public": "public"
	},
	"env_Ubuntu_vcenter_simple": {
		"env-name": "env_Ubuntu_vcenter_simple",
		"nsxbr": {"ip": "172.16.0.1", "br": ""},
		"snp": {
		    "q": ["qemu:///system", 7,  "ready_with_7_slaves"],
		    "vb": [
		        [
			"vbox@tpi85.bud.mirantis.net",
			"vcenter",
			"vcentersnap"
			],
			[
			"vbox@tpi85.bud.mirantis.net",
			"nsx",
			"nsxsnap"
			]
		    ]
		    },
		    "vlanifs": ["eth1.853", "eth1.854"],
		    "br_private": "private",
		    "br_public": "public"
	}
    }

Name of the environment could be passed by environment variable from jobs or
as command line argument or any another way if we use this script as pythonic
library.

Alternatives
------------

None

Data model impact
-----------------

None

REST API impact
---------------

None

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

None

Performance Impact
------------------

None

Other deployer impact
---------------------

It is necessary to install some pythonic library before using this script.

Developer impact
----------------

None

Implementation
==============

Assignee(s)
-----------
Primary assignee:
  gcon-monolake

Other contributors:
  igajsin

Work Items
----------

Dependencies
============

This libraries must be installed on node:
* libvirt
* pynetlinux



Testing
=======

Documentation Impact
====================


References
==========

