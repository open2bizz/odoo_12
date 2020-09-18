# Copyright 2013-2020 Open2Bizz <info@open2bizz.nl>
# License LGPL-3

from odoo import api, fields, models


class MailActivity(models.Model):
    _inherit = "mail.activity"


    project_id = fields.Many2one('project.project', string='Project')
    task_id = fields.Many2one('project.task', string='Task')
    customer_id = fields.Many2one('res.partner', string='Klant')

    @api.model
    def create(self, values):
        if self.env['ir.model'].browse(values.get('res_model_id')).model == 'project.task':
            task = self.env['project.task'].browse(values.get('res_id'))
            values.update({'project_id':task.project_id.id,'task_id':task.id,'customer_id':task.partner_id.id})
        if self.env['ir.model'].browse(values.get('res_model_id')).model == 'project.project':
            project = self.env['project.project'].browse(values.get('res_id'))
            values.update({'project_id':project.id,'customer_id':project.partner_id.id})
        return super(MailActivity, self).create(values)

