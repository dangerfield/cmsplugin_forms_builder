from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cmsplugin_forms_builder.models import PluginFormModel
from django import forms
from django.core.mail import EmailMessage
from django.utils.translation import ugettext_lazy as _
from forms_builder.forms.forms import FormForForm
from django.conf import settings

class PluginForm(CMSPluginBase):
    model = PluginFormModel
    name = _("Form Builder")
    render_template = "forms/form.html"

    def render(self, context, instance, placeholder):
        request = context['request']
        form = instance.form
        if form.login_required and not request.user.is_authenticated():
            context.update({'form': form})
            return context
        form_for_form = FormForForm(form)
        form_for_form.fields['cms_form_id'] = forms.CharField(initial=form.id, widget=forms.HiddenInput)
        
        try:
            if request.method == 'POST'  and int(request.POST.get('cms_form_id',0)) == form.id:
                form_for_form = FormForForm(form, request.POST, request.FILES)
                if form_for_form.is_valid():
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
                    context.update({'response': form.response})
                    return context
        except ValueError:
            pass

        context.update({
                'form': form,
                'form_for_form': form_for_form,
            }
        )
        return context

plugin_pool.register_plugin(PluginForm)