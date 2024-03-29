# -*- coding: utf-8 -*-
# Copyright Open2bizz (http://www.open2bizz.nl)
# See LICENSE file for full copyright and license details.
{
    'name': 'Helpdesk Ticket Solution',
    'version': '0.1',
    'category': 'Helpdesk',
    'description': """Adds a solution for helpdesk tickets""",
    'author': 'Open2bizz',
    'website': 'http://open2bizz.nl/',
    'depends': [
        'helpdesk',
        'default_data'
    ],
    'data':[
        'views/view_helpdesk_ticket.xml',
        'security/ir.model.access.csv',
    ],            
    'installable': True,
}
