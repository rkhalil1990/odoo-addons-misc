# -*- encoding: utf-8 -*-
##############################################################################
#
#    Point of Sale - Reporting for Odoo
#    Copyright (C) 2013-Today GRAP (http://www.grap.coop)
#    @author Julien WESTE
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
from openerp.addons import decimal_precision as dp


class PosDailyReport(models.Model):
    _name = 'pos.daily.report'
    _auto = False
    _table = 'pos_daily_report'

    date = fields.Date(string='Date')

    date_char = fields.Char(string='Date (Text Format)')

    company_id = fields.Many2one(comodel_name='res.company', string='Company')

    amount_tax_excluded = fields.Float(
        string='Net Sales', digits=dp.get_precision('Product Price'))

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""
            create or replace view %s as (
                    SELECT
                        min(po.id) as id,
                        to_char(po.date_order,'YY/MM/DD Dy') as date_char,
                        date_trunc('day',po.date_order) as date,
                        po.company_id AS company_id,
                        sum(pol.price_subtotal) as amount_tax_excluded
                    FROM
                        pos_order po
                        INNER JOIN pos_order_line pol
                            ON po.id = pol.order_id
                    WHERE
                    po.state not in ('draft')
                    AND po.create_date > now() - interval '1 year'
                    GROUP BY
                        po.company_id,
                        date,
                        date_char
        )""" % (self._table))
        

#                        round(sum(pol.price_subtotal),2) as amount_tax_excluded
