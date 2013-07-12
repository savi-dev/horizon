'''
Created on July 11, 2013

@author: Mohammad Faraji<ms.faraji@utoronto.ca>
'''
import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, send_mail
from django.db import transaction
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.shortcuts import render_to_response


from .forms import RequestFormNoFreeEmail
from .models import RequestProfile

LOG = logging.getLogger(__name__)

def requestAccess(request, success_url=None,
             form_class= RequestFormNoFreeEmail , profile_callback=None,
             template_name = 'accessReq/AccessRequest.html',
             extra_context=None):

    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_user, profile = form.save()
            sendEmailToAdmin(new_user, profile)
            sendEmailToUser(new_user)
            return HttpResponseRedirect(success_url)
    else:
            form = form_class()

    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    return render_to_response(template_name,
                              { 'form': form },
                              context_instance=context)

def sendEmailToAdmin(user, profile):
    admin = settings.ADMIN_EMAIL
    subject = "[HORIZON] New Access Request"
    message = render_to_response('accessReq/admin_msg.txt',
                                  {'user':user, 'profile': profile })
    email = EmailMessage(subject, message, to=[admin])
    email.send()

def sendEmailToUser(user):
    admin_email = settings.ADMIN_EMAIL
    subject = "Thanks for registering with SAVI TB"
    message = render_to_response('accessReq/user_msg.txt',
                                 {'name':user.first_name, 'admin_email': admin_email })
    email = EmailMessage(subject, message, to=[user.email])
    email.send()
 
