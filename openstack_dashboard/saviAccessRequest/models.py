'''
Created on July 11, 2013

@author: Mohammad Faraji<ms.faraji@utoronto.ca>
'''



from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

class RequestProfile(models.Model):
    STATUS = (
       ('CREATED','CREATED'),
       ('PENDING','PENDING')
    )
    user = models.ForeignKey(User, unique=True)    
    university = models.CharField(_('university'), max_length=60, blank=True)   
    status = models.CharField(_('Status'), max_length=20, choices = STATUS)

    class Meta:
        verbose_name = "Request profile"
        verbose_name_plural = "Request profiles"   
   
