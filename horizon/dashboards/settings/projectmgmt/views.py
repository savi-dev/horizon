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
from .tables import ProjectsTable

LOG= logging.getLogger(__name__)

class IndexView(tables.DataTableView):
    table_class = ProjectsTable
    template_name = 'settings/projectmgmt/index.html'

    def get_data(self):
        tenants = keystone.list_projects()
        return tenants

class CreateProjectView(forms.ModalFormView):
    form_class = CreateProjectForm
    template_name = 'settings/projectmgmt/create.html'
    success_url = reverse_lazy('horizon:settings:projectmgmt:index')
