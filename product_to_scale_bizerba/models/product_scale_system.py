# -*- coding: utf-8 -*-
# Copyright (C) 2014 GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv import fields
from openerp.osv.orm import Model


class product_scale_system(Model):
    _name = 'product.scale.system'

    def _get_field_ids(
        self, cr, uid, ids, field_names, arg=None, context=None):
        res = {}
        for id in ids:
            res.setdefault(id, [])
        # TODO
#        for system in self.browse(cr, uid, ids, context=context):
#            for line in system.product_field_lines:
#                if line.field_id: 
#                    res[system.id].append(line.field_id.id)
        return res

    _columns = {
        'name': fields.char(
            string='Name', required=True),
        'company_id': fields.many2one(
            'res.company', string='Company', select=True),
        'active': fields.boolean(
            string='Active'),
        'ftp_url': fields.char(
            string='FTP Server URL', required=True),
        'ftp_login': fields.char(
            string='FTP Login'),
        'ftp_password': fields.char(
            string='FTP Password'),
        'csv_relative_path': fields.char(
            string='Relative Path for CSV', required=True),
        'image_relative_path': fields.char(
            string='Relative Path for Product Images', required=True),
        'product_lines': fields.one2many(
            'product.scale.system.product.line', 'scale_system_id',
            'Product Lines'),
        'field_ids': fields.function(
            _get_field_ids, type='one2many', string='Fields',
            relation='ir.model.fields'),
    }

    _defaults = {
        'active': True,
        'company_id': lambda s, cr, uid, c: s.pool.get('res.company').
            _company_default_get(cr, uid, 'product.template', context=c),
        'ftp_url': 'xxx.xxx.xxx.xxx',
        'csv_relative_path': '/',
        'image_relative_path': '/',
    }