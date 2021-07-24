# Copyright Open2Bizz

from datetime import date, datetime, timedelta

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
from operator import attrgetter

class Task(models.Model):

    _inherit = "project.task"
    
    calendar_event_ids = fields.One2many(
        'calendar.event',
        'task_id',
        string='Events'
    )

    calendar_event_count = fields.Integer(compute='_compute_nr_events', string="# Events")
    next_event_id = fields.Many2one('calendar.event',compute='_compute_events', string='Upcoming Event')
    next_event_start = fields.Datetime(related='next_event_id.start', string='Upcoming Event Start')

    @api.depends('calendar_event_ids','calendar_event_count')
    def _compute_events(self):
        now = fields.Datetime.now()
        for rec in self:
            calendar_events = rec.env['calendar.event'].search([('task_id','=',rec.id),('start','>=',now)])
            sorted_list = sorted(calendar_events, key=attrgetter('start'))
            if sorted_list:
                rec.next_event_id = sorted_list[0].id
            else:
             rec.next_event_id = False

    @api.depends('calendar_event_ids','next_event_id')
    def _compute_nr_events(self):
        for rec in self:
            rec.calendar_event_count = len(rec.calendar_event_ids)

    def button_create_event(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("calendar.action_calendar_event")
        action['context'] = {
            'search_default_task_id': self.id,
            'default_partner_ids': [self.user_id.partner_id.id],
            'default_user_id': self.user_id.partner_id.id,
            'default_name': self.name,
            'default_task_id': self.id
        }
        return action
