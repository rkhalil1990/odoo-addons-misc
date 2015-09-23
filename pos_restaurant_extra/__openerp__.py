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
{
    'name': 'Point of Sale - Restaurant Extra',
    'version': '8.0.2.0.0',
    'category': 'Point Of Sale',
    'author': 'Odoo,GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'point_of_sale',
        'pos_restaurant',
    ],
    'demo': [
        'demo/restaurant_floor.yml',
        'demo/restaurant_table.yml',
        'demo/res_groups.yml',
    ],
    'data': [
        'security/ir_rule.yml',
        'security/ir_module_category.yml',
        'security/res_groups.yml',
        'security/ir_model_access.yml',
        'views/view.xml',
        'views/action.xml',
        'views/view_agregate.xml',
        'views/action_agregate.xml',
        'views/menu.xml',
    ],
}
