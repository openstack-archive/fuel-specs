======================================================
Docker Registry & Improving Deploy Time of Master Node
======================================================

Problem description
===================

Deploying Fuel Master node takes an excessively long period of time due to the
way the containers are packaged and distributed on the Fuel ISO.

Proposed change
===============

By using a local Docker registry server, we can cut down on the extra
processing power required to parse large, independent container images.
The goal is to reduce Fuel Master deploy time from 10-20 minutes to 5-15
minutes.

Alternatives
------------

We can leave the implementation as-is.

Data model impact
-----------------
What new data objects and/or database schema changes is this going to require?
None
What database migrations will accompany this change.
None
How will the initial set of new data objects be generated, for example if you
need to take into account existing instances, or modify other existing data
describe how that will work.
N/A

REST API impact
---------------

Each API method which is either added or changed should have the following
There are no REST API changes.

Security impact
---------------

Describe any potential security impact on the system.  Some of the items to
consider include:
There is no change to security impact.

Notifications impact
--------------------

Please specify any changes to notifications. Be that an extra notification,
changes to an existing notification, or removing a notification.
There are no notification changes.

Other end user impact
---------------------

Aside from the API, are there other ways a user will interact with this
feature?

* Upgrade process will be impacted slightly to work through a registry to 
  more rapidly load images.


Performance Impact
------------------

Describe any potential performance impact on the system, for example how often
will new code be called, and is there a major change to the calling pattern of
existing code.
This will improve performance in deploying Fuel Master node. Post-deployment
will remain exactly as it is in Fuel 5.0.

Other deployer impact
---------------------

Discuss things that will affect how you deploy and configure Fuel that have not
already been mentioned, such as:
Deployment impact is non-invasive. The result will be an identical, but faster
experience.

Developer impact
----------------

Discuss things that will affect other developers working on Fuel, such as:

N/A

Implementation
==============

Assignee(s)
-----------

Who is leading the writing of the code? Or is this a blueprint where you’re
throwing it out there to see who picks it up?

Primary assignee:
  raytrac3r (Matthew Mosesohn)

Work Items
----------

ISO build changes:
* Create empty Docker registry at end of docker image build
* Load images into Docker registry
* Export registry with bundled images and store on ISO

Deploy changes:
* Launch docker registry and pull images down
* Continue deployment as usual

Dependencies
============

Docker registry server image

Does this feature require any new library dependencies or code otherwise not
included in Fuel? Or does it depend on a specific version of library?

No

Testing
=======

Current Fuel Master deployment tests are adequate.

Documentation Impact
====================

What is the impact on the docs team of this change? Some changes might require
donating resources to the docs team to have the documentation updated. Don’t
repeat details discussed above, but please reference them here.
Fuel upgrades process of loading new images as part of upgrade will be
impacted, but old method would still work.

References
==========
https://github.com/dotcloud/docker-registry
