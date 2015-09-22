# -*- encoding: utf-8 -*-
##############################################################################
#
#    Product Category - Recursive property for Odoo
#    Copyright (C) 2014-Today GRAP (http://www.grap.coop)
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

from openerp.tests.common import TransactionCase


class Tests(TransactionCase):

    def setUp(self):
        super(Tests, self).setUp()
        self.category_obj = self.env['product.category']
        self.property_obj = self.env['ir.property']

        self.mother_category_id = self.ref(
            'product_category_recursive_property.mother_category')
        self.child_category_id = self.ref(
            'product_category_recursive_property.child_category')
        self.income_property_id = self.ref(
            'account.property_account_income_categ')
        self.expense_property_id = self.ref(
            'account.property_account_expense_categ')
        self.expense_account_id = self.ref(
            'account.a_sale')
        self.income_account_id = self.ref(
            'account.a_expense')

    # Test Section
    def test_01_all_default(self):
        """[Functional Test] Tests changing expense / income account
        on product categories"""

        # Delete default property value
        properties = self.property_obj.browse(
            [self.income_property_id, self.expense_property_id])
        properties.unlink()
        for category in self.category_obj.search():
            self.assertEquals(
                category.property_account_expense_categ.id, False,
                "Regression - Remove default value must remove expense"
                " property !")
            self.assertEquals(
                category.property_account_income_categ.id, False,
                "Regression - Remove default value must remove income"
                " property !")

        # Set expense categ to mother pc
        self.category_obj.browse(self.mother_pc_id).write({
            'property_account_expense_categ': self.expense_aa_id})
        child_category = self.category_obj.browse(self.child_category_id)
        self.assertEquals(
            child_category.property_account_expense_categ.id,
            self.expense_account_id,
            "Set an expense account to a mother category must set an"
            " expense account to their childs !")

        # Set income categ to mother pc
        self.category_obj.browse(self.mother_pc_id).write({
            'property_account_income_categ': self.income_aa_id})
        child_category = self.category_obj.browse(self.child_category_id)
        self.assertEquals(
            child_category.property_account_income_categ.id,
            self.income_account_id,
            "Set an income account to a mother category must set an"
            " income account to their childs !")

        # Check if other categories are not affected
        categories = self.category_obj.search([
            ('id', 'not in',
                [self.mother_category_id, self.child_category_id])])
        for category in categories:
            self.assertEquals(
                category.property_account_expense_categ.id, False,
                "Set an expense categ to a category must not affect non child"
                " categories !")
            self.assertEquals(
                category.property_account_income_categ.id, False,
                "Set an income categ to a category must not affect non child"
                " categories !")
