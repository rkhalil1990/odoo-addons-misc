# -*- encoding: utf-8 -*-
##############################################################################
#
#    Point Of Sale - Restaurant Extra module for Odoo
#    Copyright (C) 2013-Today GRAP (http://www.grap.coop)
#    @author Sylvain LE GAL (https://twitter.com/legalsylvain)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, tools
from openerp.tools.translate import _


class PosCoversReport(models.Model):
    _name = 'pos.covers.report'
    _auto = False
    _table = 'pos_covers_report'

    _WEEK_DAY = [
        (1, _('Monday')),
        (2, _('Tuesday')),
        (3, _('Wednesday')),
        (4, _('Thursday')),
        (5, _('Friday')),
        (6, _('Saturday')),
        (7, _('Sunday')),
    ]

    company_id = fields.Many2one(comodel_name='res.company', string='Company')

    floor_id = fields.Many2one(comodel_name='restaurant.floor', string='Floor')

    user_id = fields.Many2one(comodel_name='res.users', string='User')

    date = fields.Datetime(string='Date')

    week_date = fields.Datetime(string='Week (Date Format)')

    month_date = fields.Datetime(string='Month (Date Format)')

    date_txt = fields.Char(string='Day (Text Format)')

    week_txt = fields.Char(string='Week (Text Format)')

    month_txt = fields.Char(string='Month (Text Format)')

    week_day = fields.Selection(string='Week Day', selection=_WEEK_DAY)

    covers_total = fields.Integer(string='Covers Total')

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                SELECT
                    req.id,
                    req.company_id,
                    req.floor_id,
                    req.user_id,
                    req.date as date,
                    DATE_TRUNC('week',req.date) as week_date,
                    DATE_TRUNC('month',req.date) as month_date,
                    req.date as date_txt,
                    DATE_TRUNC('week',req.date) as week_txt,
                    DATE_TRUNC('month',req.date) as month_txt,
                    CASE
                        WHEN extract(dow from req.date) = 0 THEN 7
                        ELSE extract(dow from req.date)
                        END as week_day,
                    req.covers_total
                FROM (
                    SELECT
                        MIN(po.id) AS id,
                        po.company_id,
                        po.floor_id,
                        po.user_id,
                        DATE_TRUNC('day',po.date_order) AS date,
                        SUM(po.covers) as covers_total
                    FROM
                        pos_order as po
                    WHERE
                        po.state not in ('cancel', 'draft')
                    GROUP BY
                        company_id,
                        floor_id,
                        user_id,
                        date
                    ) as req
                ORDER BY
                    date desc
        )""" % (self._table))
