# -*- encoding: utf-8 -*-
##############################################################################
#
#    Point Of Sale - Restaurant module for Odoo
#    Copyright (C) Odoo (http://www.odoo.com)
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

from openerp import models, fields


class RestaurantTable(models.Model):
    _name = 'restaurant.table'
    _order = 'floor_id, name'

    # Columns section
    name = fields.Char('Name', required=True, default='/', copy=False)

    image = fields.Binary('Image')

    active = fields.Boolean(
        string='Active', help="By unchecking the active field you can disable"
        " a table without deleting it.", default=True)

    floor_id = fields.Many2one(
        comodel_name='restaurant.floor', string='Floor', required=True)

    company_id = fields.Many2one(
        comodel_name='res.company', string='Company', readonly=True,
        related='floor_id.config_id.company_id', store=True)

    # Constraint Section
    _sql_constraints = [
        ('name_floor_uniq', 'unique(name, floor_id)',
            'Table name must be unique by Floor!'),
    ]
