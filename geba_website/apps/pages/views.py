from django.views.generic import DetailView, UpdateView
from .models import Page
from django.shortcuts import get_object_or_404, render, render_to_response, HttpResponseRedirect
from .forms import PageForm, ContactForm
from django.contrib import messages
import json
from django.core import serializers
from ..core.models import ModelFormFailureHistory
from ..blog.models import Post
from ..project.models import Project, ProjectPost
from django.urls import reverse_lazy
from .utils import check_page_rights
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import RequestContext
# Create your views here.
from ..geba_analytics.signals import object_viewed_signal
from ..geba_analytics.mixins import ObjectViewMixin
from itertools import chain
from django.views.generic import ListView
from ..geba_auth.forms import UserCreationForm


class PageActionMixin(object):

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


def handler404(request, *args, **argv):
    context = RequestContext(request)
    page = get_object_or_404(Page, slug='404')
    user = request.user
    err_code = 404
    response = render_to_response('pages/detail.html', {"code": err_code, "page": page, "user": user}, context)
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    context = RequestContext(request)
    page = get_object_or_404(Page, slug='500')
    user = request.user
    err_code = 500
    response = render_to_response('pages/detail.html', {"code": err_code, "page": page, "user": user}, context)
    response.status_code = 500
    return response


def handler403(request, *args, **argv):
    context = RequestContext(request)
    page = get_object_or_404(Page, slug='403')
    user = request.user
    err_code = 403
    response = render_to_response('pages/detail.html', {"code": err_code, "page": page, "user": user}, context)
    response.status_code = 403
    return response


def handler400(request, *args, **argv):
    context = RequestContext(request)
    page = get_object_or_404(Page, slug='400')
    user = request.user
    err_code = 400
    response = render_to_response('pages/detail.html', {"code": err_code, "page": page, "user": user}, context)
    response.status_code = 400
    return response


class PageDetailView(ObjectViewMixin, DetailView):
    """This view will be used to view the details"""
    # success_msg = 'Comment Added!'
    model = Page  # generic views need to know which model to act upon
    template_name = 'pages/detail.html'  # tells the view to use this template instead of it's default


class PageUpdateView(PageActionMixin, UpdateView):
    model = Page
    success_msg = 'Page Updated!'
    form_class = PageForm
    template_name = 'pages/page_form_update.html'
    # success_url = reverse_lazy('blog:index')

    def get(self, request, slug):
        """when the geba_auth executes a get request, display blank registration form"""
        self.object = self.get_object()

        self.success_url = reverse_lazy('pages:detail', args=self.object.slug)

        form = self.form_class(request.GET or None, request.FILES or None, instance=self.object)
        return render(request, self.template_name, {'form': form})

    # make it so you have to be staff or super-geba_auth to update blog
    def dispatch(self, request, *args, **kwargs):
        request = check_page_rights(request)
        return super(PageUpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        return super(PageUpdateView, self).form_valid(form)


class HomeView(ObjectViewMixin, DetailView):
    """This view will be used to GET the detail data"""
    # success_msg = 'Comment Added!'
    model = Page  # generic views need to know which model to act upon
    template_name = 'pages/home.html'  # tells the view to use this template instead of it's default
    # latest_models = {'LatestBlog': Post, 'LatestProject': Project, 'LatestProjectPost': ProjectPost}

    latest_models = [Project, ProjectPost, Post]
    latest_models_list = ['Latest Project', 'Latest Project Post', 'Latest Blog']

    def get_object(self):
        # make it so only the admin can see items in the future or that are drafts
        # don't use annotate, use vote_by in this case, annotate only works when __iter__ is called
        instance = get_object_or_404(Page, slug='home')
        return instance

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        latest_num = 0
        context['Latest'] = []
        context['Latest_List'] = self.latest_models_list
        for i, latest_model in enumerate(self.latest_models):
            latest_m = latest_model.objects.latest()
            if latest_m:
                context['Latest'].append([self.latest_models_list[i], latest_m])
                latest_num += 1

        context['latest_num'] = latest_num

        return self.render_to_response(context)


class ContactView(DetailView):
    """This view will be used to GET the detail data"""
    # success_msg = 'Comment Added!'
    model = Page  # generic views need to know which model to act upon
    template_name = 'pages/contact.html'  # tells the view to use this template instead of it's default
    form_class = ContactForm
    success_url = reverse_lazy('pages:contact')

    def get_object(self):
        # make it so only the admin can see items in the future or that are drafts
        # don't use annotate, use vote_by in this case, annotate only works when __iter__ is called
        instance = get_object_or_404(Page, slug='contact')

        # for some reason the Contact page doesn't trigger a get_object_data, so ObjectViewedMixin doesn't work
        # connected the signal here
        if instance:
            object_viewed_signal.send(instance.__class__, instance=instance, request=self.request)
        return instance

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.GET or None, request.FILES or None)

        return render(request, self.template_name, {'form': form, 'page': self.object})

    def post(self, request, *args, **kwargs):
        """performs a post request"""

        form = self.form_class(request.POST or None, request.FILES or None)

        if form.is_valid():

            contact_first_name = request.POST.get('contact_first_name')
            contact_last_name = request.POST.get('contact_last_name')
            contact_email = request.POST.get('contact_email')

            contact_content = request.POST.get('contact_content', '')

            template = get_template('pages/contact_template.txt')

            context = {'contact_name': '%s %s' % (contact_first_name, contact_last_name),
                       'contact_email': contact_email,
                       'contact_content': contact_content}

            content = template.render(context)

            subject = 'GEBA Contact Form - %s %s ' % (contact_first_name, contact_last_name)
            from_mail = 'geoff@geba.technology'
            to_mail = ['geoff@geba.technology']
            send_mail(subject, content, from_mail, to_mail, fail_silently=False)

            previous_url = request.META.get('HTTP_REFERER')

            if previous_url:
                url_split = previous_url.split('/')

                if url_split[-2] == 'register' and url_split[-3] == 'auth':
                    # then we were on the registration page, route back to the home page
                    previous_url = '/'

                self.success_url = previous_url + '#contact_sent'
            else:
                pass

            return HttpResponseRedirect(self.success_url)

        else:
            return render_to_response(self.template_name, {'form': form, 'page': self.object})


