# -*- encoding: utf-8 -*-
##############################################################################
#
#    Stock - Internal Use Of Products for Odoo
#    Copyright (C) 2013 GRAP (http://www.grap.coop)
#    @author Julien WESTE
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

from openerp.osv.orm import Model
from openerp.osv import fields, osv
from openerp.tools.translate import _
import time




class InternalUse(Model):
    _name = 'internal.use'
    _order = 'date_done desc, name'

    _INTERNAL_USE_STATE = [
        ('draft', 'New'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
    ]

    # Columns section
    def _get_amount(self, cr, uid, ids, name, args, context=None):
        res = {}
        for use in self.browse(cr, uid, ids, context=context):
            amount = 0
            for line in use.line_ids:
                amount += line.subtotal
            res[use.id] = amount
        return res

    def _get_internal_use_from_line(self, cr, uid, ids, context=None):
        """Return Internal Use ids depending on changes of Lines"""
        res = []
        line_obj = self.pool['internal.use.line']
        lines = line_obj.browse(cr, uid, ids, context=context)
        return list(set(line.internal_use.id for line in lines))

    _columns = {
        'name': fields.char(
            'Name', size=64, required=True),
        'description': fields.char(
            'Description', size=128,
            states={
                'done': [('readonly', True)]}),
        'date_done': fields.date(
            'Date', required=True,
            states={
                'done': [('readonly', True)],
                'confirmed': [('readonly', True)]},),
        'internal_use_case': fields.many2one(
            'internal.use.case', 'Case', required=True,
            states={
                'done': [('readonly', True)],
                'confirmed': [('readonly', True)]}),
        'company_id': fields.related(
            'internal_use_case', 'company_id',
            type='many2one', relation='res.company', string='Company',
            readonly=True, store=True),
        'state': fields.selection(
            _INTERNAL_USE_STATE, 'Status', readonly=True,),
        'line_ids': fields.one2many(
            'internal.use.line', 'internal_use', 'Lines',
            states={
                'done': [('readonly', True)],
                'confirmed': [('readonly', True)]}),
        'picking_id': fields.many2one(
            'stock.picking', 'Picking', readonly=True),
        'stock_move_ids': fields.related(
            'picking_id', 'move_lines',
            type='many2many', relation='stock.move', string='Stock moves'),
        'account_move_id': fields.many2one(
            'account.move', 'Account Moves', readonly=True),
        'amount': fields.function(
            _get_amount, string='Total Amount Tax excluded',
            type='float', store={
                'internal.use': (
                    lambda self, cr, uid, ids, context=None: ids,
                    ['line_ids', 'state'], 20),
                'internal.use.line': (
                    _get_internal_use_from_line, ['subtotal'], 20),
            }),
    }

    # Defaults section
    _defaults = {
        'name': lambda obj, cr, uid, context: '/',
        'state': 'draft',
        'date_done': lambda *a: time.strftime('%Y-%m-%d'),
    }

    # Overload Section
    def create(self, cr, uid, vals, context=None):
        sequence_obj = self.pool['ir.sequence']
        vals['name'] = sequence_obj.get(cr, uid, 'internal.use')
        return super(InternalUse, self).create(cr, uid, vals, context=context)

    def copy_data(self, cr, uid, id, default=None, context=None):
        default = default and default or {}
        default.update({'move_ids': [], 'line_ids': []})
        return super(InternalUse, self).copy_data(
            cr, uid, id, default, context=context)

    def unlink(self, cr, uid, ids, context=None):
        for use in self.browse(cr, uid, ids, context=context):
            if use.state != 'draft':
                raise osv.except_osv(
                    _('User Error!'), _('You can only delete draft uses.'))
        return super(InternalUse, self).unlink(cr, uid, ids, context=context)

    # Actions section
    def action_confirm(self, cr, uid, ids, context=None):
        """ Confirm the internal use and writes its finished date"""
        account_move_obj = self.pool.get('account.move')
        product_obj = self.pool.get('product.product')
        stock_move_obj = self.pool.get('stock.move')
        picking_obj = self.pool.get('stock.picking')
        period_obj = self.pool.get('account.period')

        if context is None:
            context = {}

        for iu in self.browse(cr, uid, ids, context=context):
            # Create picking
            picking_value = {
                'type': 'out',
                'move_type': 'direct',
                'origin': iu.name,
                'invoice_state': 'none',
                'company_id': iu.company_id.id,
            }
            picking_id = picking_obj.create(cr, uid, picking_value)

            # Create stock moves
            for line in iu.line_ids:
                qty = line.product_qty
                if qty:
                    stock_move_value = {
                        'name': 'Internal Use Line/' + str(line.id),
                        'product_id': line.product_id.id,
                        'picking_id': picking_id,
                        'product_uom': line.product_uom_id.id,
                        'date': iu.date_done,
                    }

                    if qty > 0:
                        stock_move_value.update({
                            'product_qty': qty,
                            'location_id':
                            iu.internal_use_case.location_from.id,
                            'location_dest_id':
                            iu.internal_use_case.location_to.id,
                        })
                    else:
                        stock_move_value.update({
                            'product_qty': -qty,
                            'location_id':
                            iu.internal_use_case.location_to.id,
                            'location_dest_id':
                            iu.internal_use_case.location_from.id,
                        })
                stock_move_obj.create(cr, uid, stock_move_value)

            # Create account move
            period_id = period_obj.find(
                cr, uid, dt=iu.date_done, context=context)[0]
            aml_values = {
                'name': iu.name,
                'date': iu.date_done,
                'period_id': period_id,
                'account_id': iu.internal_use_case.expense_account.id,
            }
            if iu.amount >= 0:
                aml_values.update({
                    'debit': iu.amount,
                })
            else:
                aml_values.update({
                    'credit': -iu.amount,
                })
            account_move_lines = [(0, 0, aml_values)]

            for line in iu.line_ids:
                aml_values = {
                    'name': line.product_id.name,
                    'date': iu.date_done,
                    'period_id': period_id,
                    'product_id': line.product_id.id,
                    'product_uom_id': line.product_uom_id.id,
                    'quantity': line.product_qty,
                    'account_id':
                    product_obj.get_product_income_expense_accounts(
                        cr, uid, line.product_id.id,
                        context=context)['account_expense']
                }
                amount = line.subtotal
                if amount >= 0:
                    aml_values.update({
                        'credit': line.subtotal,
                    })
                else:
                    aml_values.update({
                        'debit': -line.subtotal,
                    })

                account_move_lines.append((0, 0, aml_values))
            account_move_id = account_move_obj.create(cr, uid, {
                'journal_id': iu.internal_use_case.journal.id,
                'line_id': account_move_lines,
                'date': iu.date_done,
                'period_id': period_id,
                'ref': _('Expense Transfert (%s)') % (iu.name),
            }, context=context)
            account_move_obj.button_validate(
                cr, uid, [account_move_id], context=context)

            # Validate picking (and associated stock moves)
            picking_obj.draft_force_assign(cr, uid, [picking_id])
            picking_obj.action_confirm(cr, uid, [picking_id], context=context)
            picking_obj.action_move(cr, uid, [picking_id], context=context)

            # associate internal use to stock moves and account move
            # and set to 'done'
            self.write(cr, uid, [iu.id], {
                'state': 'done',
                'picking_id': picking_id,
                'account_move_id': account_move_id,
            },
                context=context)
        return True
