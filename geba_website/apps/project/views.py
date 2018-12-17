from django.utils import timezone
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from collections import OrderedDict
from django.db.models import Q
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView, FormView, View
from django.core.exceptions import SuspiciousOperation
from django.utils.translation import ugettext as _
from formtools.wizard.forms import ManagementForm
# from django.utils.decorators import method_decorator
# from django.contrib.geba_auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .utils import check_project_rights
from django.shortcuts import render, render_to_response, get_object_or_404
from .models import Project, ProjectPost
from ..comments.forms import CommentForm
from ..comments.models import Comment
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from rest_framework.views import APIView
# from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import authentication, permissions
# from .serializers import ProjectSerializer
from formtools.wizard.views import SessionWizardView
from .forms import ProjectPostForm, ProjectForm
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from ..geba_analytics.mixins import ObjectViewMixin
from ..geba_auth.forms import UserCreationForm
from .mixins import ProjectActionMixin


# ---------- PROJECT VIEWS ---------- #
TRANSFER_FORMS = [
    ("project_form", ProjectForm),
    ("project_post_form", ProjectPostForm),
]
TRANSFER_TEMPLATES = {
    "project_form": "project/project_form_wizard.html",
    "project_post_form": "project/projectpost_form_wizard.html"
}


class ProjectWizard(SessionWizardView):
    form_list = [ProjectForm, ProjectPostForm]
    file_storage = FileSystemStorage(location=settings.MEDIA_ROOT)

    def get_template_names(self):
        return [TRANSFER_TEMPLATES[self.steps.current]]

    def post(self, *args, **kwargs):
        """
        This method handles POST requests.
        The wizard will render either the current step (if form validation
        wasn't successful), the next step (if the current step was stored
        successful) or the done view (if no more steps are available)
        """
        # Look for a wizard_goto_step element in the posted data which
        # contains a valid step name. If one was found, render the requested
        # form. (This makes stepping back a lot easier).
        wizard_goto_step = self.request.POST.get('wizard_goto_step', None)

        if wizard_goto_step and wizard_goto_step in self.get_form_list():
            return self.render_goto_step(wizard_goto_step)

        # added this step to the default so I could skip steps if I wanted to
        wizard_goto_done = self.request.POST.get('wizard_goto_done', None)
        if wizard_goto_done is not None:
            wizard_goto_done = True
        else:
            wizard_goto_done = False

        # Check if form was refreshed
        management_form = ManagementForm(self.request.POST, prefix=self.prefix)
        if not management_form.is_valid():
            raise SuspiciousOperation(_('ManagementForm data is missing or has been tampered.'))

        form_current_step = management_form.cleaned_data['current_step']
        if (form_current_step != self.steps.current and
                self.storage.current_step is not None):
            # form refreshed, change current step
            self.storage.current_step = form_current_step

        # get the form for the current step
        form = self.get_form(data=self.request.POST, files=self.request.FILES)

        # and try to validate
        if form.is_valid():
            # if the form is valid, store the cleaned data and files.
            self.storage.set_step_data(self.steps.current, self.process_step(form))
            self.storage.set_step_files(self.steps.current, self.process_step_files(form))

            # check if the user wants to skip the rest of the steps
            if wizard_goto_done:
                return self.render_done_to_current(form, self.steps.current, **kwargs)

            # check if the current step is the last step
            if self.steps.current == self.steps.last:
                # no more steps, render done view
                return self.render_done(form, **kwargs)
            else:
                # proceed to the next step
                return self.render_next_step(form)
        return self.render(form)

    def render_done_to_current(self, form, current_step, **kwargs):
        """
        This method gets called you have called the wizard_goto_done process. The method should also
        re-validate all steps until the step that initiated this process to prevent manipulation. If any form fails to
        validate, `render_revalidation_failure` should get called.
        If everything is fine call `done`.
        """
        final_forms = OrderedDict()

        # walk through the form list and try to validate the data again.
        for form_key in self.get_form_list():

            form_obj = self.get_form(
                step=form_key,
                data=self.storage.get_step_data(form_key),
                files=self.storage.get_step_files(form_key)
            )
            if not form_obj.is_valid():
                return self.render_revalidation_failure(form_key, form_obj, **kwargs)
            final_forms[form_key] = form_obj

            if form_key == current_step:
                break

        # render the done view and reset the wizard before returning the
        # response. This is needed to prevent from rendering done with the
        # same data twice.
        done_response = self.done(final_forms.values(), form_dict=final_forms, **kwargs)
        self.storage.reset()
        return done_response

    def done(self, form_list, **kwargs):

        for form_key in self.get_form_list():

            if 'project_form' in form_key:
                project_form = self.get_form(
                    step=form_key,
                    data=self.storage.get_step_data(form_key),
                    files=self.storage.get_step_files(form_key)
                )
            elif 'project_post_form' in form_key:
                post_form = self.get_form(
                    step=form_key,
                    data=self.storage.get_step_data(form_key),
                    files=self.storage.get_step_files(form_key)
                )

        if project_form.is_valid():

            project_instance = project_form.save(commit=False)

            # creates object from the form, doesn't save it to the database just yet

            project_instance.save()

            # adding the authors
            project_instance = Project.objects.get(slug=project_instance.slug)
            project_instance.authors.add(self.request.user)
            project_instance.save()

            project_instance.votes.up(self.request.user.id)  # up voting the project

            if post_form.is_valid():
                # object_slug = project_instance.slug
                # project_instance = Project.objects.get(slug=object_slug)

                instance_post = post_form.save(commit=False)
                # creates object from the form, doesn't save it to the database just yet

                instance_post.author = self.request.user

                # we already added this above, don't need to do it again
                # project_instance.authors.add(instance_post.author)
                # project_instance.save()

                instance_post.post_order = 1  # set the default to the 1st post
                instance_post.content_type = project_instance.get_content_type
                instance_post.object_id = project_instance.id

                instance_post.save()

                instance_post.votes.up(self.request.user.id)  # up voting the project post

                return HttpResponseRedirect(reverse_lazy('project:detail', kwargs={'slug': instance_post.slug}))

            return HttpResponseRedirect(reverse_lazy('project:detail', kwargs={'slug': project_instance.slug}))


