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

UI part of plugin is a directory which contains all required files: javascript
files, styles, images, etc. The plugin must also have `plugin.js` file in this
directory. `plugin.js` should be an AMD module which contains plugin metadata
and also has all other files as dependencies.

plugin.js should return an object:

.. code-block:: json

  {
    "mixins": [
      {
        "type": "cluster_tab",
        "attributes": {
          ...
        },
      },
      ...
    ],
    "translations": {
      ...
    },
    ...
  }

"mixins" field should contain a list of mixins that plugin adds into Fuel UI.
Mixin is a new entity which should be added to Fuel UI. It can be a new
cluster tab, a new page, etc. Every mixin has its type and a set of
attributes.
"translations" are i18next translations that are used in the plugin. They are
merged with existing translations when plugin is loaded.

Mixin types
-----------

TBD

Data model impact
-----------------

Plugin developer must set `ui` field in `metadata.yaml` of plugin to true so
UI can know that this plugin has UI part which must be loaded.

REST API impact
---------------

**GET /api/v1/plugins/**

Output should be modified to reflect `ui` flag. This API call should be made
auth exempt so UI could load plugins regardless of auth status.

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

Fuel plugin builder needs to be modified to support building of UI parts.
Modification is required for more or less complex plugins which rely on
libraries which are not included in minified UI (such as in-browser LESS and
JSX transformers). Also most plugins will require core Fuel UI code as they
need to reuse existing libraries, common components, utils, etc. So build
process would look like this:

* FPB gets path to fuel-web repo via command line parameters

* FPB puts UI parts of plugins to static/plugins/:plugin_name

* FPB runs `grunt build`

* FPB puts the results of the build (which is usually minifed plugin.js and
* other files which cannot be included to the build like images and fonts) to
* the .tar file

Upgrade impact
--------------

(TBD)

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

Nginx config should be modified to make UI parts of plugins available by url
`/static/plugins/:plugin_name`

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

(TBD)

* Include specific references to specs and/or blueprints in fuel, or in other
  projects, that this one either depends on or is related to.

* If this requires functionality of another project that is not currently used
  by Fuel, document that fact.

* Does this feature require any new library dependencies or code otherwise not
  included in Fuel? Or does it depend on a specific version of library?


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
