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

class Project(models.Model):
    _inherit = 'project.project'
    
    total_hours_on_project = fields.Float(string='Total hours sold'
                                        , help='Total hours sold on this project'
                                        , digits=dp.get_precision('Product Unit of Measure')
                                        , compute='_compute_total_hours_on_project',
                                        )

    #order_count = fields.Integer(compute='_compute_total_hours_on_project', string="Orders")
    # Added for QWEB report Project overview
    #order_ids = fields.One2many('sale.order', compute='_compute_total_hours_on_project', string='Orders')

    total_hours_spent_on_project = fields.Float(string='Total hours spent'
                                        , help='Total hours spent on this project'
                                        , digits=dp.get_precision('Product Unit of Measure')
                                        , compute='_compute_spent_hours_on_project',
                                        )

    def _compute_total_hours_on_project(self):
        for rec in self:
            total = 0.0
            #all_orders = self.env['sale.order'].search([('related_project_id', '=', rec.analytic_account_id.id )])
            #sold_orders = self.env['sale.order'].search([('related_project_id', '=', rec.analytic_account_id.id ), ('state', 'in', ['sale', 'done'])])
            #rec.order_ids = sold_orders
            #rec.order_count = len(all_orders)
            for order in rec.sale_order_id:
                total += order.total_hours_on_order
            rec.total_hours_on_project = total

    def _compute_spent_hours_on_project(self):
        for rec in self:
            al_ids = self.env['account.analytic.line'].search([('account_id', '=', rec.analytic_account_id.id), ('is_timesheet','=', True)])
            rec.total_hours_spent_on_project = sum(al_ids.mapped('unit_amount'))

    def inform_about_task_progress(self, *args):
        projects = self.env['project.project'].search([('active', '=', True)])
        tasks = self.env['project.task'].search([('project_id', 'in', projects.ids), ('stage_id', '!=', False), ('stage_id.fold', '=', False)])
        body_html = """
<style>
table, th, td {
    border: 1px solid black;
}
</style>
<h1>Reached or about to reach planned hours</h1>
<table style="width:100%">
  <tr>
    <th>Task</th>
    <th>Progress (%) or (hours) if planned=0</th>
    <th>Project</th>
  </tr>
"""
        for t in tasks:
            if t.progress > 80 or (t.planned_hours < t.total_hours_spent) :
                body_html += '<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % (t.name, t.progress if t.planned_hours > 0.0 else '(%0.1f)' % (t.total_hours_spent), t.project_id.name)
        body_html += '</table>'
        mail_pool = self.env['mail.mail']
        values={}
        values.update({'subject': 'Tasks that need your attention'})
        values.update({'email_to': ','.join(args)})
        values.update({'body_html': body_html })
        mail_pool.create(values) #.send()
