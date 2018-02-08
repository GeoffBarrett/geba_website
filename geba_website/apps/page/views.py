from django.shortcuts import render
from django.contrib import messages
import json
from django.core import serializers
from ..core.models import ModelFormFailureHistory
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView, FormView
from .forms import PagePostForm
from .models import Page
from .utils import check_page_rights
# Create your views here.


class PageActionMixin(object):
    # the fields that user will be able to type in the forms for CreateView
    # fields = ('published', 'title', 'body')

    @property
    def success_msg(self):
        return NotImplemented

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super(PageActionMixin, self).form_valid(form)

    def form_invalid(self, form):
        """saves invalid form and model data for later reference."""
        form_data = json.dumps(form.cleaned_data)
        model_data = serializers.serialize("json",
                                           [form.instance])[1:-1]
        ModelFormFailureHistory.objects.create(form_data=form_data, model_data=model_data)
        return super(PageActionMixin, self).form_invalid(form)


class PageCreateView(PageActionMixin, CreateView):
    model = Page
    success_msg = 'Page Created!'
    form_class = PagePostForm
    template_name = 'page/page_form.html'
    # success_url = '/'
    # Don't need to specify template name due to the html file being named ModelName_form.html

    # make it so you have to be staff or super-user to create blog
    def dispatch(self, request, *args, **kwargs):
        request = check_page_rights(request)
        return super(PageCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        return super(PageCreateView, self).form_valid(form)

    def get(self, request):
        '''when the user executes a get request, display blank registration form'''
        form = self.form_class(self.request.GET or None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """performs a post request"""
        form = self.form_class(request.POST)

        if form.is_valid():
            #self.success_url = reverse_lazy('blog:detail', kwargs={'slug': self.pk})
            instance = form.save(commit=False)  # creates object from the form, doesn't save it to the database just yet
            #if instance.publish_date is None:
            #    instance.publish_date = timezone.now()
            if request.user.get_username() == 'admin':
                instance.author = User.objects.get(username='Geoff')
            else:
                instance.author = request.user

            instance.save()

            return super(BlogCreateView, self).form_valid(form)
        else:
            return render_to_response(request, self.template_name, {'form': form}, context=RequestContext(request))


class BlogUpdateView(BlogActionMixin, UpdateView):
    model = Post
    success_msg = 'Blog Updated!'

    fields = ('title',
              'subtitle',
              'body',
              'image',
              'image_caption',
              'draft',
              'publish_date',
              )

    # make it so you have to be staff or super-user to update blog
    def dispatch(self, request, *args, **kwargs):
        request = check_blog_rights(request)
        return super(BlogUpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        return super(BlogUpdateView, self).form_valid(form)


class BlogDeleteView(BlogActionMixin, DeleteView):
    model = Post
    success_msg = 'Blog Deleted!'
    success_url = reverse_lazy('blog:index')

    # make it so you have to be a super-user or staff to delete
    def dispatch(self, request, *args, **kwargs):
        request = check_blog_rights(request)
        return super(BlogDeleteView, self).dispatch(request, *args, **kwargs)


class BlogDetailView(DetailView):

    model = Post  # generic views need to know which model to act upon
    template_name = 'blog/detail.html'  # tells the view to use this template instead of it's default

    def get_object(self):
        # make it so only the admin can see items in the future or that are drafts
        instance = super(BlogDetailView, self).get_object()
        if instance.draft or instance.publish_date > timezone.now():
            if not self.request.user.is_staff or not self.request.user.is_superuser:
                raise PermissionDenied
        return instance

    '''
    # make it so only
    def dispatch(self, request, *args, **kwargs):
        request = check_blog_rights(request)
        return super(BlogDetailView, self).dispatch(request, *args, **kwargs)
    '''