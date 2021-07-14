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
{
    'name': 'Show total hours sold on SO and Project',
    'description': 'Show total hours sold on SO and Project',
    'author': 'Open2Bizz',
    'depends': ['sale', 'project','account', 'sale_subscription', 'helpdesk', 'helpdesk_timesheet'],
    'data' : [
              'views/sale_order_views.xml',
              'views/project_views.xml',
              'views/sale_subscription.xml',
              'views/helpdesk_views.xml',
              'data/res_config_data.xml',
              ],
    'application': False,
}