class ProjectIndexView(ListView):
    template_name = 'project/index.html'  # tells the view to use this template instead of it's default
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
        # current_active_posts = Post.objects.filter(published__lte=timezone.now()).order_by("-published")[:]
        # return Post.objects.filter(draft=False).filter(publish_date=timezone.now()).order_by("-publish_date")[:]
        if self.request.user.is_staff or self.request.user.is_superuser:
            query_set_list = Project.objects.all().order_by("-publish_date")[:]
        else:
            query_set_list = Project.objects.active()[:]

        query = self.request.GET.get("q")

        if query:
            query_set_list = query_set_list.filter(
                Q(title__icontains=query)|
                Q(author__username__icontains=query)
                #Q(body__text__icontains=query)
            ).distinct()

        query_set_list = Project.votes.annotate(queryset=query_set_list, user_id=self.request.user.id)

        return query_set_list


class ProjectUpdateView(ProjectActionMixin, UpdateView):
    model = Project
    success_msg = 'Project Updated!'
    form_class = ProjectForm
    template_name = 'project/project_form_update.html'
    success_url = reverse_lazy('project:index')

    def get(self, request, slug):
        """when the geba_auth executes a get request, display blank registration form"""
        self.object = self.get_object()
        form = self.form_class(request.GET or None, request.FILES or None, instance=self.object)
        return render(request, self.template_name, {'form': form})

    # make it so you have to be staff or super-geba_auth to update blog
    def dispatch(self, request, *args, **kwargs):
        request = check_project_rights(request)
        return super(ProjectUpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        return super(ProjectUpdateView, self).form_valid(form)


class ProjectDeleteView(DeleteView):
    model = Project
    success_url = reverse_lazy('project:index')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return HttpResponseRedirect(reverse('project:detail', args=(self.object.slug)))

    # make it so you have to be a super-geba_auth or staff to delete
    def dispatch(self, request, *args, **kwargs):
        request = check_project_rights(request)
        return super(ProjectDeleteView, self).dispatch(request, *args, **kwargs)


class ProjectDetailGetView(ObjectViewMixin, DetailView):
    """This view will be used to GET the detail data"""
    model = Project  # generic views need to know which model to act upon
    template_name = 'project/detail.html'  # tells the view to use this template instead of it's default
    success_url = reverse_lazy('project:index')
    form_class = CommentForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        # the original get defines self.object, this is required otherwise you get an error stating that there is no
        # attribute 'object' in this DetailView

        instance = self.object
        context = self.get_context_data(object=self.object)
        initial_data = {
            'content_type': instance.get_content_type,
            'object_id': instance.id,
        }
        comment_form = self.form_class(request.POST or None, initial=initial_data)
        context['comment_form'] = comment_form

        register_form = UserCreationForm(self.request.GET or None, self.request.FILES or None)
        context['register_form'] = register_form

        return self.render_to_response(context)

    def get_object(self):
        # make it so only the admin can see items in the future or that are drafts
        instance = super(ProjectDetailGetView, self).get_object()
        if instance.draft or instance.publish_date > timezone.now():
            if not self.request.user.is_staff or not self.request.user.is_superuser:
                raise PermissionDenied

        # don't use annotate, use vote_by in this case, annotate only works when __iter__ is called
        instance = Project.votes.vote_by(self.request.user.id, ids=[instance.id])[0]

        return instance

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailGetView, self).get_context_data(**kwargs)

        comment_qs = context['object'].comments
        # getting the vote info

        context['comments'] = Comment.votes.annotate(queryset=comment_qs, user_id=self.request.user.id)

        return context


