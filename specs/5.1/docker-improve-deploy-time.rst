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
Describe any potential security impact on the system.  Some of the items to
consider include:
There is no change to security impact.
Notifications impact
Please specify any changes to notifications. Be that an extra notification,
changes to an existing notification, or removing a notification.
There are no notification changes.
Performance Impact
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
---------------------
Assignee(s)
Who is leading the writing of the code? Or is this a blueprint where you’re
throwing it out there to see who picks it up?
Primary assignee: raytrac3r (Matthew Mosesohn)
Work Items
---------------
Work items or tasks – break the feature up into the things that need to be done
to implement it. Those parts might end up being done by different people, but
we’re mostly trying to understand the timeline for implementation.
ISO build changes:
* Create empty Docker registry at end of docker image build
* Load images into Docker registry
* Export registry with bundled images and store on ISO

Deploy changes:
* Launch docker registry and pull images down
* Continue deployment as usual

Dependencies
------------

Docker registry server image
Does this feature require any new library dependencies or code otherwise not
included in Fuel? Or does it depend on a specific version of library?
No
Testing
Please discuss how the change will be tested. It is assumed that unit test
coverage will be added so that doesn’t need to be mentioned explicitly, but
discussion of why you think unit tests are sufficient and we don’t need to add
more functional tests would need to be included.
Benchmarking of deploy time should be checked.
Tests for regression on heavily loaded environments with little available
memory.
Is this untestable in gate given current limitations (specific hardware /
software configurations available)? If so, are there mitigation plans (3rd
party testing, gate enhancements, etc).
No
Documentation Impact
--------------------

What is the impact on the docs team of this change? Some changes might require
donating resources to the docs team to have the documentation updated. Don’t
repeat details discussed above, but please reference them here.
Fuel upgrades process of loading new images as part of upgrade will be
impacted, but old method would still work.

References
==========
https://github.com/dotcloud/docker-registry
