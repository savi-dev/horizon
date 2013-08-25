# vim: tabstop=4 shiftwidth=4 softtabstop=4
'''
Created on July 23, 2013

@author: Mohammad Faraji<ms.faraji@utoronto.ca>
'''
import logging

from django.core.urlresolvers import reverse_lazy

from horizon import forms
from horizon import tables
from horizon.api import keystone

from .forms import CreateProjectForm
from .tables import JoinProjectsTable

LOG= logging.getLogger(__name__)


class CreateProjectView(forms.ModalFormView):
    form_class = CreateProjectForm
    template_name = 'settings/membership/create/create.html'
    success_url = reverse_lazy('horizon:settings:membership:index')
