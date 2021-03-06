# -*- encoding: utf-8 -*-
##############################################################################
#
#    POS Keep Draft Orders module for Odoo
#    Copyright (C) 2015-Today GRAP (http://www.grap.coop)
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

from openerp import netsvc
from osv.osv import except_osv
from openerp.tests.common import TransactionCase


class TestPosKeepDraftOrders(TransactionCase):
    """Tests for 'Point Of Sale - Keep Draft Orders' Module"""

    def setUp(self):
        super(TestPosKeepDraftOrders, self).setUp()

        self.imd_obj = self.registry('ir.model.data')
        self.ps_obj = self.registry('pos.session')
        self.po_obj = self.registry('pos.order')
        self.pmp_obj = self.registry('pos.make.payment')
        self.wf_service = netsvc.LocalService('workflow')

        self.pos_config_id = self.ref('point_of_sale.pos_config_main')
        self.product_1 = self.ref('product.product_product_48')
        self.cash_journal_id = self.ref('account.cash_journal')

    # Test Section
    def test_01_allow_draft_order_unpaid(self):
        """Test the possibility to let a PoS Order in a slate if it is not
        paid at all."""
        cr, uid = self.cr, self.uid

        # Open a new session
        ps1_id = self.ps_obj.create(cr, uid, {
            'config_id': self.pos_config_id,
        })

        # Create Order
        po_id = self.po_obj.create(cr, uid, {
            'session_id': ps1_id,
            'lines': [
                [0, False, {
                    'discount': 0,
                    'price_unit': 10,
                    'product_id': self.product_1,
                    'qty': 1}]]
        })

        # Close Session
        self.wf_service.trg_validate(
            uid, 'pos.session', ps1_id, 'close', cr)

        ps1 = self.ps_obj.browse(cr, uid, ps1_id)

        self.assertEquals(
            ps1.state, 'closed',
            """Draft Orders without Payment must not block the closing
            process of the associated session.""")

        # Open a second session
        ps2_id = self.ps_obj.create(cr, uid, {
            'config_id': self.pos_config_id,
        })

        po = self.po_obj.browse(cr, uid, po_id)

        self.assertEquals(
            po.session_id.id, ps2_id,
            """Draft Orders of a previous session must be associated to the
            new opened session to allow payment.""")

    # Test Section
    def test_02_block_draft_order_partial_paid(self):
        """Test the unpossibility to let a PoS Order in a slate if it is
        in a partial paid state."""
        cr, uid = self.cr, self.uid

        # Open a new session
        ps_id = self.ps_obj.create(cr, uid, {
            'config_id': self.pos_config_id,
        })

        # Create Order
        po_id = self.po_obj.create(cr, uid, {
            'session_id': ps_id,
            'lines': [
                [0, False, {
                    'discount': 0,
                    'price_unit': 10,
                    'product_id': self.product_1,
                    'qty': 3}]]
        })

        # Make partial payment
        self.po_obj.add_payment(cr, uid, po_id, {
            'amount': 1,
            'journal': self.cash_journal_id,
        })

        # Try Close Session (Must fail)
        with self.assertRaises(except_osv):
            self.wf_service.trg_validate(
                uid, 'pos.session', ps_id, 'close', cr)
