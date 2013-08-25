# vim: tabstop=4 shiftwidth=4 softtabstop=4
'''
Created on July 23, 2013

@author: Mohammad Faraji<ms.faraji@utoronto.ca>
'''
import logging

from django.conf import settings
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.utils.translation import ugettext_lazy as _

from horizon import api
from horizon import exceptions
from horizon import messages
from horizon import tables
from horizon.api import get_project

LOG=logging.getLogger(__name__)

def get_dscr(tenant):
    return tenant.description


class LeaveProject(tables.BatchAction):
    name = "Leave"
    action_present = _("Leave")
    action_past = _("You are successfully left the project")
    data_type_singular = _("Project")
    data_type_plural = _("Projects")
    classes = ('btn-danger',)

    def allowed(self, request, project_id=None):
        if len(request.user.authorized_tenants) > 1:
            return True
        return False
            

    def action(self, request, project_id):
        project = get_project(project_id)
        admin = settings.ADMIN_EMAIL
        try:
            subject = "[HORIZON] User Leave Stat"
            message = render_to_response('settings/membership/leave/leaveInfo.txt',
                                  {'username':request.user.username,
                                    'project': project.name })
            email = EmailMessage(subject, message, to=[admin])
            email.send()
            api.keystone.remove_tenant_user(request, project_id, request.user.id)
        except:
            redirect = reverse("horizon:settings:membership:index")
            exceptions.handle(request,
                              _('Unable to sent Request.'),
                              redirect=redirect)


class LeaveProjectsTable(tables.DataTable):
    
    project_name = tables.Column('name', verbose_name=_("Project Name"))
    project_dscr = tables.Column(get_dscr,
                                 verbose_name=_("Description"))

    class Meta:
        name = "leaveproject"
        verbose_name = _("Your Projects")
        row_actions = (LeaveProject,)

    