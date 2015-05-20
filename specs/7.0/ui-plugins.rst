..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===============================
Support for UI Parts of Plugins
===============================

https://blueprints.launchpad.net/fuel/+spec/ui-plugins

Some plugin writers may want to add new elements to Fuel UI like new pages,
tabs, styles, etc.

Problem description
===================

Currently Fuel has support for basic plugins, which can only modify UI by
extending the settings tab. For some complex plugins extending the settings
tab is not sufficient, so support for custom UI modifications is required.

Proposed change
===============

Each plugins should be able to provide its custom UI parts with arbitrary
Javascript files, styles, images and other static content. UI parts should
also contain one or more mixins (UI elements which are embedded into Fuel UI).
Fuel UI should support a few mixin types, such as a new tab, a complex control
for the settings tab, etc.

Format of UI part of plugin
---------------------------

A UI part of plugin is a `ui_static` directory which contains all the files the
plugin needs. The plugin must also have a `plugin.js` file in this directory.
`plugin.js` should be a module described using Asynchronous Module Definition
(AMD) format. The module should have all other files as dependencies and should
export plugin metadata.

.. code-block:: text

    .
    |-- environment_config.yaml
    |-- metadata.yaml
    |-- tasks.yaml
    |-- ...
    `-- ui_static
        |-- plugin.js
        |-- module1.jsx
        |-- styles.less
        |-- ...
        `-- pic1.png

plugin.js should export an object:

.. code-block:: js

  {
    mixins: [
      {
        type: 'cluster_tab',
        ...
      },
      ...
    ],
    translations: {
      ...
    }
  }

* `mixins` field should contain a list of mixins that plugin adds into Fuel
  UI. Mixin is a new entity which should be added to Fuel UI. Every mixin has
  its type and a set of attributes.

* `translations` are translations in `i18next
  <http://i18next.com/pages/doc_features.html>`_ format that are used in the
  plugin. They are merged with existing translations when plugin is loaded.

Mixin types
-----------

cluster_tab
^^^^^^^^^^^

Creates a new tab:

.. code-block:: js

  {
    type: 'cluster_tab',
    attributes: {
      name: 'fencing',
      after: 'settings',
      constructor: FencingTab
    }
  }

* `name` is a name of the tab. It will be used in URL for tab and for its
  icon.

* `after` is name of a tab after which the tab provided by the plugin should
  be inserted. If there are several plugins with same after field, then
  sorting by their names will be used to determine order.

* `constuctor` is a `React
  <https://facebook.github.io/react/>`_ component which renders tab contents.

  - It accepts the following props:

    + `cluster`: `Backbone.Model
      <http://backbonejs.org/#Model/>`_ instance of the current cluster. The
      model contains output of cluster API.

    + `tabOptions`: Array of tab parameters from the URL. In case of URL
      `/cluster/1/custom_tab/opt1/opt2` there should be `['opt1', 'opt2']`.

  - It may have `visible` static method. It determines whether tab is visible
    or not by its return value. Accepts an object with the props (`cluster`
    and `tabOptions`).


settings_control
^^^^^^^^^^^^^^^^

(TBD)

Handling multiple versions of a plugin
--------------------------------------

If there are multiple versions of a plugin installed, mixins will be used from
the plugin with the highest version at the time of environment creation.

Alternatives
------------

We can continue to extend our control descriptions format, but it's not
possible to cover all the cases using it - some plugins may require very
complex UI, displaying some graphs, etc.

Data model impact
-----------------

Plugin developer must set `ui` field in `metadata.yaml` of plugin to true so
UI can know that this plugin has UI part which must be loaded. Also plugin
developer may want to build (preprocess/minify) his plugin, in that case
`ui_build` must also be set to true.

REST API impact
---------------

**GET /api/v1/plugins/**

A new boolean field `ui` should be added API output. This field has the value
of `ui` field in `metadata.yaml`. If this field is set to true, then Fuel UI
should load and process the UI part of the plugin.

.. code-block:: json

  [
    {
      "id": 1,
      "name": "plugin_name",
      "version": "1.0",
      ...
      "ui": true
    }
  ]

**GET /api/v1/clusters/:id/**

A new field `plugins` should be added to list plugin ids which are used for the
environment. It should be used to determine which mixins from which plugins of
which versions should be added to the environment.

.. code-block:: json

  [
    {
      "id": 1,
      "name": "Env #1",
      ...
      "plugins": [11, 13, 17]
    }
  ]

Fuel Plugin Builder impact
--------------------------

(TBD)

Upgrade impact
--------------

None

Security impact
---------------

* Plugin can inject arbitrary Javascript code into Fuel UI.

* Plugin can break Fuel UI, and it only would be possible to uninstall that
  plugin using Fuel CLI.

Notifications impact
--------------------

None

Other end user impact
---------------------

Time of Fuel UI loading with lots of plugins will increase.

Performance Impact
------------------

There will be slight performance impact as mixins and translations provided by
plugin will be processed.

Plugin impact
-------------

Described above.

Other deployer impact
---------------------

* Nginx config should be modified to make `ui_static` dir of plugins available
  by url `/static/plugins/<plugin_name>-<plugin_version>`.
* UI parts of plugins should be extracted from a plugin archive and placed to
  nginx container so nginx should be able to serve them.

Developer impact
----------------

New UI code should be written to be easily extendable by mixins.

Infrastructure impact
---------------------

(TBD)

Explain what changes in project infrastructure will be required to support the
proposed change. Consider the following:

* Will it increase the load on CI infrastructure by making build or test jobs
  consume more CPU, network, or storage capacity? Will it increase the number
  of scheduled jobs?

* Will it require new workflows or changes in existing workflows implemented in
  CI, packaging, source code management, code review, or software artefact
  publishing tools?

  * Will it require new or upgraded tools or services to be deployed on project
    infrastructure?

  * Will it require new types of Jenkins jobs?

  * Will it affect git branch management strategies?

  * Will it introduce new release artefacts?

* Will it require changes in build environments of any existing CI jobs? Would
  such changes be backwards compatible with previous Fuel releases currently
  supported by project infrastructure?


Implementation
==============

Assignee(s)
-----------

Primary assignee:
  vkramskikh@mirantis.com

Other contributors:
  (TBD)

Work Items
----------

(TBD)

Work items or tasks -- break the feature up into the things that need to be
done to implement it. Those parts might end up being done by different people,
but we're mostly trying to understand the timeline for implementation.

Dependencies
============

None

Testing
=======

This feature should be covered by unit tests. Functional tests are not needed.

Documentation Impact
====================

Changes to plugin format and available mixin types should be documented. There
should be a simple plugin example for every mixin type. There should be a guide
to create a plugin, how to debug it, etc.

References
==========

None
