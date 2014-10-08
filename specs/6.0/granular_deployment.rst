..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==================================
Granular deployment for fuel roles
==================================

Problem description
===================

Our deployment process is very complicated. There are a lot of Puppet modules
used together by our manifests and dependencies between these modules are also
very complex and abundant.
This leads to the following consequences:
- It becomes very difficult to add new features. Even changes that could
look minor from the first glance can easily and randomly break any other
functionality. Trying to guess how any e change could affect dependencies
and ordering of deployment process is very hard and error-prone.
- Debugging is also affected. Localizing bugs could be very troublesome due
to manifests being complex and hard to understand. Debugging tools are
also almost non-existent.
- Reproducing bugs and testing takes lots of time because we have no easy
and reliable way to repeat only some part of the deployment. The only thing
we can do is to start the process again and wait for several hours to get any
results. Snapshots are not very helpful because deployment cannot be reliably
stopped and the state saved. These actions most likely break deployment or at
least change its outcome.
- New members of our team or outside developers who want to add some new
functionality to our project are completely out of luck. They will have to
spend many days just to gain minor understanding how our deployment works.
And most likely will make a lot of hard to debug mistakes.
- Using our product is also not as easy as we would like it to be for customers
and other people in the community. People usually cannot easily understand how
the deployment works and have to just follow every step in documentation. It
makes them unable to act reasonably if something goes wrong.
- Integrating our Puppet library with any existing Puppet environments or any
other deployment system is far too difficult in most cases because we are using
too many customizations and also due to the nature of Puppet that makes core
sharing and reuse not as effective as with other programming languages.


Proposed change
===============

If we want to address any of these issues we should find a way to make our
architecture less complex and more manageable. It’s known that the best way
to understand any large and monolithic structure is to to take it apart and
then learn how does each of the pieces work and then how do they interact with
each other.

So we should try to separate the whole deployment process to many small parts
that could do only one or several closely related tasks. Each of these parts
would be easy to understand for a single developer. Testing and debugging could
also be done separately so localizing and fixing bugs would be much easier than
it is now.

Thinking about the deployment process as a list of atomic tasks will make our
reference architectures and server roles much more dynamic. If you change what
tasks you are going to perform and their order you can create as many custom
sets of roles as you need without any modification of the tasks themselves.
Another good feature of separated deployment would be the ability to run
pre-deployment and post-deployment tests before and after these tasks.
They could be just sanity checks to determine if the task can be performed
before it is started. Or there could be some smoke tests that will check the
results of the previously performed tasks. Failed and passed tests will greatly
increase the feedback a user or developer is getting from the deployment
process making it possible to determine what have failed by just a single
glance at the deployment UI.

Each task can have some internal dependencies but most likely there would not
be too many of them. It will make manual analyzing of dependency graph possible
within a single task. The task can also have some requirements. System should
be in the specific state before the task can be started and this can be ensured
by the pre-deployment tests.

The introduction of Granular Deployment will be a rather extensive change
to almost all components of the Fuel project and a serious architectural
modification.

Our deployment architecture consists of many components that can be represented
as following layers. Each layer servers it’s own purpose.

Control Layer
-------------

This layer is represented by Nailgun, its agent, API, Web and CLI interface.
All this tools serve as both user interface and the business logic center.
- Nailgun should generate the configuration of the environment that should be
deployed based on user input and hardware data. Configuration includes settings
structure and a list of tasks that should be done to deploy each node.
- Nailgun should pass this configuration to the Orchestration layer and receive
status and report from it.
- Nailgun should be extensible through plug in system and upgradable together
with the master node.
- Nailgun should try NOT to delve deeper into how exactly the generated
configuration would be deployed and how tasks are being executed. It’s out of
the scope of control layer and goes against the loose coupling of the
architecture that would allow us to develop other components more or less
independently from the control layer.

Orchestration Layer
-------------------

