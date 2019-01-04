# -*- encoding: utf-8 -*-
##############################################################################
#
#    open2bizz
#    Copyright (C) 2019 open2bizz (open2bizz.nl).
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
import logging
from odoo import api, models, fields
import odoo.addons.decimal_precision as dp

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    total_hours_on_order = fields.Float(string='Total hours sold'
                                        , help='Total hours sold on this order'
                                        , digits=dp.get_precision('Product Unit of Measure')
                                        , compute='_compute_total_hours_on_order',
                                        )

    @api.depends('order_line')
    def _compute_total_hours_on_order(self):
        uom_hour_mds = self.env['ir.model.data'].search([('module', 'in', ['product', 'uom']), ('model', '=', 'uom.uom'), ('name', '=', 'product_uom_hour')] )
        uom_hour_ids = [x.res_id for x in uom_hour_mds]

        uom_day_mds = self.env['ir.model.data'].search([('module', 'in', ['product', 'uom']), ('model', '=', 'uom.uom'), ('name', '=', 'product_uom_day')] )
        uom_day_ids = [x.res_id for x in uom_day_mds]
        
        for rec in self:
            total = 0.0
            for line in rec.order_line:
                if line.product_uom.id in uom_day_ids:
                    total += line.product_uom_qty * 8
                elif line.product_uom.id in uom_hour_ids:
                    total += line.product_uom_qty
                # Until we phase out the use of hour pack products
                elif line.product_id.product_tmpl_id.id == 309:
                    try:
                        s = line.product_id.display_name
                        pack = s[s.find("(")+1:s.find(")")].split(' ')[0]
                        total += float(pack)
                    except:
                        _logger.error('Error converting line %s to hours' % (line))
                        total = 0.0
            rec.total_hours_on_order = total
    
