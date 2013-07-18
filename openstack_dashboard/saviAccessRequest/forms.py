'''
Created on July 11, 2013

@author: Mohammad Faraji<ms.faraji@utoronto.ca>
'''


from  django import forms
from django.contrib.auth.models import User

from  .models import RequestProfile

attrs_dict = { 'class': 'required' }

class RequestForm(forms.Form):
   username = forms.RegexField(regex=r'^\w+$',
                                max_length=30,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_("Desired Username"),
                                error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
   first_name = forms.CharField(label=_("First Name"))
   last_name = forms.CharField(label=_("Last Name"))
   email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,maxlength=75)),
                             label=_("Email address")) 
   university = forms.CharField(label=_("University"))

   def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:

            return self.cleaned_data['username']
        raise forms.ValidationError(_("A user with that username already exists.")) 
   
   def clean_email(self):
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is already in use. Please supply a different email address."))
            
        return self.cleaned_data['email'] 

   def save(self, profile_callback=None):

        new_user = User.objects.create_user(username= self.cleaned_data['username'],email=self.cleaned_data['email'])
        new_user.first_name = self.cleaned_data['first_name']
        new_user.last_name = self.cleaned_data['last_name']
        new_user.save()
        profile = RequestProfile.objects.create(user = new_user, university=self.cleaned_data['university'], status='PENDING')
        return new_user, profile

class RequestFormNoFreeEmail(RequestForm):
     bad_domains = ['aim.com', 'aol.com', 'email.com', 'gmail.com',
                   'googlemail.com', 'hotmail.com', 'hushmail.com',
                   'msn.com', 'mail.ru', 'mailinator.com', 'live.com',
                   'yahoo.com'] 
     def clean_email(self):
        email_domain = self.cleaned_data['email'].split('@')[1]
        if email_domain in self.bad_domains:
            raise forms.ValidationError(_("Requesting using free email addresses is prohibited. Please supply a different email address."))
        return self.cleaned_data['email']