This layer should control the provisioning and deployment of nodes. It
processes the status of nodes and the progress of their deployment to determine
when and what tasks should be run.
- Astute receives deployment setting from the control layer and starts to
execute the deployment starting with provisioning.
- Astute reports the progress of the deployment and the result to Nailgun.
- Astute uses the Communication layer to execute tasks or commands on the
managed nodes or to communicate with the provisioning tool. It also polls the
deployment and provisioning processes to determine their statuses.
- Astute should NOT modify the settings passed by the Nilgun or make any data
processing.
- Astute MAY in some conditions execute extra tasks or actions not mentioned by
Nailgun.

Communication Layer
-------------------

Communication layer provides means of remote execution of tasks or commands
mostly for Orchestration layer. It should pass unmodified data to the managed
server and return back the results.
In our case this layer is represented by MCollective and it’s agents.

Deployment Layer
----------------

This layer is responsible for the actual provisioning and deployment of managed
servers. Currently we have Cobbler for provisioning and we are using a single
Puppet manifest for deployment. We are going to implement TaskLib as an
abstraction layer between different types of tasks and actions and
Communication layer.
These tasks should be able to do anything they was designed to do independently
from the Orchestration. They can use data provided indirectly through the
astute.yaml file. A task can be anything from a simple shell exec to Puppet
manifests and Ruby/Python scripts. It doesn’t really matter how do the task
implement it’s purpose as long as it does work.

Tasks, roles and plugin
-----------------------

After this iteration will be completed - it should be possible to execute
any number of tasks for specific fuel role. These actions can
be either Puppet manifest runs or shell commands. Both plugins
and deployment hook can be converted to task format. Tasks and roles
can come either from the basic deployment or from a plugins, developed
either by partners or external contributers.

A plugin should have at least these components:
- One or more additional tasks that will be delivered
to the managed node and executed there
- Mappings between these task and roles when they should
be run.
- Packages, if they are required.
- Metadata that can describe additional environment settings

Task format
-----------

A task is nothing more then a directory with task.yaml file in it.
This file should contain the type of task, optional description
and comment, and special attributes required for the type. Task
is named by the name of it's folder. Tasks can be stored in a hierarchy
stating from the task library directory root.
::

  >> controller/mysql/task.yaml

    comment: Deploy MySQL on controller
    description: This task will deploy MySQL on the controller node
    type: puppet
    puppet_manifest: site.pp

This file describes controller/mysql task that will deploy
mysql using site.pp Puppet manifest.

Role format
~~~~~~~~~~~

A role is a mapping between role name and a set of task names
that should be executed when this role is assigned to a server.
These files are placed to /etc/fuel/roles where they are read
by Nailgun and then sent to Astute as a list of task names:
::

    >> /etc/fuel/roles/controller.yaml

    - role: *
      priority: 0
      task: config_network
    - role: controller
      priority: 1
      task: controller/mysql
    - role: controller
      priority: 2
      task: controller/rabbitmq
    - role: controller
      priority: 3
      task: nova
    - role:
        - controller
        - compute
      priority: 100
      task: update_hosts_file

Here '*' means all the roles and role attribute can conatin
array of roles. For each role tasks are sorted by their priority
before they are sent to Astute.

A plugin can contain additional role file like this:
::

    >> /etc/fuel/roles/glusterfs.yaml

    - role: glusterfs
      priority: 1
      task: deploy_glusterfs

    And a task deploy_glusterfs

    >> /etc/puppet/task/deploy_glusterfs/task.yaml

    comment: Deploy glusterfs node
    description: This task deploys glusterfs node to be used as a storage for
    OpenStack cluster
    type: puppet
    puppet_manifest: gluster.pp

Plugin configuration management and metadata to run those tools
---------------------------------------------------------------
Plugin writer will prepare package with manifests/simple bash scripts
and metadata about how run them.
This tools (scripts and metadata) will be placed on master node in
specified folders.
And astute will rsync them on deployment start or as separate action.

Alternatives
------------

In general we dont have time to work on replacement of astute,
for next reasons:

- Short release cycle for 6.0
- Any disruptive changes will require tremendous amount of qa resources,
  and can limit overall team velocity.
