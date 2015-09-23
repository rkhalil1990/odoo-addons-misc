.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3

=====================================
Add extra informations for restaurant
=====================================

* Possibility to set table and covers number in back-office view;

Technically
-----------
* Add a model 'restaurant.table' and 'restaurant.floor' managed in PoS
  configuration menu;
* Add a field 'table_id' and 'covers' on 'pos.order' model;
* Add a field 'max_covers' on 'pos.config' model;

Screenshots
-----------

* Reports

.. image:: /pos_restaurant_extra/static/description/covers_daily_evolution.png
.. image:: /pos_restaurant_extra/static/description/covers_monthly_evolution.png
.. image:: /pos_restaurant_extra/static/description/covers_weekly_distribution.png
.. image:: /pos_restaurant_extra/static/description/covers_weekly_evolution.png


Roadmap / Limit
---------------

* Possibility to set table and covers number in front-office view;

Credits
=======

History
-------

* Part of this module has been **ported** from 'pos_restaurant' V7.0 module of
  **GRAP**;
* Other part of this module is a **backport** works from 'pos_restaurant' V9.0
  of **Odoo SA**;
* The name of this module is 'pos_restaurant_extra' because in Odoo 8.0, there
   is a module named 'pos_restaurant', but it doesn't belong table / floor
   model, nor covers concept;

* For instance, this module works mainly like the V7.0 module, but using models
of the official V9.0 module, to make more easy futur migration;

Contributors
------------
* Odoo SA (https://www.odoo.com);
* Sylvain LE GAL (https://twitter.com/legalsylvain);
