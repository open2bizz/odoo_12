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
from datetime import datetime
from dateutil.relativedelta import *

_logger = logging.getLogger(__name__)

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    commercial_partner_id = fields.Many2one("res.partner", related="partner_id.commercial_partner_id", readonly=True, string="Customer Company" )

    monthly_hours_contract = fields.Float('Monthly contract hours'
                                 , help='The amount of hours per month included in this contract'
                                 , compute='_compute_total_hours')
    
    monthly_hours_spend = fields.Float('Monthly spend'
                                 , help='The amount of hours spend this month'
                                 , compute='_compute_total_hours')
    
    monthly_hours_left = fields.Float('Current month left'
                                 , help='The amount of hours left for this month'
                                 , compute='_compute_total_hours')

    @api.depends('timesheet_ids')
    def _compute_total_hours(self):
        uom_hour_mds = self.env['ir.model.data'].search([('module', 'in', ['product', 'uom']), ('model', '=', 'uom.uom'), ('name', '=', 'product_uom_hour')] )
        uom_hour_ids = [x.res_id for x in uom_hour_mds]

        start_date = datetime.now().strftime("%Y-%m-01")
        end_date = (datetime.strptime(start_date, "%Y-%m-%d")+relativedelta(months=+1)).strftime("%Y-%m-%d")
        for rec in self:
            monthly_hours = 0.0
            for sub in self.env['sale.subscription'].search([('analytic_account_id', '=', rec.project_id.analytic_account_id.id )]):
                monthly_hours += sub.monthly_hours

            al=self.env['account.analytic.line'].search([('account_id', '=', rec.project_id.analytic_account_id.id )
                                                         , ('product_uom_id', 'in', uom_hour_ids)
                                                         , ('date', '>=', start_date)
                                                         , ('date', '<', end_date)
                                                         ])
            monthly_hours_spend = 0.0
            for a in al:
                monthly_hours_spend += a.unit_amount
            
            rec.monthly_hours_contract = monthly_hours
            rec.monthly_hours_spend = monthly_hours_spend
            rec.monthly_hours_left = monthly_hours - monthly_hours_spend
