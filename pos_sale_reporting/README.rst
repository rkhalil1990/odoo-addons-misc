.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3

====================================================
Add reports merging 'Sale' and 'Point of Sale' Datas
====================================================

Add a graph report view in the Report menu to merge sale and point of sale Net
informations:

* Net Sales Evolution;
* Net Sales by Category (3 levels);
* Top Products saled;

Technical Information
---------------------

* As this module merge point of sale and sale information, the sql views are
  using UNION statement; So, performance are very bad, and to avoid that this
  module create MATERIALIZED view;
* So information doesn't take into account, last day sales;
* A cron Task update the materialized view each night;

**you so need Postgresql 9.3+ to install this module;**


Ref:
----
http://stackoverflow.com/questions/18134798/why-does-my-view-in-postgresql-not-use-the-index

.. image:: /pos_sale_reporting/static/description/sale_and_pos_net_sale.png


Credits
=======

Contributors
------------

* Julien WESTE;
* Sylvain LE GAL (https://twitter.com/legalsylvain);
