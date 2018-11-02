from .signals import object_viewed_signal


class ObjectViewMixin(object):

    def get_context_data(self, *args, **kwargs):
        # get the context
        context = super(ObjectViewMixin, self).get_context_data(*args, **kwargs)
        # define instance
        instance = context['object']

        print(instance, '-------------------')
        if instance:
            # if instance exists, emit signal
            object_viewed_signal.send(instance.__class__, instance=instance, request=self.request)
        return context