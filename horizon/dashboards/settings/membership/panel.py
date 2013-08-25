# vim: tabstop=4 shiftwidth=4 softtabstop=4

from django.utils.translation import ugettext_lazy as _

import horizon
from horizon.dashboards.settings import dashboard


class JoinAndLeaveProject(horizon.Panel):
    name = _("Join and Leave Project")
    slug = 'membership'


dashboard.Settings.register(JoinAndLeaveProject)
