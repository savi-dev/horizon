# vim: tabstop=4 shiftwidth=4 softtabstop=4
'''
Created on July 23, 2013

@author: Mohammad Faraji<ms.faraji@utoronto.ca>
'''

from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages


class CreateProjectForm(forms.SelfHandlingForm):
    name = forms.CharField(max_length="255", label=_("Name"), required=True)
    description = forms.CharField(widget=forms.Textarea,
            label=_("Description"), required=False)
    
    def handle(self, request, data):
        try:
            admin = settings.ADMIN_EMAIL
            subject = "[HORIZON] New Project Create Request"
            message = render_to_response('settings/membership/create/CreateReq.txt',
                                      {'username':request.user.username,
                                        'projectName': data['name'],
                                        'description':data['description'] })
            email = EmailMessage(subject, message, to=[admin])
            email.send()
            messages.success(request,
                             _('Successfully sent the request'))
        except:
            redirect = reverse("horizon:settings:membership:index")
            exceptions.handle(request,
                              _('Unable to send Request.'),
                              redirect=redirect)

        return True