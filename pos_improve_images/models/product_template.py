# -*- encoding: utf-8 -*-
##############################################################################
#
#    Point Of Sale - Improve Images module for OpenERP
#    Copyright (C) 2014-Today GRAP (http://www.grap.coop)
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

from openerp import fields, models, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    has_image = fields.Boolean(
        compute='_compute_has_image', string='Has Image', store=True)

    @api.depends('image_medium')
    def _compute_has_image(self):
        for item in self:
            item.has_image = not (item.image is None)
