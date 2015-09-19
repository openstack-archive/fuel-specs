================
 Team Structure
================

This document describes the structure of the Fuel team and how it is used to
organize code review, design discussions, and overall technical decision making
process in the Fuel project.

Problem Description
===================

Code review is the primary tool for day to day interactions between Fuel
contributors. Problems with code review process can be grouped into two
buckets.

It is hard to get code reviewed and merged:

1. It is hard to find subject matter experts and core reviewers for the
   specific part of codebase, especially if you are new to the project.

2. Contributor sometimes receives contradicting opinions from different
   reviewers, including cores.

3. Without an assigned core reviewer, it is hard to guide a feature through
   architectural negotiations and code review process to landing the code into
   master.

4. Some commits are waiting for a long time for a reviewer.

Quality of code review itself could be better:

5. Reviews are not thorough enough. Instead of examining the whole patch set
   and identifying all problems in one shot, a reviewer can leave a -1 vote
   after identifying only one minor problem. This increases number of patch
   sets per commit, and demotivates contributors.

6. Some of the core reviewers decreased their involvement, and so number of
   reviews has dropped dramatically. However, they still occasionally merge
   code.

7. As a legacy of the past, we still have old core reviewers being able to
   merge code in all Fuel repos. All new cores have core rights only for single
   repo, which is their primary area of expertise.

Having well defined areas of ownership in Fuel components addreses most of
these problems: from making it easier to identify the right reviewers for your
code, to prioritizing code review work so that core reviewers can spend more
attention on smaller number of commits.

Proposed Policy
===============

Definitions
-----------

Contributor:
    Submitter of a code review, who doesn't necessarily work on Fuel regularly,
    may not be familiar with the team structure or with Fuel codebase.

Maintainer:
    Subject matter expert in certain Fuel area of code, which they regularly
    contribute to and review code of other contributors into this area. For
    example: network checker or Nailgun agent would have their own lists of
    maintainers.

    List of maintainers for different parts of a Fuel git repository is
    provided in a MAINTAINERS file at the top level of that repository. A
    repository that contains multiple components may have multiple MAINTAINERS
    files in the component subdirectories.

Core Reviewer:
    Maintainer who has maintained high level of contribution and high quality
    of code reviews and was promoted to core reviewers team by consensus of
    other core reviewers of the same Fuel component.

Component Lead:
    Defines architecture of a particular module or component in Fuel, resolves
    technical disputes in their area of responsibility. All design specs that
    impact a component must be approved by the corresponding component lead.

Fuel PTL:
    Project Team Lead in its OpenStack standard definition. Delegates most of
    the review and design work to component leads, resolves technical disputes
    across components and for components that don't have dedicated component
    leads.

Code Review Workflow
--------------------

Typical commit goes through the following code review stages:

0. Contributor makes sure their commit receives no negative votes from CI. When
   possible, contributor also invites peers to review their commit.

1. Contributor finds the maintainers for the areas of the code modified by
   their commit in the MAINTAINERS file, and invites them to the review.

2. Once maintainer is ready to add +1 code review vote to the commit, they
   invite core reviewers of the modified component to the review.

3. A commit that has a +2 vote from a core reviewer can be merged by another
   core reviewer, or by the component lead of the modified component.

Governance Process
------------------

Fuel PTL is elected twice a year following the same cycle and rules as other
OpenStack projects.

Fuel component leads are elected twice a year immediately after PTL elections,
following the same process. Same person can't be PTL and component lead in the
same cycle.

Following Fuel components have elected leads:

* fuel-library (code: fuel-library)

* fuel-python (code: fuel-web except fuel-ui that currently lives under
  fuel-web/nailgun/static)

In other repositories, technical decisions are made by consensus of core
reviewers, and disputes are resolved by Fuel PTL.

Core reviewers are approved by consensus of existing core reviewers, following
the same process as with other OpenStack projects. Core reviewers can
voluntarily step down, or be removed by consensus of existing core reviewers.
Separate core reviewers list is maintained for each Fuel git repository.

Maintainers are defined by the contents of the MAINTAINERS files in Fuel git
repositories, following the standard code review process. Any contributor can
propose an update of a MAINTAINERS file; a core reviewer can approve an update
that has a +2 from another core reviewer; if the update adds new maintainers,
it must also have +1 votes from all added maintainers.

Alternatives
============

Flat project structure
----------------------

Many other OpenStack projects keep a flat team structure: one elected PTL, and
a single list of core reviewers for the whole project. The advantage is a more
simple and straightforward governance process. The disadvantages are described
in the problem description.

Split Fuel into sub-projects
----------------------------

An alternative way to address the problem of insufficiently granular ownership
is to split Fuel into several sub-projects with independent governance. The
advantage is not having to introduce the role of a component lead that doesn't
exist in other OpenStack projects. The disadvantage is even more governance
overhead, and having to involve TC in cross-sub-project dispute resolution.

Implementation
==============

Author(s)
---------

Primary author: mihgen (Mike Scherbakov)

Other contributors: angdraug (Dmitry Borodaenko)

Milestones
----------

The current policy was put in place for Mitaka.

Work Items
----------

N/A

References
==========

* Code review process in Fuel and related issues (by Mike Scherbakov):
  http://lists.openstack.org/pipermail/openstack-dev/2015-August/072406.html

* Fuel Review Inbox (by Dmitry Borodaenko):
  http://git.openstack.org/cgit/stackforge/gerrit-dash-creator/tree/dashboards/fuel.dash

* Fuel contribution statistics (Stackalytics):
  http://stackalytics.com/report/contribution/fuel-group/90

* Open Reviews for Fuel (by Russel Bryant):
  http://russellbryant.net/openstack-stats/fuel-openreviews.html

.. note::

  This work is licensed under a Creative Commons Attribution 3.0
  Unported License.
  http://creativecommons.org/licenses/by/3.0/legalcode
