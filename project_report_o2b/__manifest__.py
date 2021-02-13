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
{
    "name": "Project Overview Report",
    "summary": "This app creates a Qweb report that gives a complete overview of tasks, planned hours, timesheets and responsible persons of project(s)",
    "version": "1.0",
    "author": "Open2bizz",
    'website': 'http://www.open2bizz.nl',
    "category": "Reports",
    "description":"""
        This app adds the following reports:
            - Project Overview
    """,
    "depends": [
        "base",
        "project",
        "hour_totals_sold",
#        "helpdesk_project"
    ],
    "data": [
        "views/project_overview.xml",
        "report/reports.xml",
        "views/project_task_type.xml",
        "views/project_backlog.xml"
        "data/mail_template.xml",
    ],
    "application": True,
    "installable": True,
}
