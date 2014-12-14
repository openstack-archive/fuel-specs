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

`mixins` field should contain a list of mixins that plugin adds into Fuel UI.
Mixin is a new entity which should be added to Fuel UI. It can be a new
cluster tab, a new page, etc. Every mixin has its type and a set of
attributes.

`translations` are translations in `i18next
<http://i18next.com/pages/doc_features.html>`_ format that are used in the
plugin. They are merged with existing translations when plugin is loaded.

Mixin types
-----------

cluster_tab
^^^^^^^^^^^^

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

`name` is a name of the tab. It will be used in URL for tab and for its icon.
`after` is name of a tab after which the tab providede by the plugin should be
inserted. If there are several plugins with same after field, then sorting by
their names will be used to determine order.
`visible` is a function which determines whehter tab is visible or not.
Accepts cluster as a parameter.
`constuctor` is a React component or Backbone.View which renders tab contents.

(more mixin types TBD)
^^^^^^^^^^^^^^^^^^^^^^

Data model impact
-----------------

Plugin developer must set `ui` field in `metadata.yaml` of plugin to true so
UI can know that this plugin has UI part which must be loaded. Also plugin
developer may want to build (preprocess/minify) his plugin, in that case
`build_ui` must also set to true.

REST API impact
---------------

**GET /api/v1/plugins/**

Boolean `ui` flag should also be added to output so UI would know that a
plugin has UI part which should be loaded. `plugin.js` file. This API call
should be made auth exempt so UI could load plugins regardless of auth status.

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

Fuel Plugin Builder impact
--------------------------

Fuel plugin builder needs to be modified to support UI parts of plugins. If
`build_ui` flag is not set to true, nothing changes in the flow and
`ui_static` dir appears in the resulting .tar file without changes. But this
works only for very simple plugins and more or less complex plugins which rely
on libraries which are not included in minified UI (such as in-browser LESS
and JSX transformers) will require preprocessing. Also most plugins will
require core Fuel UI code as they need to reuse existing libraries, common
components, utils, etc. So for plugins with `build_ui` flag build process
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

* /api/v1/plugins/ will be made auth exempt

* plugin can inject any Javascript code in Fuel UI

Notifications impact
--------------------

None

Other end user impact
---------------------

None

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

(TBD)

Please discuss how the change will be tested. It is assumed that unit test
coverage will be added so that doesn't need to be mentioned explicitly,
but discussion of why you think unit tests are sufficient and we don't need
to add more functional tests would need to be included.

Is this untestable in gate given current limitations (specific hardware /
software configurations available)? If so, are there mitigation plans (3rd
party testing, gate enhancements, etc).


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
