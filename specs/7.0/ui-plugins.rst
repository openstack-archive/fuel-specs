..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===============================
Support for UI Parts of Plugins
===============================

https://blueprints.launchpad.net/fuel/+spec/ui-plugins

Some plugin writers should have an ability to add new elements to Fuel UI like
new tabs, checks, styles, etc.

Problem description
===================

Currently Fuel has support for basic plugins, which can only modify UI by
extending the settings tab. For some complex plugins extending the settings
tab is not sufficient, so support for custom UI modifications is required.

Proposed change
===============

Each plugin should be able to provide its custom UI parts with arbitrary
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
      my_plugin: {
        sample_key: 'Sample Value',
        ...
      },
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

(TBD: decide with data format: POJO or models)

cluster_tab
^^^^^^^^^^^

Adds a new tab.

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

* `constructor` is a React component which renders tab contents.

  - It accepts the following props:

    + `cluster`: `Backbone.Model
      <http://backbonejs.org/#Model/>`_ instance of the current cluster. The
      model contains output of cluster API.

    + `tabOptions`: Array of tab parameters from the URL. In case of URL
      `/cluster/1/custom_tab/opt1/opt2` there should be `['opt1', 'opt2']`.

  - It may have `visible` static method. It determines whether tab is visible
    or not by its return value. Accepts an object with the props (`cluster`
    and `tabOptions`). If there is no such method, the tab is always visible.

settings_control
^^^^^^^^^^^^^^^^

Adds a handler for a new type of controls used in `environment_config.yaml`.
Should be used when a complex interface within the settings tab is needed.

.. code-block:: js

  {
    type: 'settings_control',
    attributes: {
      type: 'fencing_agent_config',
      constructor: FencingAgentConfigurationControl
    }
  }

* `type` is a type of the control which is specified in the `type` field in
  `environment_config.yaml` file:

  .. code-block:: yaml

    attributes:
      agent_config:
        type: fencing_agent_config
        value:
          # value may have arbitrary format
          key1: value1
          key2:
            - value21
            - value22
        ...

* `constructor` is a React component which renders a control.

  - It accepts the following props:

    + All props from `environment_config.yaml`. From the example above, the
      component will receive `type` and `value` props.

    + `path`: path to current control, i.e. `fencing_plugin.agent_config`.

    + `disabled`: true if control needs to be disabled, e.g. after successful
      deployment.

    + `cluster` and `settings` models.

  - It may have `validate` static method. It is used when validation is
    performed. It accepts two arguments: the first one is a control declaration
    from `environment_config.yaml` and the second one is an object with models
    used for restrictions (`cluster`, `settings` and others).

predeployment_check
^^^^^^^^^^^^^^^^^^^

Adds a configuration validator which checks environment configuration before
deployment start. Currently validators are called from the deployment
confirmation dialog. Validators should check plugin-managed data for validity.

.. code-block:: js

  {
    type: 'predeployment_check',
    attributes: {
      validator: function(cluster) { ... }
    }
  }

* `validator` is a function which accepts a cluster model as an argument. It
  should return an object of this format:

  .. code-block:: js

    {
      blocker: [
        'Fencing agent configuration is not valid',
        ...
      ],
      warning: [
        'There are no fencing agents configured',
        ...
      ]
    }

  - If there are items in the `blocker` list, then deployment won't be
    possible. Items from this list will be displayed as errors.
  - If there are items in the `warning` list, they will be displayed as
    warnings in the deployment confirmation dialog. Deployment will be
    possible unless there are items in `blocker` list.

Mixin Constructors
------------------

Fuel UI is using `React
<https://facebook.github.io/react/>`_ for views, so mixin constructors must
be React components. You should create a wrapper component if you want to use
some other library/framework:

.. code-block:: js

  ...
  constructor: React.createClass({
    componentDidMount: function() {
      // use jQuery to render contents
      $(this.refs.wrapper.getDOMNode()).html('Hello from a plugin!');
    },
    render: function() {
      return React.createElement('div', {ref: 'wrapper'});
    }
  })

Preprocessing of Plugins Code
-----------------------------

If a plugin developer sets `ui_build` field in `metadata.yaml` to true, then
the same transformations will be applied to the plugin which are applied to the
Fuel UI core code. Currently they are: JSX to JS compilation, LESS to CSS
compilation, minification and concatenation of code.

