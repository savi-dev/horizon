# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 Nebula, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import logging
from datetime import datetime
import pytz

from django import shortcuts
from django.conf import settings
from django.forms import ValidationError
from django.utils.translation import force_unicode, ugettext_lazy as _
from django.utils import translation
from django.views.decorators.debug import sensitive_variables

from horizon import api
from horizon import exceptions
from horizon import forms
from horizon import messages
from horizon.utils import validators

LOG = logging.getLogger(__name__)

class UserSettingsForm(forms.SelfHandlingForm):
    language = forms.ChoiceField()
    timezone = forms.ChoiceField()
    password = forms.RegexField(label=_("Password"),
            widget=forms.PasswordInput(render_value=False),
            regex=validators.password_validator(),
            required=False,
            error_messages={'invalid':
                    validators.password_validator_msg()})
    confirm_password = forms.CharField(
            label=_("Confirm Password"),
            widget=forms.PasswordInput(render_value=False),
            required=False)
    
    def clean(self):
        '''Check to make sure password fields match.'''
        data = super(forms.Form, self).clean()
        if 'password' in data:
            if data['password'] != data.get('confirm_password', None):
                raise ValidationError(_('Passwords do not match.'))
        return data
    
    def __init__(self, *args, **kwargs):
        super(UserSettingsForm, self).__init__(*args, **kwargs)

        # Languages
        languages = [(k, "%s (%s)"
                      % (translation.get_language_info(k)['name_local'], k))
                      for k, v in settings.LANGUAGES]
        self.fields['language'].choices = languages

        # Timezones
        d = datetime(datetime.today().year, 1, 1)
        timezones = []
        for tz in pytz.common_timezones:
            try:
                utc_offset = pytz.timezone(tz).localize(d).strftime('%z')
                utc_offset = " (UTC %s:%s)" % (utc_offset[:3], utc_offset[3:])
            except:
                utc_offset = ""

            if tz != "UTC":
                tz_name = "%s%s" % (tz, utc_offset)
            else:
                tz_name = tz
            timezones.append((tz, tz_name))

        self.fields['timezone'].choices = timezones

    @sensitive_variables('data')
    def handle(self, request, data):
        response = shortcuts.redirect(request.build_absolute_uri())
        # Language
        lang_code = data['language']
        password = data.pop('password')
        data.pop('confirm_password', None)
        if password:
                try:
                    api.user_update_password(request, request.user, password)
                    messages.success(request,
                             _('Successfully Password is updated'))
                except:
                    exceptions.handle(request,
                              _('Unable to update the password.'))
        if lang_code and translation.check_for_language(lang_code):
            if hasattr(request, 'session'):
                request.session['django_language'] = lang_code
            else:
                response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)

        # Timezone
        request.session['django_timezone'] = pytz.timezone(data['timezone'])

        messages.success(request, translation.ugettext("Settings saved."))

        return response
