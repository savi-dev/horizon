# vim: tabstop=4 shiftwidth=4 softtabstop=4

"""
Views for Join or Leave a project.
"""
import logging

from django.utils.translation import ugettext_lazy as _

from horizon import api
from horizon import exceptions
from horizon import tables
from .leave.tables import LeaveProjectsTable
from .join.tables import JoinProjectsTable


LOG = logging.getLogger(__name__)


class IndexView(tables.MultiTableView):
    table_classes = (LeaveProjectsTable, JoinProjectsTable)
    template_name = 'settings/membership/index.html'

    def get_leaveproject_data(self):
        try:
            leave_projects = api.keystone.tenant_list(self.request)
        except:
            leave_projects = []
            exceptions.handle(self.request,
                              _('Unable to retrieve Projects list that you are already joined'))
        return leave_projects

    def get_joinproject_data(self):
        try:
            join_projects = api.keystone.list_projects()
            user_projects = self.request.user.authorized_tenants
            for project in user_projects:
               if next((tenant for tenant in join_projects if tenant.id == project.id), None):
                    join_projects.remove(project)
        except:
            join_projects = []
            exceptions.handle(self.request,
                              _('Unable to retrieve list of projects.'))
        return join_projects

