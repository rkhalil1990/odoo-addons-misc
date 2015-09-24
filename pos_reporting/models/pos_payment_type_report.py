# -*- encoding: utf-8 -*-
##############################################################################
#
#    Point of Sale - Reporting for Odoo
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


class PosPaymentTypeReport(models.Model):
    _name = 'pos.payment.type.report'
    _auto = False
    _table = 'pos_payment_type_report'

    company_id = fields.Many2one(
        comodel_name='res.company', string='Company')

    journal_id = fields.Many2one(
        comodel_name='account.journal', string='Journal')

    month = fields.Datetime('Month')
#    size=7, readonly=True
    total = fields.Float(string='Total (Taxes Included)')

    average = fields.Float(string='Average (Taxes Included)')

    quantity = fields.Integer(string='Quantity')

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                SELECT
                    MIN(absl.id) AS id,
                    absl.company_id,
                    absl.journal_id,
                    absl.month,
                    SUM(absl.amount) AS total,
                    AVG(absl.amount) AS average,
                    COUNT(*) as quantity
                FROM (
                    SELECT
                        absl.id,
                        absl.journal_id,
                        absl.pos_statement_id,
                        absl.date,
                        absl.company_id,
                        absl.amount,
                        DATE_TRUNC('month', date::timestamp) AS month
                    FROM account_bank_statement_line AS absl
                    ) AS absl
                LEFT OUTER JOIN account_journal AS aj
                    ON aj.id = absl.journal_id
                WHERE
                    absl.journal_id IS NOT NULL
                    AND absl.pos_statement_id IS NOT NULL
                GROUP BY
                    absl.company_id,
                    absl.journal_id,
                    absl.month
                ORDER BY
                    absl.company_id,
                    absl.journal_id,
                    absl.month
        )""" % (self._table))
