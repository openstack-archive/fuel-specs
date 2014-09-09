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
collecting service (collector), the second one is analytical service
(analytic).

.. figure:: images/fuel-stat-architecture.png
   :alt: Fuel-stat architecture

   Fuel-stat architecture

Community and commercial Fuel installations will be provided by different
Fuel-stat instances. So we should provide different URIs of collector and
analytic in community and commercial ISOs.

Collector service provides REST API which available from the internet.
Analytic provides REST API and have UI to viewing stat reports online.

Requests and responses in collector and analytic must be validated by
JSON Schema.

Analytic web UI uses analytic API. UI design is out of scope of this
specification.

Each Fuel installation, with enabled anonymous stat option, periodically
sends info to collector API. Each request and response is validated by
JSON scheme. After validation and processing data saves into collector DB.
Collector DB has slave replica. Data from collector DB extracted, transformed,
loaded (ETL) into analytic DB.

Periodically backup of collector and analytic DBs is made. Collector DB's
backup is made from slave replica due to performance issues.

Analytics information can be accessed through analytic API or web UI. For
heavy analytic reports can be used asynchronous processing, based on tasks
and messaging system.

Sending of anonymous statistics option should be added into Nailgun UI.
Detailed description of sending statistics should be added into Nailgun UI.

Storing of action logs should be added into Nailgun. Each modification
requested through Nailgun API should be stored into DB table action_logs.
Success and failure operations should be logged. Logged info should be
sanitized from any credentials data. Requests from fuel-cli have 'python'
in HTTP User-Agent header and can be separated by this criterion.

Handle calculation of execution time for asynchronous tasks. Add execution
time into action_logs.

Sending of statistics from Nailgun to collecting service will be implemented
as background process. This background process should save info about last
sent action log and sends only fresh records. Sending process should not
affect Nailgun services, should be robust to errors. It can be started as
uWSGI mule process for example.

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
No changes in Nailgun REST API.

Upgrade impact
--------------

Action logs table should be included into DB migration.

Security impact
---------------

There are open questions:
* Authentication and authorization in analytic. Is it required?
* HTTPS on collector and analytic API? Have we certificates for wildcard
  third level domains for mirantis.com or single certificate to be issued
  or self signed certificates?
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

We require hosting for collector and analytic services and their DBs.

Collector and analytic services, DBs migrations should be deployed by
puppet manifests.

Community and commercial Fuel installation are provided by different
Fuel-stat instances. Different URIs should be in settings of
community and commercial Fuel distributions.

Developer impact
----------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  aroma@mirantis.com (Artem Roma)
  akislitsky@mirantis.com (Alexander Kislitksy)

Other contributors:
  UI developer
  Devops developer
  QA specialist
  OSCI specialist

Work Items
----------

Implementation is separated on several stages.

Used technologies
^^^^^^^^^^^^^^^^^

* Programming language - Python 2.7.
* Application server - uWSGI.
* API protocol definition - JSON Schema.
* Web service - Nginx.
* Database - PostgreSQL.
* Slave DB replica - by PostgreSQL native WAL technology.
* DB schema migrations - Alembic.
* ETL - to be defined when analytics reports format will be defined.
  Possible options: Pentaho, Talend, self implemented, e.t.c.

Stage 1
^^^^^^^

All logic should be covered by unittests.

* Configure uWSGI + Nginx + DB. Run simple WSGI application in collector
* Add JSON Schema support and validation of test request/response
* Initiate implementation of puppet manifests for service deployment,
  DBs backup
* Check deployment of collector and analytic, when deployment is ready
* Implement part of collector API and initiate testing and load testing
  of it by QA team
* Implement saving action logs in Nailgun
* Implement sending statistics to collector from Nailgun
* Initiate Nailgun testing by QA
* Implement logic enough for switching to implementation of analytic service
* Implement part of analytic API with JSON validation
* Initiate analytic UI implementation
* Implement full analytic API, collector API
* Testing, fixing
* First release is done

Limitations of the first release:
* No authentication
* Only one DB for collector and analytic
* No ETL
* No replication of collector DB
* No backup of DB
* Heavy analytic reports are not handled

Stage 2
^^^^^^^

* Handle collector DB replication
* Handle collector DB backup
* Improve analytic reports

Stage 3
^^^^^^^

* Handle authentication
* Handle SSL in APIs, UI
* Improve analytic reports

Stage 4
^^^^^^^

* ETL
* Separate analytic and collector DBs
* Handle analytic DB backup
* Improve analytic reports

Stage 5
^^^^^^^

* Handle heavy analytic reports
* Handle data partitioning
* Improve analytic reports

Dependencies
============

None

Testing
=======

We require those tests:

* APIs integration testing
* APIs load testing
* UI functional testing

Documentation Impact
====================

Option for enabling sending, and statistics data details hould be documented.

Collector and analytic APIs will be documented by JSON Schemas (probably by
sphinx).

Analytic reports and analytic UI should be documented.

References
==========

None