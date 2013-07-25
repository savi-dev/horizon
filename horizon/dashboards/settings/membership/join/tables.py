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


from horizon import exceptions
from horizon import messages
from horizon import tables
from horizon.api import get_project

LOG=logging.getLogger(__name__)

def get_dscr(tenant):
    return tenant.description


class JoinProject(tables.BatchAction):
    name = "join"
    action_present = _("Join")
    action_past = _("Your request to join the project has been sent to admin")
    data_type_singular = _("Project")
    data_type_plural = _("Projects")
    classes = ('btn-launch',)

    def allowed(self, request, project=None):
        return True

    def action(self, request, project_id):
        project = get_project(project_id)
        admin = settings.ADMIN_EMAIL
        try:
            subject = "[HORIZON] New Access Request"
            message = render_to_response('settings/membership/join/JoinReq.txt',
                                  {'username':request.user.username,
                                    'project': project.name })
            email = EmailMessage(subject, message, to=[admin])
            email.send()
        except:
            redirect = reverse("horizon:settings:membership:index")
            exceptions.handle(request,
                              _('Unable to sent Request.'),
                              redirect=redirect)


class CreateProject(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Project")
    url = "horizon:settings:membership:join:create"
    classes = ("ajax-modal", "btn-create")


class JoinProjectsTable(tables.DataTable):
    
    project_name = tables.Column('name', verbose_name=_("Project Name"))
    project_dscr = tables.Column(get_dscr,
                                 verbose_name=_("Description"))

    class Meta:
        name = "joinproject"
        verbose_name = _("Projects You Can Join")
        table_actions = (CreateProject,)
        multi_select = False
        row_actions = (JoinProject,)

    