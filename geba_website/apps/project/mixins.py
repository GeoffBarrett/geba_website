from django.contrib import messages
import json
from django.core import serializers
from ..core.models import ModelFormFailureHistory


class ProjectActionMixin(object):
    # the fields that geba_auth will be able to type in the forms for CreateView
    # fields = ('published', 'title', 'body')

    @property
    def success_msg(self):
        return NotImplemented

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super(ProjectActionMixin, self).form_valid(form)

    def form_invalid(self, form):
        """saves invalid form and model data for later reference."""
        form_data = json.dumps(form.cleaned_data)
        model_data = serializers.serialize("json",
                                           [form.instance])[1:-1]
        ModelFormFailureHistory.objects.create(form_data=form_data, model_data=model_data)
        return super(ProjectActionMixin, self).form_invalid(form)
