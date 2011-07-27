from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cmsplugin_forms_builder.models import PluginFormModel
from django import forms
from django.utils.translation import ugettext_lazy as _
from forms_builder.forms.forms import FormForForm

class PluginForm(CMSPluginBase):
    model = PluginFormModel
    name = _("Form Builder")
    render_template = "forms/form.html"

    def render(self, context, instance, placeholder):
        request = context['request']
        form = instance.form
        form_for_form = FormForForm(form)
        form_for_form.fields['cms_form_id'] = forms.CharField(initial=form.id, widget=forms.HiddenInput)
        
        try:
            if request.method == 'POST'  and int(request.POST.get('cms_form_id',0)) == form.id:
                form_for_form = FormForForm(form, request.POST, request.FILES)
                if form_for_form.is_valid():
                    form_for_form.save()
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