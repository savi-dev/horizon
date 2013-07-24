# vim: tabstop=4 shiftwidth=4 softtabstop=4
'''
Created on July 23, 2013

@author: Mohammad Faraji<ms.faraji@utoronto.ca>
'''

from django.utils.translation import ugettext_lazy as _

import horizon
from horizon.dashboards.settings import dashboard


class TenantPanel(horizon.Panel):
    name = _("Project Settings")
    slug = 'projectmgmt'


dashboard.Settings.register(TenantPanel)
