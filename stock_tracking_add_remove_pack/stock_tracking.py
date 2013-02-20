# -*- coding: utf-8 -*-
#################################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011 Julius Network Solutions SARL <contact@julius.fr>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################

from openerp.osv import fields, osv, orm
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
import time

class stock_tracking(orm.Model):
    _inherit = 'stock.tracking'
    
    def _add_pack(self, cr, uid, pack_id, child_ids, context=None):
        if context == None:
            context = {}
        history_obj = self.pool.get('stock.tracking.history')
        pack = self.browse(cr, uid, pack_id, context=context)
        child = self.browse(cr, uid, child_ids, context=context)[0]
        hist_id = history_obj.create(cr, uid, {
           'tracking_id': pack.id,
           'type': 'add_object',
           'location_id': pack.location_id.id,
           'location_dest_id': pack.location_id.id,
           'child_pack_id': child.id,
           'qty': 1.0,
        }, context=context)
        self.write(cr, uid, child_ids, {'parent_id': pack_id}, context=context)
        self.get_products(cr, uid, [pack_id], context=context)
        self.get_serials(cr, uid, [pack_id], context=context)
        return True
    
    def _remove_pack(self, cr, uid, pack_id, child_ids, context=None):
        if context == None:
            context = {}
        history_obj = self.pool.get('stock.tracking.history')  
        pack = self.browse(cr, uid, pack_id, context=context)
        child = self.browse(cr, uid, child_ids, context=context)[0]
        hist_id = history_obj.create(cr, uid, {
           'tracking_id': pack.id,
           'type': 'remove_object',
           'location_id': pack.location_id.id,
           'location_dest_id': pack.location_id.id,
           'child_pack_id': child.id,
           'qty': 1.0,
        }, context=context)
        self.write(cr, uid, child_ids, {'parent_id': False}, context=context)
        self.get_products(cr, uid, [pack_id], context=context)
        self.get_serials(cr, uid, [pack_id], context=context)
        return True
<<<<<<< TREE
    
class stock_tracking_history(osv.osv):
    
    _inherit = "stock.tracking.history"
    
    def _get_types(self, cr, uid, context={}):
        res = super(stock_tracking_history, self)._get_types(cr, uid, context)
        if not res:
            res = []
        res = res + [('add_pack',_('Add pack')),('remove_pack',_('Remove pack'))]
        return res
    
    _columns = {
        'type': fields.selection(_get_types, 'Type'),
        'child_pack_id': fields.many2one('stock.tracking', 'Pack'),
        
        
    }
=======
>>>>>>> MERGE-SOURCE

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
