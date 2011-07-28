from cms.models.pluginmodel import CMSPlugin

from forms_builder.forms.models import Form
from django.db import models
from django.utils.translation import ugettext_lazy as _

class PluginFormModel(CMSPlugin):
    form = models.ForeignKey(Form, verbose_name=_('form'))