class ProjectDetailPostView(SingleObjectMixin, FormView):
    """This view will be used to POST the detail data

    SingleObjectMixin = Provides a mechanism for looking up an object associated with the current HTTP request.
    """
    template_name = 'project/detail.html'  # tells the view to use this template instead of it's default
    form_class = CommentForm
    model = Project  # generic views need to know which model to act upon

    def post(self, request, *args, **kwargs):
        # comment_form = self.form_class(request.POST, request.FILES)
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        self.object = self.get_object()
        self.object = Project.votes.annotate(queryset=Project.objects.filter(slug=self.kwargs.get('slug')),
                                             user_id=self.request.user.id)[0]

        form = self.form_class(request.POST)
        if form.is_valid():
            content_type = ContentType.objects.get_for_model(Project)
            object_id = form.cleaned_data.get("object_id")
            content_data = form.cleaned_data.get("content")
            parent_object = None

            # check if it has a parent_id
            try:
                parent_id = int(request.POST.get("parent_id"))
            except:
                parent_id = None

            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists():
                    parent_object = parent_qs.first()  # get the first object in that queryset

            new_comment, created = Comment.objects.get_or_create(
                author=request.user,
                content_type=content_type,
                object_id=object_id,
                content=content_data,
                parent=parent_object
            )

        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('project:detail', kwargs={'slug': self.object.slug})


# ----------  Both View  ---------- #


class ProjectDetailView(View):
    """
    This view will be used to ensure that one is for GET and the other for POST
    we will use this for both the Project and the ProjectPost since I want them to have the same url structure
    """

    def get(self, request, *args, **kwargs):

        qs = Project.objects.filter(slug=kwargs['slug'])

        if qs.exists():
            # Then it is a Project slug
            view = ProjectDetailGetView.as_view()
            # pass
        else:
            view = ProjectPostDetailGetView.as_view()

        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        qs = Project.objects.filter(slug=kwargs['slug'])

        if qs.exists():
            # Then it is a Project slug
            view = ProjectDetailPostView.as_view()
            # pass
        else:
            view = ProjectPostDetailPostView.as_view()

        return view(request, *args, **kwargs)


# ---------- PROJECT POST VIEW  ---------- #