Handling multiple versions of a plugin
--------------------------------------

If there are multiple versions of a plugin installed, mixins will be used from
the plugin with the highest version at the time of environment creation.

Choosing Upgrade Strategy
-------------------------

The process of Fuel master node upgrade can affect UI plugin format
significantly. There are 2 options here:

* Tight coupling with the core code (with mixin types described in this
  proposal). Plugin may use core libraries, reusable components, styles. Mixins
  get data as Backbone models, can use their helper methods, interact with API
  without implementing their own data layer, authentication mechanism, etc.

  - Pros:

    + Due to reusing styles, plugins will look like other parts of Fuel UI.

    + Due to reusing code and libraries, size of plugin code can be really
      small and contain mostly business logic related to the plugin.

  - Cons:

    + There is high probability that plugin won't work correctly with the next
      version of Fuel UI after master node upgrade. Many things may be changed
      in the core UI: paths to reusable components, styles, Twitter Bootstrap
      version, React version, Backbone can be replaced with something else,
      API output can be changed, some cluster/networking modes can become
      deprecated, etc.

    + Due to the previous statement, some upgrade restrictions should be added.
      For example, it should be prohibited to upgrade from 7.0 to 7.1 if some
      environment is using some plugin with UI part for 7.0 until the same
      plugin for 7.1 is installed. And if development of some plugin is
      abandoned, it means that upgrade is not possible.

    + We need to determine some point in Fuel development process where we
      freeze major changes in Fuel UI so that plugin developers can adapt their
      plugins for the next Fuel version. I think this point should be around
      Feature freeze or Soft code freeze.

* Loose coupling with the core code. Mixins should operate with POJOs only.
  Using React components should be ok, but they should be rendered in iframes
  or in shadow DOM to avoid using core styles.

  - Pros:

    + Absence of a newer version doesn't block upgrading.

  - Cons:

    + It's not possible to reuse core code. Plugin writers should implement
      their own interaction with server (if needed), authentication, copy
      styles from core, etc.

    + It's not possible to reuse libraries from core. If plugin writers have to
      include another copies of Twitter Bootstrap and jQuery if they want to
      use them.

    + Extra JS API is needed (for example, to get current Keystone token,
      current locale, etc.)


Developing a Plugin
-------------------

It should be possible to develop UI plugins using `Nailgun fake mode
<https://docs.mirantis.com/fuel-dev/develop/nailgun/development/env.html#running-nailgun-in-fake-mode>`_.
After setting up a development environment, a process of creating a UI part for
a plugin "Sample Plugin" of version 1.0.0 should look like this:

* Developer should place UI part of a plugin (at least `plugin.js`) to
  `nailgun/static/plugins/<plugin_name>-<plugin_version>` directory. For the
  sample plugin the path should be
  `nailgun/static/plugins/sample-plugin-1.0.0`. Minimal `plugin.js` looks like
  this:

  .. code-block:: js

    define(function() {
      'use strict';
      return {
        mixins: [],
        translations: {}
      };
    });

* Developer should create a fixture for a plugin with `ui` field set to true:

  .. code-block:: json

    [
      {
        "pk": 1,
        "model": "nailgun.plugin",
        "fields": {
          "name": "sample-plugin",
          "title": "Sample Plugin",
          "version": "1.0.0",
          "package_version": "1.0.0",
          "description": "Just a sample plugin",
          "ui": true
        }
      }
    ]

* Developer should upload this fixture by running
  `./manage.py loaddata sample_plugin_fixture.json`

* After performing these actions `plugin.js` should be loaded and executed on
  the fake UI.

(TBD: packaging and stuff, testing on compressed UI)

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

Described above.

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

Fuel Plugin CI workers should have NPM dependencies installed to successfully
run FPB for plugins with UI parts.


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

* UI parts loader (should load plugin UI parts and register mixins and
  translations).

* Mixin registry (should have a list of all available mixins and filter mixins
  by environment and type).

* Mixin embedders (parts of code which add mixins: tab list renderer,
  deployment confirmation dialog).

* Nailgun modifications.

* FPB modifications to handle UI parts.

* Gulpfile modifications to build UI parts.

* Sample plugin with all mixin types.

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
