from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cmsplugin_forms_builder.models import PluginFormModel
from django import forms
from django.core.mail import EmailMessage
from django.utils.translation import ugettext_lazy as _
from forms_builder.forms.forms import FormForForm
from django.conf import settings
from forms_builder.forms.models import Form
from forms_builder.forms.settings import USE_SITES
from django.contrib.sites.models import Site

class PluginForm(CMSPluginBase):
    model = PluginFormModel
    name = _("Form Builder")
    render_template = "cmsplugin_forms_builder/form.html"

    def render(self, context, instance, placeholder):
        request = context['request']
        form = instance.form
        context.update({'form': form, 'published' : True, 'valid': False})
        if form.login_required and not request.user.is_authenticated():
            return context
        
        published = Form.objects.published(for_user=request.user)
        if USE_SITES:
            published = published.filter(sites=Site.objects.get_current())
        if form not in published:
            context.update({'published': False})
            return context
            
        form_for_form = FormForForm(form)
        form_for_form.fields['cms_form_id'] = forms.CharField(initial=form.id, widget=forms.HiddenInput)
        
        try:
            if request.method == 'POST'  and int(request.POST.get('cms_form_id',0)) == form.id:
                form_for_form = FormForForm(form, request.POST, request.FILES)
                if form_for_form.is_valid():
                    context.update({'valid': True})
                    entry = form_for_form.save()
                    fields = ["%s: %s" % (v.label, form_for_form.cleaned_data[k]) for (k, v) in form_for_form.fields.items()]
                    subject = form.email_subject
                    if not subject:
                        subject = "%s - %s" % (form.title, entry.entry_time)
                    body = "\n".join(fields)
                    if form.email_message:
                        body = "%s\n\n%s" % (form.email_message, body)
                    email_from = form.email_from or settings.DEFAULT_FROM_EMAIL
                    email_to = form_for_form.email_to()
                    if email_to and form.send_email:
                        msg = EmailMessage(subject, body, email_from, [email_to])
                        msg.send()
                    email_from = email_to or email_from # Send from the email entered.
                    email_copies = [e.strip() for e in form.email_copies.split(",")
                        if e.strip()]
                    if email_copies:
                        msg = EmailMessage(subject, body, email_from, email_copies)
                        for f in form_for_form.files.values():
                            f.seek(0)
                            msg.attach(f.name, f.read())
                        msg.send()
                    return context
        except ValueError:
            pass

        context.update({'form_for_form': form_for_form})
        return context

plugin_pool.register_plugin(PluginForm)
