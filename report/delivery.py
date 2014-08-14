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

from openerp.report import report_sxw
from openerp.netsvc import Service

for x in ['report.sale.shipping','report.sale.shipping.inherit','report.picking.out.delivery.receipt']:
    try:
        del Service._services[x]
    except:
        pass

class shipping(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(shipping, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'line_number':self._get_product_line_number,
            
        })
        

    def _get_product_line_number(self,data,context=None):
        cr = self.cr
        #intigrate fetching of bundle items
        res = [(obj.line_number,obj) for x,obj in enumerate(data)]
        return res        
# 
#report_sxw.report_sxw('report.picking.equipment.transfer','stock.picking','addons/lc5_report_customizations/report/equipment_transfer.rml',parser=shipping)
report_sxw.report_sxw('report.picking.out.delivery.receipt','stock.picking.out','addons/lc5_report_customizations/report/delivery_receipt.rml',parser=shipping)
report_sxw.report_sxw('report.picking.out.delivery.order','stock.picking.out','addons/lc5_report_customizations/report/delivery_order.rml',parser=shipping)
report_sxw.report_sxw('report.sale.shipping.inherit','stock.picking','addons/lc5_report_customizations/report/delivery_order.rml',parser=shipping)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