class ProjectPostDetailGetView(ObjectViewMixin, DetailView):
    """This view will be used to GET the detail data"""
    # success_msg = 'Comment Added!'
    model = ProjectPost  # generic views need to know which model to act upon
    template_name = 'project/post_detail.html'  # tells the view to use this template instead of it's default
    success_url = reverse_lazy('project:index')
    form_class = CommentForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        # the original get defines self.object, this is required otherwise you get an error stating that there is no
        # attribute 'object' in this DetailView

        instance = self.object
        context = self.get_context_data(object=self.object)
        initial_data = {
            'content_type': instance.get_content_type,
            'object_id': instance.id,
        }
        comment_form = self.form_class(request.POST or None, initial=initial_data)
        context['comment_form'] = comment_form

        register_form = UserCreationForm(self.request.GET or None, self.request.FILES or None)
        context['register_form'] = register_form

        return self.render_to_response(context)

    def get_object(self):
        # make it so only the admin can see items in the future or that are drafts
        instance = super(ProjectPostDetailGetView, self).get_object()
        if instance.draft or instance.publish_date > timezone.now():
            if not self.request.user.is_staff or not self.request.user.is_superuser:
                raise PermissionDenied

        # make it so users cannot see any of the posts if the project is a draft
        parent = instance.get_project()

        if parent.draft or parent.publish_date > timezone.now():
            if not self.request.user.is_staff or not self.request.user.is_superuser:
                raise PermissionDenied

        # qs = ProjectPost.objects.filter(slug=self.kwargs.get('slug'))

        # instance = ProjectPost.votes.annotate(queryset=qs, user_id=self.request.geba_auth.id)[0]
        # don't use annotate, use vote_by in this case, annotate only works when __iter__ is called
        instance = ProjectPost.votes.vote_by(self.request.user.id, ids=[instance.id])[0]

        return instance

    def get_context_data(self, **kwargs):
        context = super(ProjectPostDetailGetView, self).get_context_data(**kwargs)
        # context['object'] provides the instance for us

        comment_qs = context['object'].comments
        # getting the vote info

        # context['comments'] = comment_qs
        context['comments'] = Comment.votes.annotate(queryset=comment_qs, user_id=self.request.user.id)

        # context['comment_form'] = CommentForm()
        return context


class ProjectPostDetailPostView(SingleObjectMixin, FormView):
    """This view will be used to POST the detail data

    SingleObjectMixin = Provides a mechanism for looking up an object associated with the current HTTP request.
    """
    template_name = 'project/post_detail.html'  # tells the view to use this template instead of it's default
    form_class = CommentForm
    model = ProjectPost  # generic views need to know which model to act upon

    def post(self, request, *args, **kwargs):
        # comment_form = self.form_class(request.POST, request.FILES)
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        self.object = self.get_object()
        self.object = ProjectPost.votes.annotate(queryset=ProjectPost.objects.filter(slug=self.kwargs.get('slug')),
                                                 user_id=self.request.user.id)[0]

        form = self.form_class(request.POST)
        if form.is_valid():
            # c_type = form.cleaned_data.get("content_type")
            # content_type = ContentType.objects.get(model=c_type)
            content_type = ContentType.objects.get_for_model(ProjectPost)
            object_id = form.cleaned_data.get("object_id")
            content_data = form.cleaned_data.get("content")
            parent_object = None

            # check if it has a parent_id
            try:
                parent_id = int(request.POST.get("parent_id"))
            except:
                parent_id = None

            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists():
                    parent_object = parent_qs.first()  # get the first object in that queryset

            new_comment, created = Comment.objects.get_or_create(
                author=request.user,
                content_type=content_type,
                object_id=object_id,
                content=content_data,
                parent=parent_object
            )

        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('project:detail', kwargs={'slug': self.object.slug})


