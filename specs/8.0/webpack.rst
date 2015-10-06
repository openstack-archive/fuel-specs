..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

====================
Migration to Webpack
====================

https://blueprints.launchpad.net/fuel/+spec/webpack

Currently we use require.js module loader, AMD modules format and r.js build
system. We've been using these technologies from the very beginning (more than
3 years ago!) and now they seems to be outdated and causing lots of problems
during development. Migration to webpack is going to solve most of them.

--------------------
Problem description
--------------------

Current require.js-based build approach has the following issues:

* Different approaches for nodejs and in-browser compilation of styles and JS
  - this doubles efforts to support them and doesn't guarantee that a change
  made in dev environment will work in production. Some transformations (like
  CSS-autoprefixer) are even not possible (or very hard to setup) in browser.
  Webpack uses single approach for every environment.

* Long in-browser compilation time. On my laptop I have to wait about 10-15
  seconds after hitting F5 for loading and compilation. Webpack allows hot
  updates without refresh which take effect in 1-2 seconds.

* Inability to use original LESS styles from twitter bootstrap. With
  require.js we have to use precompiled CSS styles (attempting to load LESS
  styles directly results in extra 20s of compilation time). With webpack we
  can use original styles with minimal impact on performance.

* With require.js too granular modules may lead to longer loading
  times. Thus we currently try to put as many related stuff to a single module
  as possible, which has impact on unit-testing as we usually expose only 1
  component from a module. Webpack will eliminate such limitation.

* ES2015 - webpack allows us to write code using ES2015 syntax and use ES2015
  modules (official JS modules standard). It's hardly achievable with
  require.js - we have to use AMD and ES5.


----------------
Proposed changes
----------------

Web UI
======

* Replace require.js build stack with webpack.

* Replace Intern for unit-tests with Karma: Intern doesn't have support for
  wepback, only AMD modules are supported.

* Set up webpack-dev-server for developer convenience - it provides lots of
  useful options such as hot reloading, incremental builds, etc.

Nailgun
=======

Data model
----------

None


REST API
--------

None


Orchestration
=============

RPC Protocol
------------

None


Fuel Client
===========

None


Plugins
=======

None


Fuel Library
============

None


------------
Alternatives
------------

* Do nothing and keep require.js stack.

* Use CommonJS/browserify - though for our project setup would be more
  complicated and would miss some webpack-specific features (like React hot
  reloading)


--------------
Upgrade impact
--------------

None


---------------
Security impact
---------------

None


--------------------
Notifications impact
--------------------

None


---------------
End user impact
---------------

None


------------------
Performance impact
------------------

* Applying changes in dev mode will become much faster due to hot reloads and
  incremental builds.

* Unit tests will run slower - build is needed before starting the tests.

* Production UI build will become ~2 times faster.


-----------------
Deployment impact
-----------------

None


----------------
Developer impact
----------------

Developer must manually compile UI by running `gulp build` after fetching
updates - otherwise previously compiled UI will be used. As an alternative,
developer may want to use webpack-dev-server.


--------------------------------
Infrastructure/operations impact
--------------------------------

None


--------------------
Documentation impact
--------------------

Development documentation should be updated accordingly.


--------------------
Expected OSCI impact
--------------------

Quite a few new NPM packages (webpack itself, loaders, etc.) should be added.

--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  vkramskikh@mirantis.com

Other contributors:
  None

Mandatory design review:
  vkramskikh@mirantis.com
  jkirnosova@mirantis.com
  astepanchuk@mirantis.com


Work Items
==========

* Remove require.js artifacts and make build work.

* Set up build task.

* Set up dev-server task.

* Set up karma for unit tests.


Dependencies
============

None


------------
Testing, QA
------------

UI functional tests involve UI compression, so after switching to webpack they
must work without any changes.


Acceptance criteria
===================

* There should be no dependency on require.js.

* UI unit tests should work.

* UI functional tests should work.

* Development documentation should be updated.

* Development server with live reload should work.


----------
References
----------

http://webpack.github.io/
