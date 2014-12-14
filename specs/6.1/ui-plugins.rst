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
tab is not sufficient, so support of custom UI modifications is required.

Proposed change
===============

Alternatives
------------

None

Format of UI part of plugin
---------------------------

UI part of plugin is a `ui_static` directory which contains all required
files: javascript files, styles, images, etc. The plugin must also have
`plugin.js` file in this directory. `plugin.js` should be a module in
Asynchronous Module Definition (AMD) format which contains plugin metadata and
also has all other files as dependencies.

.. code-block:: text

    .
    |-- tasks.yaml
    |-- metadata.yaml
    |-- ...
    `-- ui_static
        |-- plugin.js
        |-- module1.jsx
        |-- styles.less
        |-- ...
        `-- pic1.png

plugin.js should return an object:

.. code-block:: js

  {
    mixins: [
      {
        type: 'cluster_tab',
        attributes: {
          ...
        },
      },
      ...
    ],
    translations: {
      ...
    },
    ...
  }

* `mixins` field should contain a list of mixins that plugin adds into Fuel
  UI. Mixin is a new entity which should be added to Fuel UI. It can be a new
  cluster tab, a new page, etc. Every mixin has its type and a set of
  attributes.

* `translations` are translations in `i18next
  <http://i18next.com/pages/doc_features.html>`_ format that are used in the
  plugin. They are merged with existing translations when plugin is loaded.

Mixin types
-----------

There are 2 types of mixins: `global` mixins and `environment` mixins.
Global mixins affect the whole Fuel UI, while environment mixins are
environment-specific. If there are multiple versions of a plugin installed,
global mixin will be used from the plugin with the highest version. For
environment mixins, mixins will be used from the plugin with the highest
version at the time of environment creation.

cluster_tab
^^^^^^^^^^^

Type: `environment`

Used when a separate tab with complex UI is needed:

.. code-block:: js

  {
    type: 'cluster_tab',
    attributes: {
      name: 'fencing',
      after: 'settings',
      visible: function(cluster) {
        return cluster.get('mode') != 'multinode';
      },
      constructor: FencingTab
    }
  }

* `name` is a name of the tab. It will be used in URL for tab and for its
  icon.

* `after` is name of a tab after which the tab provided by the plugin should
  be inserted. If there are several plugins with same after field, then
  sorting by their names will be used to determine order.

* `visible` is a function which determines whehter tab is visible or not.
  Accepts cluster as a parameter.

* `constuctor` is a React component or Backbone.View which renders tab
  contents.

route
^^^^^

Type: `global`

Used when new global route needs to be added. A convenient way to add a new
page.

.. code-block:: js

  {
    type: 'route',
    attributes: {
      url: 'custom_route/:entity_id',
      handler: function() {
        app.loadPage(MyCustomPage);
      }
    }
  }

* `url` is a URL of the route in `Backbone.Router
  <http://backbonejs.org/#Router>`_ format.
* `handler` is a function which is called for this route.

(more mixin types TBD)
^^^^^^^^^^^^^^^^^^^^^^

Data model impact
-----------------

Plugin developer must set `ui` field in `metadata.yaml` of plugin to true so
UI can know that this plugin has UI part which must be loaded. Also plugin
developer may want to build (preprocess/minify) his plugin, in that case
`ui_build` must also be set to true.

REST API impact
---------------

**GET /api/v1/plugins/**

2 new boolean fields should be added to output: `ui` and `enabled`.

The `ui` flag is set to true for plugins which have UI part which should be
loaded.
The `enabled` flag is set to true when a plugin is enabled. This flag should
be editable by PUT/PATCH requests.

.. code-block:: json

  [
    {
      "id": 1,
      "name": "plugin_name",
      "version": "1.0",
      ...
      "ui": true,
      "enabled": true
    }
  ]

**GET /api/v1/clusters/:id/**

A new field `plugins` should be added to show a list of plugin ids which are
used for the environment. It would be used to determine which mixins should be
added.

.. code-block:: json

  [
    {
      "id": 1,
      "name": "Env #1",
      ...
      "plugins": [11, 13, 17]
    }
  ]

Plugin Loading Process Concerns
-------------------------------

Plugin loading process seems to be pretty straightforward, but there are two
obstacles:

* Plugin list can only be obtained and UI parts can be loaded only if the user
  is authenticated

* Plugins can be disabled - do we need to load UI parts in that case?

As for authentication issue, we can try to load UI parts after authentication.
It's not clear yet if this approach has some issues and if it has, then plugin
list API should be made auth exempt like it is done for version API. If there
are no issues, then in case if plugin adds some styles, they will be added
only after authentication. It is also obvious that in this case login page
cannot be modified by plugins.

As for disabling of plugins, it seems that UI parts of disabled plugins should
also be loaded. Even plugin is disabled, some existing enivronments could be
created when some of disabled plugins were enabled. This means that for such
environments environment mixins should still be added. Global mixins from
disabled plugins shouldn't be added.

Fuel Plugin Builder impact
--------------------------

Fuel plugin builder needs to be modified to support UI parts of plugins. If
`ui_build` flag is not set to true, nothing changes in the flow and
`ui_static` dir appears in the resulting .tar file without changes. But this
works only for very simple plugins and more or less complex plugins which rely
on libraries which are not included in minified UI (such as in-browser LESS
and JSX transformers) will require preprocessing. Also most plugins will
require core Fuel UI code as they need to reuse existing libraries, common
components, utils, etc. So for plugins with `ui_build` flag build process
should look like this:

* FPB gets path to fuel-web repo via command line parameters

* FPB puts UI part of plugins from `ui_static` dir to
  `static/plugins/<plugin_name>-<plugin_version>`

* FPB runs `grunt build`

* FPB puts the results of the build (which is usually minifed plugin.js and
  other files which cannot be included to the build like images and fonts) to
  the .tar file

Upgrade impact
--------------

None

Security impact
---------------

* plugin can inject any Javascript code in Fuel UI

Notifications impact
--------------------

None

Other end user impact
---------------------

Loading time of UI with lots of plugins can slightly increase.

Performance Impact
------------------

There will be slight performance impact as mixins and translations provided by
plugin will be registered and handled.

Other deployer impact
---------------------

Nginx config should be modified to make `ui_static` dir of plugins available
by url `/static/plugins/<plugin_name>-<plugin_version>`

Developer impact
----------------

New UI code should be written to be easily extendable by mixins.

Implementation
==============

Assignee(s)
-----------

Primary assignee:
  vkramskikh@mirantis.com

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

For this feature it is almost essential to have JS unit tests. So we need to
finish integration with Intern in this release.

Documentation Impact
====================

(TBD)

What is the impact on the docs team of this change? Some changes might require
donating resources to the docs team to have the documentation updated. Don't
repeat details discussed above, but please reference them here.


References
==========

(TBD)

Please add any useful references here. You are not required to have any
reference. Moreover, this specification should still make sense when your
references are unavailable. Examples of what you could include are:

* Links to mailing list or IRC discussions

* Links to relevant research, if appropriate

* Related specifications as appropriate

* Anything else you feel it is worthwhile to refer to
