..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

=====================================================
Template based test cases with external configuration
=====================================================

Improve the system test for using external configuration

--------------------
Problem description
--------------------

We have a permanent growing product with a lot of features. From release to
release we should cover more and more cases and current approach can not keep
up with the changes.

* Tests have a lot of copy-paste code

* Many tests have a hardcoded cluster configuration

* For test additional configuration with the same steps, we should write
another test


----------------
Proposed changes
----------------

Write extension for current test framework which might works with external
configuration and has template structure for the test cases.

**Pros**:

* Configuration for test be at the external human readable yaml file

* Unified library for steps of test, checkers and actions

* Inheritance, simple expanding and composition new cases with already existing

* Get a test matrix cases and configuration


Configuration files for tests
=============================

Basic idea, why we use configuration. We can store everything what we need for test in one place.

Configuration contains a basic settings for OpenStack which provided into Fuel when  test create OS environment.

For match the test with the configuration, framework uses name of configuration file like suffix for *base_groups* of test.

*Basic structure for configuration file (example_config.yaml)*::

    template:
        name: 1 Controller, 1 Compute, 1 Cinder on Neutron/VLAN
        slaves: 3
        devops-template: *devops-config
        cluster-template:
            name: env1
            release: ubuntu
            settings:
                components: *componets-config
                storages: *storages-config
            network: *network-config
            nodes: *nodes

*Components config*::

    sahara: false
    murano: false
    ceilometer: false

*Storages configuration*::

    storages-config: &storages-config
        volume-lvm: true
        volume-ceph: false
        image-ceph: false
        ephemeral-ceph: false
        rados-ceph: false
        replica-ceph: 2

*Network configuration*::

    network-config: &network-config
        provider: neutron
        segment-type: vlan
        public-ip-to-all: false

*Node configuration*::

    nodes: &nodes
        - roles:
            - controller
          count: 1
          node_group: rack-01 # Assing node into devops node group
        - roles:
            - compute
          count: 1
          node_group: rack-01
        - roles:
            - cinder
          count: 1
          node_group: rack-01


Test cases re-design
====================

New approach for writing of test scripts.

* coding separate steps like atomic actions

* combine and sort steps as needed for a scenario

* better a test report which contains each step and result for it

* more readable test output to improve quality of investigation

*Actions example*::

  class BaseActions:

    # Default value
    deploy_timeout = 1200

    def _action_deploy_cluster(self):
        """Deploy environment"""
        self.fuel_web.deploy_cluster_wait(self.cluster_id,
            timeout=self.deploy_timeout)

    def _action_network_check(self):
        """Run network checker"""
        self.fuel_web.verify_network(self.cluster_id)

    @action
    def health_check(self):
        """Run health checker"""
        self.fuel_web.run_ostf(self.cluster_id)


*Test example*::

  class CreateDeployOstf(BaseActions):
    """Case deploy Environment
        Scenario:
        1. Deploy Environment
        2. Run network checker
        3. Run OSTF
    """

    # To control behavior of action use a class attribute
    deploy_timeout = 1800

    base_group = ['system_test', 'system_test.deploy_ostf']
    actions_order = [
        '_action_deploy_cluster',
        '_action_network_check',
        '_action_health_check',
    ]


Running new test cases
======================

For selecting test with specific configuration please use special test group.
It contains combination of base_groups from the test plus name of
configuration file without extension. Test group and configuration group
divided by point - BASE_GROUP.CONFIG_NAME:

* system_test.example_config

* system_test.deploy_ostf.example_config

------------
Alternatives
------------

N/A

--------------
Upgrade impact
--------------

N/A

---------------
Security impact
---------------

N/A

--------------------
Notifications impact
--------------------

N/A

---------------
End user impact
---------------

N/a

------------------
Performance impact
------------------

N/A

-----------------
Deployment impact
-----------------

N/A

----------------
Developer impact
----------------

N/A

---------------------
Infrastructure impact
---------------------

N/A

--------------------
Documentation impact
--------------------

N/A

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  Dmytro Tyzhnenko

Other contributors:
  Denys Dmytriiev

Mandatory design review:
  Anastasiia Urlapova, Denys Dmytriiev

Work Items
==========

* Create configuration structure

* Code base models for templated tests

* Implement collector of test + configuration combination

* Integrate with current framework

* Update reporting tools

Dependencies
============

* Environment templates for devops https://blueprints.launchpad.net/fuel/+spec/template-based-virtual-devops-environments

------------
Testing, QA
------------

All existed tests and tools should work as worked before.

Acceptance criteria
===================

Tool which can combine templated tests and external configuration files on same
infrastructure as exist today.

----------
References
----------

https://blueprints.launchpad.net/fuel/+spec/template-based-testcases
