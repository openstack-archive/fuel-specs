..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=============================
Package handling via Fuel CLI
=============================

https://blueprints.launchpad.net/fuel/+spec/example

We need a possibility to handle packages upgrade/install/remove on already
deployed nodes.

After package manipulation we need way to execute custom oneliner or to
perform service restart.

-------------------
Problem description
-------------------

Now you can do package manipulation by login to proper server and manually
start apt-get/yum process. After that operation operator should restart needed
services.

----------------
Proposed changes
----------------

We will extend Fuel API to be able to store package manipulation YAML.
This YAML format is described in data model section.

We will create two additional granular task:

   - upload_pm - upload package manipulation file to node
   - execute_pm - execute puppet manifest which will perform package
     manipulation

Upload_pm will get YAML from Fuel Master and stores it in /etc/hiera/
directory. Data from YAML will be available to puppet via hiera()/hiera_hash().

Execute_pm task will execute puppet manifest which will handle package
manipulation.

Execute_pm task will require upload_pm task, this way user can run only
execute_pm and upload_pm will be started automatically.

Web UI
======

None. Package manipulation will be available only to advanced users via CLI.

Nailgun
=======

Data model
----------

We need to store in DB information about package manipulation for each node.

Package manipulation YAML format is described below.

Example:

.. code-block:: yaml

 ---
 packages:
 - name: apache2
   version: 2.4.7-1ubuntu4.6
   after:
   - provider: upstart
     ensure: running
     name: apache2
 - name: wget
   version: latest
   after:
   - provider: exec
     name: wget -V
 - name: tmux
 - name: screen
   version: absent
 - name: mysql-server-wsrep
   version: latest
   after:
   - provider: corosync
     ensure: running
     name: p_mysql

List of possible entries in YAML:

   - name - name of package (mandatory)
   - version - version after manipulation (optional). If 'version' parameter is
     missing, default is 'latest'. possible values:

        - latest
        - absent (remove package)
        - <VERSION>

   - after - this contains list of action which should be performed after
     package manipulation (optional). If 'after' parameter is missing,
     default is do nothing.
   - provider - puppet service provider (optional). If 'provider' has value
     'exec' instead of service puppet resource we will execute puppet exec.
   - ensure - puppet ensure parameter for service provider (optional).
     If 'ensure' is missing, default is 'running'.
   - name - puppet name parameter for service provider (mandatory if 'after'
     is present).
     If 'provider' has value 'exec' here you should pass bash oneliner.

REST API
--------

API should allow to get/set information about package manipulation for given
environment.

This API call should be available per environment.
API should do some validation for each call:

   - Check if uploaded data has YAML format.

Orchestration
=============

RPC Protocol
------------

None

Fuel Client
===========

Flow of plugin manipulation:

#. upload YAML:

   fuel package --env 1 --upload file.yaml

#. download YAML

   fuel package --env 1 --download

#. execute uploaded YAML on given nodes:

   fuel node --node 2,3 --tasks execute_pm

Plugins
=======

None

Fuel Library
============

We need to prepare new granular tasks responsible for syncing YAML and for
executing package manipulation.

------------
Alternatives
------------

We can prepare some kind of script (bash/python/...) which will allow operator
to run command on multiple servers. This can be achieved by ussing python pssh.

   Cons:
      - Hard to use outside Fuel Master (no API).
      - User need to write onliners for each command (ex. upgrade+restart
        service)

   Pros:
      - Easy implementation

--------------
Upgrade impact
--------------

None

---------------
Security impact
---------------

New API should have standard Fuel API authentication enabled.
It is possible that on some nodes operator will have differenet (vulnerable)
versions of packages.

--------------------
Notifications impact
--------------------

None

---------------
End user impact
---------------

In some cases package manipulation can lead to service disruption. 
In some cases package manipulation can lead to data loss (e.g. overwrite of
data).

This feature is designed on for advanced users, because there is possibility
to destroy running cluster (ex. remove some crucial packages).

------------------
Performance impact
------------------

In most cases none. 
But sometimes package manipulation can run some "heavy" tasks.
Ex. Ceph upgrade can run some kind of index rebuilding which will lead to high
IO on node.

Different versions of the packages can lead to hard to debug performance
problems.
Ex. daemon in version A installed on node B in version C on environment D have
performance problems.

-----------------
Deployment impact
-----------------

None

----------------
Developer impact
----------------

None

--------------------------------
Infrastructure/operations impact
--------------------------------

None

--------------------
Documentation impact
--------------------

We need to prepare documenation which will describe this feature.

--------------------
Expected OSCI impact
--------------------

None

--------------
Implementation
--------------

Assignee(s)
===========

Work Items
==========

 * Extend API to allow to store package manipulation YAML
 * Write upload_pm and execute_pm granular task

Dependencies
============

None

-----------
Testing, QA
-----------



Acceptance criteria
===================



----------
References
----------
