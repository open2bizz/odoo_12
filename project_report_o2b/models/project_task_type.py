# -*- encoding: utf-8 -*-
##############################################################################
#
#    open2bizz
#    Copyright (C) 2016 open2bizz (open2bizz.nl).
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

from odoo import fields, models

class SaleOrderText(models.Model):
    _inherit = 'project.task.type'

    responsiblity_of_partner = fields.Boolean(string="Responsibility of Partner", help="When task is in this stage its the responsibility of the partner assigned to perform actions regarding this task")
    backlog_stage = fields.Boolean(string="Backlog stage", help="When task is in this stage it's treated as a backlog item, there is no funding for this item therefor it cannot be cannot be carried out yet.")

class BacklogProject(models.Model):
    _inherit = 'project.project'

    backlog_project_id = fields.Many2one(
        comodel_name = 'project.project',
        string = 'Project Backlog',
        required = False,
        domain = "[('partner_id.commercial_partner_id', '=', partner_id.commercial_partner_id)]",
        context = "{'default_partner_id' : partner_id,'default_allow_timesheets': False,'default_allow_forecast': False,'default_name': 'Backlog ' + name,'default_user_id': user_id}"
    )    
