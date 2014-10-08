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
functionality. Trying to guess how any change could affect dependencies
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
- Nailgun should be extensible through plugin system and upgradable together
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
- Astute should NOT modify the settings passed by the Nailgun or make any data
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
Puppet manifest for deployment.
These tasks should be able to do anything they was designed to do independently
from the Orchestration. They can use data provided indirectly through the
astute.yaml file. A task can be anything from a simple shell exec to Puppet
manifests and Ruby/Python scripts. It doesn’t really matter how do the task
implement it’s purpose as long as it does work.

Graph-based Task API
-----------

Several types of tasks will be introduced in addition to basic deployment
types, like puppet, shell, rsync, upload_file. This types are roles and stages,
and they will serve the purpose to build flexible graph of tasks.

Types of tasks:
    - type: role - grouping of the tasks based on nailgun role entities
    - type: stage - skeleton of deployment graph in fuel, right now there is 4 stages: prepare, pre_deployment, deployment, post_deploment
    - deployment tasks:
     - type: puppet - executes puppet manifests with puppet apply
     - type: shell - executes any shell command, like python script.py, ./script.sh
     - type: upload_file - used for configuration upload to target nodes, repo creation
     - type: rsync

Ideally all dependencies between tasks should be described with
requires and required_for attributes, it will allow us to build graph
of tasks in nailgun and then serialize it into orchestrator acceptable format
(workbooks for mistral, or astute-speficic roles with priorities).

type: ROLE
-------------
id: controller
type: role
requires: [primary-controller, <roles>, <tasks>]
required_for: [<stages>, <roles>]
parameters:
    strategy:
        type: parallel
        amount: 8
* each chunk of nodes with this role (8 in this example) will be executed in parallel
    strategy:
        type: one_by_one
* all nodes with this role will be executed sequentially
    strategy:
        type: parallel
* all nodes with this role will be executed in parallel

type: STAGE
------------
id: deploy
type: stage
requires: [<stages>]

Right now we are using hardocded set of stages, but it is completely possible
to make it flexible, and define them with API.

type: DEPLOYMENT TASK TYPES
----------------------------
id: deploy_legacy
type: puppet
role: [primary-controller, controller,
       cinder, compute, ceph-osd]
requires: [<tasks>]
required_for: [<stage>]
parameters:
    puppet_manifest: /etc/puppet/manifests/site.pp
    puppet_modules: /etc/puppet/modules
    timeout: 360

id: network
type: shell
role: [primary-controller, controller]
requires: [deploy_legacy]
required_for: [deploy]
parameters:
    cmd: python /opt/setup_network.py
    timeout: 600


Usage of graph in nailgun
------------------------------------
Based on provided tasks and dependencies between tasks we will build
graph object with help of networkx library [1].
Format of serialized information will depend on orchestrator that we will use
in any particular release.

Let me provide an example:

Consider that we have several types of roles:

- id: deploy
  type: stage
- id: primary-controller
  type: role
  required_for: [deploy]
  parameters:
    strategy:
      type: one_by_one
- id: controller
  type: role
  requires: [primary-controller]
  required_for: [deploy]
  parameters:
    strategy:
      type: parallel
      amount: 2
- id: cinder
  type: role
  requires: [controller]
  required_for: [deploy]
  parameters:
    strategy:
      type: parallel
- id: compute
  type: role
  requires: [controller]
  required_for: [deploy]
  parameters:
    strategy:
        type: parallel
- id: network
  type: role
  requires: [controller]
  required_for: [compute, deploy]
  parameters:
    strategy:
        type: parallel

And there is defined tasks for each role:

- id: setup_services
  type: puppet
  requires: [setup_network]
  role: [controller, primary-controller, compute, network, cinder]
  required_for: [deploy]
  parameters:
    puppet_manifests: /etc/puppet/manifests/controller.pp
    puppet_modules: /etc/puppet/modules
    timeout: 360
- id: setup_network
  type: shell
  role: [controller, primary-controller, compute, network, cinder]
  required_for: [deploy]
  parameters:
    cmd: run_setup_network.sh
    timeout: 120

For each role we can define different subsets of tasks, but for simplicity
lets make this tasks applicable for each role.

Based on this configuration nailgun will send to orchestrator config
in expected by orchestator format.

For example we have several nodes for deployment:

primary-controller: [node-1]
controller: [node-4, node-2, node-3, node-5]
cinder: [node-6]
network: [node-7]
compute: [node-8]

This nodes will be executed in following order:
Deploy primary-controller node-1
Deploy controller node-4, node-2 - you can see that parallel amount is 2
Deploy controller node-3, node-5
Deploy network role node-7 and cinder node-6 - they depend on controller
Deploy compute node-8 - compute depends both on network and controller

During deployment for each node 2 tasks will be executed sequentially:

Run shell script setup_network
Run puppet setup_services

Pre/Post tasks will be added a bit later, but in general they wont be much
different from how it is done for plugins.

Alternatives
------------


Data model impact
-----------------

Astute facts:
Nailgun will generate additional section for astute facts.
This section will contain list of tasks with its priorities for specific role.
Astute fact will be extended with tasks exactly in same format it is stored
in database, so if we are generating fact for compute role,
astute will have section like:
::

    tasks:
        -
          priority: 100
          type: puppet
          uids: [1] - this is done for compatibility reasons
          parameters:
            puppet_manifest: /etc/network.pp
            puppet_modules: /etc/puppet
            timeout: 360
            cwd: /
        -
          priority: 100
          type: puppet
          uids: [2]
          parameters:
            puppet_manifest: /etc/controller.pp
            puppet_modules: /etc/puppet
            timeout: 360
            cwd: /

REST API impact
---------------

In 1st iteration Rest API will not allow to override tasks, or execute
graph partially.

2nd iteration will be covered by separate spec, because this one already
overloaded.

Upgrade impact
--------------

Changes for orchestration will be backward compatible.
For old releases orchestrator will execute only one task,
which will run osnailyfacter manifest.

Security impact
---------------

Notifications impact
--------------------

Other end user impact
---------------------

Performance Impact
------------------

Wont significantly affect deployment time.
Maybe for some cases puppet run will be shorter.

Other deployer impact
---------------------

Developer impact
----------------

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

1. Graph based API for nailgun (config-defined tasks and roles)
2. Add hooks support for deployment stage in astute
3. Remove pre/post tasks from astute, orchestration to nailgun,
   functionality to library (reuse plugins mechanism)
4. Packaging Mistral
5. Dockerizing Mistral
6. Modularizing puppet

Dependencies
============

Testing
=======

Every new piece of code will be covered by unit tests.
This is internal functionality, therefore it will be covered by
system tests without any modifications.
Separate granular functional tests TBD.

Documentation Impact
====================

Requires update to developer and plugin documentation.

References
==========

1. https://networkx.github.io/ - Python utilities for working with graph's
