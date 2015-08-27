..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=======================================
Improved bootstrap images configuration
=======================================

https://blueprints.launchpad.net/fuel/+spec/fuel-bootstrap-on-ubuntu

Configure, rebuild, and switch between the (Ubuntu based) bootstrap images
using Fuel UI and CLI.

--------------------
Problem description
--------------------

At the moment customizing the bootstrap image is a complicated process.
Although the script_ which actually builds the image is quite flexible
customizing the image involves editing config files and running scripts
on the master node.

The second issue is that only one bootstrap image can exist. Having
multiple bootstrap images (say, normal, failsafe, test) would make
the operators' life much easier.

Therefore a proper Fuel CLI and web UI for configuring, rebuilding
and switching between bootstrap images is required.

----------------
Proposed changes
----------------

Extend nailgun to manage the bootstrap images and the related settings.
Add the web UI and CLI for configuring, building, and switching between
the bootstrap images.

Web UI
======

The following pages should be added:

* The list of bootstrap images. It's possible to select an image
  and set it as a current, or browse its detailed information.
* The image details page. Displays the current image information,
  makes it possible to reconfigure and rebuild the image.
* The global bootstrap related settings.


Nailgun
=======

Data model
----------

The following global settings will be added:

- The ID of the current bootstrap image
- Default Ubuntu and MOS (APT) repositories
- Extra (APT) repositories which should be used for every image
- Package pinning rules (repositories' priorities)
- Extra packages included into every image
- Public ssh keys included into every image
- Extra kernel modules included into initramfs of every image
- Extra udev rules which should be included into every image
- Default proxies for accessing the above repositories

The following per image settings will be added:

- Human readable name of the image
- Ubuntu and MOS APT repositories
- (APT) repositories which should be used for building an image
- Package pinning rules (repositories' priorities)
- Extra packages which should be included into the image 
- Public ssh keys included into every image
- Extra modules which should be included into initramfs
- Extra udev rules which should be included into the image
- HTTP/FTP/whatever proxies for accessing the repositores


REST API
--------

The following methods should be added:

* Query the list of bootstrap images
* Set an image as a current
* Rebuild the image
* Query/change image parameters
* Query/change the global bootstrap related parameters
* Add a new bootstrap image
* Remove the image

Orchestration
=============

TODO


RPC Protocol
------------

Astute needs to know the name of the cobbler profile which corresponds
to the current bootstrap image. Nailgun should pass this information
to astute.

Fuel Client
===========

TODO: describe CLI commands for
- querying the list of bootstrap images
- setting the image as a current
- querying/altering the global bootstrap settings
- querying/altering the per image settings
- rebuilding, adding, removing images
  
Plugins
=======

TODO: figure out if this affects plugins

Fuel Library
============

* Manifests which configure cobbler should be aware that there might be
  quite a number of bootstrap images and corresponding cobbler profiles

------------
Alternatives
------------

None

--------------
Upgrade impact
--------------

TODO: how to support old environments with static bootstrap image?

---------------
Security impact
---------------

TODO

--------------------
Notifications impact
--------------------

The following notification should be added:

- Building the default bootstrap image failed

---------------
End user impact
---------------

The user can customize the bootstrap images (include extra drivers, packages,
ssh keys, etc). This gives an extra flexibility but also gives more than enough
rope to hang yourself.

------------------
Performance impact
------------------

The deployed OpenStack nodes are not affected in any way.
The master node deployment will take a bit longer (5 -- 10 minutes)
due to the generation of the default bootstrap image.

-----------------
Deployment impact
-----------------

The default bootstrap image is generated after the master node deployment.
This process is supposed to work without any user intervention if the master
node has an access to the default Ubuntu_ and MOS_ mirrors. Otherwise
a warning is displayed in the UI and the user is redirected to configure
and build the default bootstrap image.

----------------
Developer impact
----------------

TODO

--------------------------------
Infrastructure/operations impact
--------------------------------

TODO

--------------------
Documentation impact
--------------------

Document that there might be several bootstrap images, explain how
to (re)build them, and switch between the images.

--------------------
Expected OSCI impact
--------------------

TODO

--------------
Implementation
--------------

Assignee(s)
===========



Work Items
==========

TODO

Dependencies
============

None

------------
Testing, QA
------------

TODO

Acceptance criteria
===================

TODO


----------
References
----------

TODO