class ProjectPostUpdateView(ProjectActionMixin, UpdateView):
    model = ProjectPost
    success_msg = 'Post Updated!'
    form_class = ProjectPostForm
    template_name = 'project/project_post_form_update.html'
    # success_url = reverse_lazy('project:index')

    def get(self, request, slug):
        """when the geba_auth executes a get request, display blank registration form"""
        self.object = self.get_object()
        self.success_url = reverse_lazy('project:detail', args=self.object.slug)
        form = self.form_class(request.GET or None, request.FILES or None, instance=self.object)
        return render(request, self.template_name, {'form': form})

    # make it so you have to be staff or super-geba_auth to update blog
    def dispatch(self, request, *args, **kwargs):
        request = check_project_rights(request)
        return super(ProjectPostUpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        return super(ProjectPostUpdateView, self).form_valid(form)


class ProjectPostDeleteView(DeleteView):

    model = ProjectPost
    # success_msg = 'Blog Deleted!'
    success_url = reverse_lazy('project:index')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return HttpResponseRedirect(reverse('project:detail', args=self.object.slug))

    # make it so you have to be a super-geba_auth or staff to delete
    def dispatch(self, request, *args, **kwargs):
        request = check_project_rights(request)
        return super(ProjectPostDeleteView, self).dispatch(request, *args, **kwargs)


class ProjectPostCreateView(ProjectActionMixin, CreateView):
    model = ProjectPost
    success_msg = 'Post Created!'
    form_class = ProjectPostForm
    template_name = 'project/project_post_form.html'
    # success_url = '/'  # if no success_url is given, it will use the get_absolute_url() on the object if available
    # Don't need to specify template name due to the html file being named ModelName_form.html

    # make it so you have to be staff or super-geba_auth to create blog
    def dispatch(self, request, *args, **kwargs):
        request = check_project_rights(request)

        return super(ProjectPostCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        return super(ProjectPostCreateView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        """when the geba_auth executes a get request, display blank registration form"""
        form = self.form_class(request.GET or None, request.FILES or None)
        # context = self.get_context_data()
        return render(request, self.template_name, {'form': form, 'project_slug': kwargs['slug'],
                                                    'new_post_order': kwargs['post_order']})

    def post(self, request, *args, **kwargs):
        """performs a post request"""

        form = self.form_class(request.POST or None, request.FILES or None)

        if form.is_valid():

            # object_slug = kwargs['slug']
            object_slug = self.kwargs.get("slug")  # get the post slug

            project_instance = get_object_or_404(Project, slug=object_slug)  # get the project instance
            # project_instance = Project.objects.get(slug=object_slug)

            instance = form.save(commit=False)
            # creates object from the form, doesn't save it to the database just yet

            if request.user.get_username() == 'admin':
                instance.author = request.user
                pass
                # instance.author = User.objects.get(username='Geoff')
            else:
                instance.author = request.user

            # instance.post_order = kwargs['post_order']  # set the default to the 1st post
            instance.post_order = self.kwargs.get('post_order')  # set the default to the 1st post

            instance.content_type = project_instance.get_content_type
            instance.object_id = project_instance.id
            instance.save()

            # instance = ProjectPost.objects.get(id=instance.id)
            project_instance.pages.add(instance)

            if instance.author not in project_instance.authors.all():
                project_instance.authors.add(instance.author)

            project_instance.save()

            # obj = get_object_or_404(ProjectPost, id=instance.id)
            instance.votes.up(request.user.id)

            return HttpResponseRedirect(reverse_lazy('project:detail', kwargs={'slug': instance.slug}))
            # return super(ProjectPostCreateView, self).form_valid(form)

        else:
            return render_to_response(self.template_name, {'form': form, 'project_slug': kwargs['slug'],
                                                    'new_post_order': kwargs['post_order']})

# ----------voting ---------- #


UP = 0
DOWN = 1


class ProjectPostLikeToggleAjax(APIView):

    authentication_classes = (authentication.SessionAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, slug=None, format=None):
        # slug = self.kwargs.get("slug")
        obj = get_object_or_404(ProjectPost, slug=slug)
        # url_ = obj.get_absolute_url()  # get the url of the project post
        user = self.request.user  # get the geba_auth
        updated = False
        liked = False

        if user.is_authenticated:
            # check if the geba_auth is authenticated
            # check if the geba_auth has already voted on this object
            if obj.votes.exists(user.id, action=UP):
                obj.votes.delete(user.id)
                liked = False
            else:
                # upvote the object
                obj.votes.up(user.id)
                liked = True

            updated = True

        data = {'updated': updated,
                'liked': liked}

        return Response(data)


class ProjectPostDislikeToggleAjax(APIView):

    authentication_classes = (authentication.SessionAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, slug=None, format=None):
        # slug = self.kwargs.get("slug")
        obj = get_object_or_404(ProjectPost, slug=slug)
        # url_ = obj.get_absolute_url()  # get the url of the project post
        user = self.request.user  # get the geba_auth
        updated = False
        disliked = False

        if user.is_authenticated:

            # check if the geba_auth is authenticated
            # check if the geba_auth has already voted on this object
            if obj.votes.exists(user.id, action=DOWN):
                obj.votes.delete(user.id)
                disliked = False
            else:
                # downvote the object
                obj.votes.down(user.id)
                disliked = True

            updated = True

        data = {'updated': updated,
                'disliked': disliked}

        return Response(data)


class ProjectLikeToggleAjax(APIView):

    authentication_classes = (authentication.SessionAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, slug=None, format=None):
        # slug = self.kwargs.get("slug")
        obj = get_object_or_404(Project, slug=slug)
        # url_ = obj.get_absolute_url()  # get the url of the project post
        user = self.request.user  # get the geba_auth
        updated = False
        liked = False

        if user.is_authenticated:

            # check if the geba_auth is authenticated
            # check if the geba_auth has already voted on this object
            if obj.votes.exists(user.id, action=UP):
                obj.votes.delete(user.id)
                liked = False
            else:
                # upvote the object
                obj.votes.up(user.id)
                liked = True

            updated = True

        data = {'updated': updated,
                'liked': liked}

        return Response(data)


class ProjectDislikeToggleAjax(APIView):

    authentication_classes = (authentication.SessionAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, slug=None, format=None):
        # slug = self.kwargs.get("slug")
        obj = get_object_or_404(Project, slug=slug)
        # url_ = obj.get_absolute_url()  # get the url of the project post
        user = self.request.user  # get the geba_auth
        updated = False
        disliked = False

        if user.is_authenticated:

            # check if the geba_auth is authenticated
            # check if the geba_auth has already voted on this object
            if obj.votes.exists(user.id, action=DOWN):
                obj.votes.delete(user.id)
                disliked = False
            else:
                # downvote the object
                obj.votes.down(user.id)
                disliked = True

            updated = True

        data = {'updated': updated,
                'disliked': disliked}

        return Response(data)


class PublishProjectPostAjax(APIView):

    authentication_classes = (authentication.SessionAuthentication, )
    permission_classes = (permissions.IsAdminUser, )

    def get(self, request, slug=None, format=None):
        # slug = self.kwargs.get("slug")
        obj = get_object_or_404(ProjectPost, slug=slug)
        # url_ = obj.get_absolute_url()  # get the url of the project post
        user = self.request.user  # get the geba_auth
        updated = False
        published = False

        if user.is_authenticated:

            # check if the geba_auth is authenticated
            # check if the post is already published
            if not obj.draft:
                published = False
            else:
                # set the post as not a draft
                obj.draft = False
                obj.save()
                obj.votes.down(user.id)
                published = True

            updated = True

        data = {'updated': updated,
                'published': published}

        return Response(data)


class MakeDraftProjectPostAjax(APIView):

    authentication_classes = (authentication.SessionAuthentication, )
    permission_classes = (permissions.IsAdminUser, )

    def get(self, request, slug=None, format=None):
        # slug = self.kwargs.get("slug")
        obj = get_object_or_404(ProjectPost, slug=slug)
        # url_ = obj.get_absolute_url()  # get the url of the project post
        user = self.request.user  # get the geba_auth
        updated = False
        drafted = False

        if user.is_authenticated:

            # check if the geba_auth is authenticated
            # check if the post is already a draft
            if obj.draft:
                drafted = False
            else:
                # make the post a draft
                obj.draft = True
                obj.save()
                drafted = True

            updated = True

        data = {'updated': updated,
                'drafted': drafted}

        return Response(data)


class PublishProjectAjax(APIView):

    authentication_classes = (authentication.SessionAuthentication, )
    permission_classes = (permissions.IsAdminUser, )

    def get(self, request, slug=None, format=None):
        # slug = self.kwargs.get("slug")
        obj = get_object_or_404(Project, slug=slug)
        # url_ = obj.get_absolute_url()  # get the url of the project post
        user = self.request.user  # get the geba_auth
        updated = False
        published = False

        if user.is_authenticated:

            # check if the geba_auth is authenticated
            # check if the post is already published
            if not obj.draft:
                published = False
            else:
                # set the post as not a draft
                obj.draft = False
                obj.save()
                obj.votes.down(user.id)
                published = True

            updated = True

        data = {'updated': updated,
                'published': published}

        return Response(data)


class MakeDraftProjectAjax(APIView):

    authentication_classes = (authentication.SessionAuthentication, )
    permission_classes = (permissions.IsAdminUser, )

    def get(self, request, slug=None, format=None):
        # slug = self.kwargs.get("slug")
        obj = get_object_or_404(Project, slug=slug)
        # url_ = obj.get_absolute_url()  # get the url of the project post
        user = self.request.user  # get the geba_auth
        updated = False
        drafted = False

        if user.is_authenticated:

            # check if the geba_auth is authenticated
            # check if the post is already a draft
            if obj.draft:
                drafted = False
            else:
                # make the post a draft
                obj.draft = True
                obj.save()
                drafted = True

            updated = True

        data = {'updated': updated,
                'drafted': drafted}

        return Response(data)