class SearchAllView(ListView):
    """This view will search be used for searching for all projects and project posts under one view."""

    template_name = 'pages/search.html'  # tells the view to use this template instead of it's default
    context_object_name = 'object_list'  # tell the view to use this context_object_name instead of the default

    def get_context_data(self, *args, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        form = UserCreationForm(self.request.GET or None, self.request.FILES or None)

        context['register_form'] = form
        return context

    def get_queryset(self, *args, **kwargs):
        """
        Excludes any questions that aren't published yet.
        """

        if self.request.user.is_staff or self.request.user.is_superuser:
            blog_qs = Post.objects.all().order_by("-publish_date")
            project_qs = Project.objects.all().order_by("-publish_date")
            project_post_qs = ProjectPost.objects.all().order_by("-publish_date")
        else:
            blog_qs = Post.objects.active()
            project_qs = Project.objects.active()
            project_post_qs = ProjectPost.objects.active()

        query = self.request.GET.get("query")
        if query:
            # this is for searching using the search bar
            blog_qs = Post.objects.search(qs=blog_qs, query=query)
            project_qs = Project.objects.search(qs=project_qs, query=query)
            project_post_qs = ProjectPost.objects.search(qs=project_post_qs, query=query)

        author_query = self.request.GET.get("author")
        if author_query:
            # filter query list by author
            blog_qs = Post.objects.search(qs=blog_qs, query=author_query)
            project_qs = Project.objects.search(qs=project_qs, query=author_query)
            project_post_qs = ProjectPost.objects.search(qs=project_post_qs, query=author_query)

        tag_query = self.request.GET.get("tag")
        if tag_query:
            # filter query list by keyword/tag
            blog_qs = Post.objects.search(qs=blog_qs, query=tag_query)
            project_qs = Project.objects.search(qs=project_qs, query=tag_query)
            project_post_qs = ProjectPost.objects.search(qs=project_post_qs, query=tag_query)

        blog_qs = Post.votes.annotate(queryset=blog_qs, user_id=self.request.user.id)
        project_qs = Project.votes.annotate(queryset=project_qs, user_id=self.request.user.id)
        project_post_qs = ProjectPost.votes.annotate(queryset=project_post_qs, user_id=self.request.user.id)

        queryset_chain = chain(
            blog_qs,
            project_qs,
            project_post_qs,
        )
        qs = sorted(queryset_chain,
                    key=lambda instance: instance.vote_score,
                    reverse=True)
        return qs
