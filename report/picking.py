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

for x in ['report.stock.picking.list','report.stock.picking.list.in','report.stock.picking.list.out']:
    try:
        del Service._services[x]
    except:
        pass


class picking(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(picking, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'get_product_desc': self.get_product_desc,
            'line_number':self._get_product_line_number,
            
        })
    def get_product_desc(self, move_line):
        print "get_product_desc".upper()
        desc = move_line.product_id.name
        if move_line.product_id.default_code:
            desc = '[' + move_line.product_id.default_code + ']' + ' ' + desc
        return desc
    
            
    def get_components_line(self,datum,count,result=None,context=None):
        print "get_components_line".upper()
        if not datum.child_ids:
            return []
        if not result:
            result=[]
        for sub_count,x in enumerate(datum.child_ids):
            counter = '.'.join([str(count),str(sub_count+1)])
            result.append(counter)
            if x.child_ids:
                counter = '.'.join([str(count),str(sub_count+1)])
                result.extend(self.get_components_line(x, counter))
        return result
    
    def _get_product_line_number(self,data,context=None):
        print "_get_product_line_number".upper()
        cr = self.cr
        #intigrate fetching of bundle items
        #fetch main products (not bundle components)
        fin_count=[]
        parent_data = [x for x in data if not x.parent_id]
        for count,datum in enumerate(parent_data):
            fin_count.append(count+1)
            fin_count.extend(self.get_components_line(datum,count+1))
        res=[]
        for count,datum in enumerate(data):
            datum.bundle_items=[]
            res.append((fin_count[count],datum))
        return res            

for suffix in ['', '.in', '.out']:
    report_sxw.report_sxw('report.stock.picking.list' + suffix,
                          'stock.picking' + suffix,
                          'addons/lc5_report_customizations/report/picking1.rml',
                          parser=picking)
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
