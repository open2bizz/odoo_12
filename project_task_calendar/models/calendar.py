# Copyright Open2Bizz

from datetime import date, datetime, timedelta

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

class Meeting(models.Model):
    _inherit = 'calendar.event'


    task_id = fields.Many2one(
        "project.task",
        string="Linked task"
    )
    project_id = fields.Many2one(
        "project.project",
        string="Project",
        related="task_id.project_id",
        store=True
    )
    def default_get(self, flds):
        res = super(Meeting, self).default_get(flds)
        if self._context.get('task_id', False):
            task = self.env['project.task'].browse(self._context.get('task_id', False))
            res['name'] = self._task_event_name(task)
        return res

