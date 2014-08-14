# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

import time
from openerp import netsvc
from openerp.netsvc import Service

for x in ['report.sale.order','report.sale.order.inherit',"report.sale.shipping"]:
    try:
        del Service._services[x]
    except:
        pass


from openerp.report import report_sxw

class order(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(order, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time, 
            'show_discount':self._show_discount,
            'line_number':self._get_product_line_number,
            'get_designation':self._get_designation,
            #'get_product_bundle_items':self._get_product_bundle_items,
        })
        
    #def _get_product_bundle_items(self,product_id,context=None):
    #    cr=self.cr
    #    uid = self.uid
        #Comment: fetch connected product item entries
    #    cr.execute('select product_id from product_item where product_id = %s' % product_id)
    #    bundle_product_item_ids = [x[0] for x in cr.fetchall()]
    #    product_dicts=self.pool.get('product.product').read(cr,uid,bundle_product_item_ids,['name'])
    #    bundle_product_names = [product_dict['name'] for product_dict in product_dicts]
    #    res = bundle_product_names
    #    if context and 'mode' in context and context['mode'] == 'all':
    #        res = [product_dict['id'] for product_dict in product_dicts]
    #    return res
            

    def _get_product_line_number(self,data,context=None):
        cr = self.cr
        #intigrate fetching of bundle items
        #for datum in data:
        #    datum.bundle_items=self._get_product_bundle_items(datum.product_id.id)
        res = [(x+1,obj) for x,obj in enumerate(data)]
        return res        

        return data
   
    def _get_designation(self,data,context=None):
        cr = self.cr
        uid = self.uid
        pool = self.pool.get
        employee_id = pool('hr.employee').search(cr,uid,[('user_id','=',data)],limit=1)
        res = ''
        if employee_id:
            employee_dict = pool('hr.employee').read(cr,uid,employee_id[0],['job_id'])
            if employee_dict['job_id']:
                res = employee_dict['job_id'][1]
        return res
        

    def _show_discount(self, uid, context=None):
        cr = self.cr
        try: 
            group_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'sale', 'group_discount_per_so_line')[1]
        except:
            return False
        return group_id in [x.id for x in self.pool.get('res.users').browse(cr, uid, uid, context=context).groups_id]

report_sxw.report_sxw('report.sale.order.inherit', 'sale.order', 'addons/lc5_report_customizations/report/sale_order.rml', parser=order, header="external")
report_sxw.report_sxw('report.sale.order', 'sale.order', 'addons/lc5_report_customizations/report/sale_order.rml', parser=order, header="external")
#report_sxw.report_sxw('report.sale.order.proforma.invoice', 'sale.order', 'addons/lc5_report_customizations/report/proforma_invoice.rml', parser=order, header="external")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

