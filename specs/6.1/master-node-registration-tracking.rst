==========================================
Fuel downloads and registrations - functional requirements
==========================================

Problem description
===================

(1) We would like to proactively identify failed deployments based on product stats, but we are currently unable to identify which stats corresponds to which user account in SFDC. Also, even though we use our free 30-day support as a motivation to register, it doesn’t work very well because the registration process is tedious.

(2) In addition, if user has multiple environments and needs help with one of them, identifying the corresponding master-node is not straightforward - the Master Node UID is burried in config files. This negatively affects user experience and creates additional complexity on support side.

Proposed change
===============


Concept description
------------

We can solve this problem (1) by mapping the stats of fuel master-nodes with SFDC accounts by email and triggering 30-day countdown automatically upon successful installation of the master-node, so there’s no need to manually register only after the product is deployed. To solve problem (2) we will display Master Node UID in Support tab of Fuel Dashboard UI. In addition, we will also display registration status, so if master node is already registered, it’s clear for the user.

User experience and back-end logic
------------

Obtaining ISO directly from Mirantis

User fills in the download form on software.mirantis.com and clicks Download Now button. Once the button is clicked, the following is done:

User account is automatically created in the background. Account credentials:
Login=user email
Password=randomly generated 8-character combination.
Email notification is sent to user with account credentials
User account is created in SFDC (same logic)
Download links are displayed

Once the download links are displayed, user downloads the ISO and completes Master Node installation. 

Master Node UI Welcome screen

Once user logs into Master Node UI for the first time, we show the updated “Welcome to Mirantis Openstack” screen with sign-in/sign-up prompt (instead of Name/Email/Company fields) with product stats checkboxes.

Checkboxes description:

There are 2 checkboxes for product stats - Anonymous (triggers sending stats reports) and Personal (adds Name/Company/Email to the stats reports). Visually, personal checkbox should be part of sign-in/sign-up prompt. If Personal checkbox is checked, Anonymous is checked automatically.

Sign-in/sign up prompt description:

Sign-in. If user obtained the ISO from Mirantis web site, he already has the account, so he just signs in with his login/password.

Sign-up. If the ISO was obtained from an external source (e.g. partner/friend/torrent/etc), user can sign up by right from within the UI by completing the sign-up form (same fields as on download page). Once the form is completed, the account is created the same way as on the download page and the credentials are emailed to user. User then signs in with the emailed credentials. 

(!) If we detect that we already have the account with associated email address, we email the password from this particular account with displaying a message like “looks like you’re already registered, we resent you your password, please check email and log in”. No updates are made to the account on server side, even if user submitted different name/phone/etc.

Lost Password link. The prompt also contains "lost password?" link which can be used for restoring lost/forgotten password. User clicks the link and enters his email address. If there is an account with such email, we send the password to this email (and display a message like “we resent your password, please check your email”). If there’s no account associated with the email, we display a message like “we don’t have an account with such an email, please create one”.

Signing in

Once user signs in, his Master Node becomes registered and we start counting 30-day support period. No additional actions required.

(!) Sign-in/sign-up is optional, so if user doesn’t want to register, he can skip this step and start using Fuel immediately. If the Personal stats checkbox is checked, but user has not signed in, UI displays a text like “we’ll be sending personal stats once you log in” near the checkbox. Checking Personal stats checkbox does not prevent user from proceeding without signing in, this just means that we don’t send personal stats. User can sign in / sign up later at any time through Support Tab in Fuel Dashboard (see below).

Credentials for support account

(!) User must be able to log in to his support account with the same credentials that were used to register the product (single sign-on).

Support Tab in Fuel Dashboard UI

If user skipped sign-in step at the welcome screen, the Support Tab should say something like “product is not registered” and display sign-in/sign-up form (same logic as in Welcome Screen, including “forgot password” link).

Checkboxes should have the same state as on Welcome Screen. If Personal checkbox is checked, but the user hasn’t signed in, UI displays a text like “we’ll be sending personal stats once you log in” near the checkbox (just like on Welcome Screen).

Once user signed in, we show the following:

Registration status in Support tab of Fuel Dashboard UI like “This Master Node is registered to Eugene Bogdanov (ebogdanov@mirantis.com), Master Node UID is 223322223322.
Information about support subscription (trial/paid, how many days left).

(!) User cannot sign out once he signed in (to avoid cheating with support period).

Notes and remarks

No UI changes to download page - same fields and same download workflow. No password needed to access download links.
We have request from support to encourage users to submit corporate emails (not linke @yahoo/@gmail/etc). In response to this request, we will rename the field "email" to "corporate email" and add some wording that discourages from using such kind of emails like “for best experience please avoid using emails like @yahoo/@gmail/etc”
We assume that by the time we launch this feature we will have finished support transition to SFDC.
Mirantis OpenStack Express and feeding product stats data to SFDC is out of scope for this iteration. Our goal now is to ensure we can unambiguously identify product stats with SFDC accounts, we'll think about further steps later on.

Trial support period countdown:

We map 30-day free support to account. Countdown starts since the first Master Node is registered. If more Master Nodes are registered later on, we DO NOT reset the countdown.



Error response workflow for sign-in/sign-up form:

Sign-in/sign-up procedure can fail for 2 reasons: lack of internet connection on user side or problems on Mirantis server side. So,

If no internet connection available, we encourage user to log in to Fuel Master Node from a machine that has internet connection. 
If internet connection is available, but Fuel can’t connect to our servers, we say that something is broken on the server side and encourage user to try again later. Simultaneously Fuel can send an alert to a dedicated alias so we are notified that something is broken with our registration procedure.


Alternatives
------------

1. Registration codes/files VS account email

It was originally proposed that we provide users with registration codes/files generated with the start of ISO download and then prompt users to submit these registration codes/files during installation (as originally proposed in https://mirantis.jira.com/browse/PROD-198). I see no point in this because these registration codes will ultimately still be mapped to accounts so essentially this complicates the whole process both to user experience and to back-end logic without adding value.

2. Support period - map to account VS map to particular installation

We can map support period to the account (and count the support period since the first installation) or give 30 day-support to each particular installation. I see no issues going with either variant, but I think it’s up to sales to decide.
UPDATE: Upon Paul’s input, we map 30-day free support to account. Countdown starts since the first Master Node is registered. If more Master Nodes are registered later on, we DO NOT reset the countdown.


Data model impact
-----------------


TBD

REST API impact
---------------

TBD

Upgrade impact
--------------

TBD

Security impact
---------------

TBD

Notifications impact
--------------------

TBD

Other end user impact
---------------------

TBD

Performance Impact
------------------

Not expected. TBC

Other deployer impact
---------------------

Not expected. TBC

Developer impact
----------------

Not expected. TBC

Implementation
==============

Assignee(s)
-----------
Who is leading the writing of the code? Or is this a blueprint where you're
throwing it out there to see who picks it up?

If more than one person is working on the implementation, please designate the
primary author and contact.

Primary assignee:
<ebogdanov>

Other contributors:
  <None so far>

Work Items
----------

Work items or tasks -- break the feature up into the things that need to be
done to implement it. Those parts might end up being done by different people,
but we're mostly trying to understand the timeline for implementation.


Dependencies
============




Testing
=======

TBD.

Documentation Impact
====================

We might need to describe the registration process in the documentation. Not sure it’s obligatory though since the process is self-explanatory from user standpoint.


References
==========

Jira task: https://mirantis.jira.com/browse/PROD-198