- Quite unique deployment model, so anything we will choose will require
  customization.

Additional updates will be provided later.

- Mistral
- Salt
- Custom orchestrator with celery

Data model impact
-----------------

DB:
task_metadata field on Release model will be required to store tasks
for all roles.
::

    controller:
        -
          priority: 0
          description: Network configuration, maybe something else
          name: network_config
    compute:
        -
          priority: 0
          description: Network configuration, maybe something else
          name: network_config
        -
          priority: 10
          description: Task for deployment of nova compute
          name: deploy_compute


Astute facts:
Nailgun will generate additional section for astute facts.
This section will contain list of tasks with its priorities for specific role.
Astute fact will be extended with tasks exactly in same format it is stored
in database, so if we are generating fact for compute role,
astute will have section like:
::

    tasks:
        -
          priority: 0
          description: Network configuration, maybe something else
          name: deploy_all
        -
          priority: 10
          description: Task for plugin deployment
          name: deploy_xen

Task format perspective:
    Will be extended.


Task deployment process
-----------------------

- When deployment plugin is installed it should place tasks order extension
  in yaml format. By default it will be:
  **/etc/fuel/roles/{release}/*.yaml**
- On deployment start nailgun will perform lookup by glob:
  **/etc/fuel/roles/{cluster.release.version}/*.yaml**
  If any configuration is there we are validating it and proceed
  with deployment
- Tasks subsection will be added to deployment_info sended for node to astute
- Astute executes tasks for each role in linear fashion

Conditional tasks
-----------------

To support task execution based on cluster settings/network provider settings/
maybe something else ???
we will use same expression parser that is used on UI for restrictions:

https://github.com/stackforge/fuel-web/blob/master/nailgun/nailgun/utils/
expression_parser.py

Next example will be always evaluated as false ofcourse, just for example:
::

    controller:
      - condition: 'false'
        description: Install vcenter driver
        name: install_vcenter_driver
        priority: 20

    And this one makes sense actually:

    controller:
      - condition: "settings:common.libvirt_type.value == 'vcenter'"
        description: Install vcenter driver
        name: install_vcenter_driver
        priority: 20


REST API impact
---------------
Iteration 1:
Current rest api implementation will be enough to modify/add tasks
for specific release.

Iteration 2:
Rest api will be extended to support different kinds of operation with tasks.
For example something like:
**fuel deploy --node 3 --tasks 0-10**
That will execute only tasks with priorities from 0 to 10.
Will be designed later if there will be time for this stuff.

Upgrade impact
--------------

Support for invoking different astute task names in nailgun based
on release version. If we are managing cluster with 5.1 release we will
use Puppet plugin to deploy/patch slaves. But in 6.0 it will be TaskAPI plugin.
This basic versioning support will be done in nailgun.

Security impact
---------------

Notifications impact
--------------------

We can show user exact step of deployment task with description and name.

Other end user impact
---------------------

Performance Impact
------------------

No singnificat changes in execution model, so i assume deployment time
will stay the same.

Other deployer impact
---------------------

It will be possible to execute only desired scripts on target slave node.

Developer impact
----------------

Easier debuging/development process.

Implementation
==============

Assignee(s)
-----------

Primary assignee:

- Dmitry Ilyin <dilyin@mirantis.com>
- Dmitry Shulyak <dshulyak@mirantis.com>
- Vladimir Sharshov <vsharhov@mirantis.com>

Work Items
----------
Iteration 1:
- write TaskAPI mcollective plugin that will invoke cmd interface for
TaskAPI util
- Refactor/Add separate deployment method to work with task list provided
by nailgun and use TaskAPI plugin
- prepare packages for TaskAPI and move Dmitry Ilyin's implementation
to fuel-astute/fuel-library repo or create new one (fuel-tasklib ???)

Dependencies
============

Testing
=======

Every new piece of code will be covered by unit tests.
Everything will be automaticly covered by system tests.
Will be great to implement functional tests to run deployment for
each role with its own actions.

Documentation Impact
====================

References
==========
