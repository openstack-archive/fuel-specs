..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===============================================
Fuel-stat - sending of the anonymous statistics
===============================================

https://blueprints.launchpad.net/fuel/+spec/send-anon-usage

Fuel-stat is the service of collecting anonymous and providing analytical
information about using of the Fuel product.

Problem description
===================

We need to understand how customers are using Fuel. We need to collect
anonymous usage statistics and provide the analytics reports.

Proposed change
===============

Fuel-stat service is separated into two parts. The first one is statistics
collecting service (collector), the second one is analytical service (analytic).

Collector service provides REST API which available from the internet.
Analytic provides REST API and have UI to viewing stat reports online.

Requests and responses in collector and analytic must be validated by
JSON Schema.

Analytic web UI uses API for fetching data

Each Fuel installation, with enabled anonymous stat option, periodically
sends info to collector API. Each request and response is validated by
JSON scheme. After validation and processing data saves into collector DB.
Collector DB has slave replica. Data from collector DB extracted, transformed,
loaded into analytic DB.

Periodically backup of collector and analytic DBs is made. Collector DB's
backup is made from slave replica due to performance issues.

Analytics information can be accessed through analytic API or web UI. For heavy
analytic reports can be used asynchronous processing, based on tasks and
messaging system.

Sending of anonymous statistics option should be added into Nailgun UI.
Detailed description of sending statistics should be added into Nailgun UI.

Add storing of action logs added into Nailgun. Each modification requested
through Nailgun API should be stored into DB table action_logs. Success and
failure operations should be logged. Logged info should be sanitized from any
credentials data.

Handle calculation of execution time for asynchronous tasks. Add execution
time into action_logs.

Add background sending of statistics from Nailgun to collecting service.
This background process should save info about last sent action log and send only fresh
records. Sending process should not affect Nailgun services, should be
robust to errors. Can be started as uWSGI mule process for example.


Alternatives
------------

None

Data model impact
-----------------

New databases fer collector and analytic will be created.
Action_logs table added into Nailgun.
In case of extra-large data amounts DB can be periodically partitioned.

REST API impact
---------------

REST API for collector and analytic services will be created.

Upgrade impact
--------------

None

Security impact
---------------

There ara open questions:
* Authentication and authorization in analytic. Is it required?
* HTTPS on collector API? Have we certificates for wildcard third level
  domains for mirantis.com or single certificate to be issued or self
  signed certificates?
  The same question for analytic web UI and API.
* Protection from data spoofing. Is MasterNode uid enough for checking
  request is not fake?

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

Discuss things that will affect how you deploy and configure Fuel
that have not already been mentioned, such as:

* What config options are being added? Should they be more generic than
  proposed? Are the default values ones which will work well in
  real deployments?

* Is this a change that takes immediate effect after its merged, or is it
  something that has to be explicitly enabled?

* If this change is a new binary, how would it be deployed?

* Please state anything that those doing continuous deployment, or those
  upgrading from the previous release, need to be aware of. Also describe
  any plans to deprecate configuration values or features.  For example, if we
  change the directory name that instances are stored in, how do we handle
  instance directories created before the change landed?  Do we move them?  Do
  we have a special case in the code? Do we assume that the operator will
  recreate all the instances in their cloud?

Developer impact
----------------

Discuss things that will affect other developers working on Fuel,
such as:

* If the blueprint proposes a change to the driver API, discussion of how
  drivers would implement the feature is required.

Implementation
==============

Assignee(s)
-----------

Who is leading the writing of the code? Or is this a blueprint where you're
throwing it out there to see who picks it up?

If more than one person is working on the implementation, please designate the
primary author and contact.

Primary assignee:
  <launchpad-id or None>

Other contributors:
  <launchpad-id or None>

Work Items
----------

Work items or tasks -- break the feature up into the things that need to be
done to implement it. Those parts might end up being done by different people,
but we're mostly trying to understand the timeline for implementation.


Dependencies
============

* Include specific references to specs and/or blueprints in fuel, or in other
  projects, that this one either depends on or is related to.

* If this requires functionality of another project that is not currently used
  by Fuel, document that fact.

* Does this feature require any new library dependencies or code otherwise not
  included in Fuel? Or does it depend on a specific version of library?


Testing
=======

Please discuss how the change will be tested. It is assumed that unit test
coverage will be added so that doesn't need to be mentioned explicitly,
but discussion of why you think unit tests are sufficient and we don't need
to add more functional tests would need to be included.

Is this untestable in gate given current limitations (specific hardware /
software configurations available)? If so, are there mitigation plans (3rd
party testing, gate enhancements, etc).


Documentation Impact
====================

What is the impact on the docs team of this change? Some changes might require
donating resources to the docs team to have the documentation updated. Don't
repeat details discussed above, but please reference them here.


References
==========

Please add any useful references here. You are not required to have any
reference. Moreover, this specification should still make sense when your
references are unavailable. Examples of what you could include are:

* Links to mailing list or IRC discussions

* Links to relevant research, if appropriate

* Related specifications as appropriate

* Anything else you feel it is worthwhile to refer to
