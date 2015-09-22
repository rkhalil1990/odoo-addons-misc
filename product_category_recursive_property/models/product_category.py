# -*- encoding: utf-8 -*-
##############################################################################
#
#    Product Category - Recursive property for Odoo
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

from openerp import models, api


class ProductCategory(models.Model):
    _inherit = 'product.category'

    _PRODUCT_CATEGORY_PROPERTY_LIST = [
        'property_stock_journal',
        'property_stock_account_input_categ',
        'property_stock_account_output_categ',
        'property_stock_valuation_account_id',
        'property_account_income_categ',
        'property_account_expense_categ',
    ]

    # Custom Function
    @api.multi
    def _propagate_properties_to_childs(self, vals):
        values = {}
        for property_name in self._PRODUCT_CATEGORY_PROPERTY_LIST:
            if property_name in vals.keys():
                values[property_name] = vals[property_name]
        if values:
            childs = self.browse()
            for item in self:
                childs += item.child_id
            if childs.ids:
                childs.write(values)

    @api.one
    def _get_vals_from_parent(self):
        res = {}
        for property_name in self._PRODUCT_CATEGORY_PROPERTY_LIST:
            res[property_name] = self[property_name].id
        return res

    # Overload Section
    @api.model
    def create(self, vals):
        if vals.get('parent_id', False):
            parent = self.browse(vals.get('parent_id'))
            vals.update(parent._get_vals_from_parent()[0])
        res = super(ProductCategory, self).create(vals)
        res._propagate_properties_to_childs(vals)
        return res

    @api.multi
    def write(self, vals):
        if vals.get('parent_id', False):
            parent = self.browse(vals.get('parent_id'))
            vals.update(parent._get_vals_from_parent()[0])
        res = super(ProductCategory, self).write(vals)
        if self:
            self._propagate_properties_to_childs(vals)
        return res
