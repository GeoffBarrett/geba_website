from django.utils import timezone
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView, FormView, View, \
    TemplateView
from django.contrib import messages
# from django.utils.decorators import method_decorator
# from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core import serializers
from .utils import check_project_rights
import json, os
from django.shortcuts import render, render_to_response, get_object_or_404
from .models import Project, ProjectPost
from ..core.models import ModelFormFailureHistory
from .forms import ProjectPostForm, ProjectForm
from ..comments.forms import CommentForm
from ..comments.models import Comment
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.contrib.contenttypes.models import ContentType
from rest_framework.views import APIView
# from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import authentication, permissions, status
from .serializers import ProjectSerializer
from formtools.wizard.views import SessionWizardView, WizardView
from .forms import ProjectPostForm, ProjectForm
from django.core.files.storage import FileSystemStorage
from django.conf import settings


class ProjectActionMixin(object):
    # the fields that user will be able to type in the forms for CreateView
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


# ---------- PROJECT VIEWS ---------- #
TRANSFER_FORMS = [
    ("project_form", ProjectForm),
    ("project_post_form", ProjectPostForm),
]
TRANSFER_TEMPLATES = {
    "project_form": "project/project_form2.html",
    "project_post_form": "project/project_form3.html"
}


class ProjectWizard(SessionWizardView):
    form_list = [ProjectForm, ProjectPostForm]
    file_storage = FileSystemStorage(location=settings.MEDIA_ROOT)

    def get_template_names(self):
        return [TRANSFER_TEMPLATES[self.steps.current]]

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

            project_instance.votes.up(self.request.user.id)  # up voting the project

            if post_form.is_valid():

                object_slug = project_instance.slug

                project_instance = Project.objects.get(slug=object_slug)

                instance_post = post_form.save(commit=False)
                # creates object from the form, doesn't save it to the database just yet

                if self.request.user.get_username() == 'admin':
                    # instance_post.author = User.objects.get(username='Geoff')
                    instance_post.author = self.request.user
                    pass
                else:
                    instance_post.author = self.request.user

                project_instance.authors.add(instance_post.author)
                project_instance.save()

                instance_post.post_order = 1  # set the default to the 1st post
                instance_post.content_type = project_instance.get_content_type
                instance_post.object_id = project_instance.id

                # project_instance.save()
                instance_post.save()

                instance_post.votes.up(self.request.user.id)  # up voting the project post

        return HttpResponseRedirect(reverse_lazy('project:index'))


class ProjectIndexView(ListView):
    template_name = 'project/index.html'  # tells the view to use this template instead of it's default
    context_object_name = 'object_list'  # tell the view to use this context_object_name instead of the default

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


class ProjectCreateGetView(TemplateView):

    project_form = ProjectForm
    post_form = ProjectPostForm
    success_url = '/'

    template_name = 'project/project_form.html'

    def get(self, request):
        """when the user executes a get request, display blank form"""
        project_form = self.project_form(request.GET or None, request.FILES or None)
        post_form = self.post_form(request.GET or None, request.FILES or None)
        return render(request, self.template_name, {'project_form': project_form, 'post_form': post_form})


class ProjectCreationPostView(FormView):

    project_form = ProjectForm
    post_form = ProjectPostForm

    template_name = 'project/project_form.html'

    success_url = reverse_lazy('project:index')

    def post(self, request, *args, **kwargs):

        project_form = self.project_form(request.POST)
        post_form = self.post_form(request.POST)

        if project_form.is_valid():

            project_instance = project_form.save(commit=False)

            # creates object from the form, doesn't save it to the database just yet

            project_instance.save()

            project_instance.votes.up(request.user.id)  # up voting the project

            return super(ProjectCreationPostView, self).form_valid(post_form)
        else:
            # return render_to_response(self.template_name, {'project_form': project_form, 'post_form': post_form})
            return render(request, self.template_name, {'project_form': project_form, 'post_form': post_form})


class ProjectUpdateView(ProjectActionMixin, UpdateView):
    model = Project
    success_msg = 'Project Updated!'
    form_class = ProjectPostForm
    template_name = 'project/project_form.html'
    success_url = reverse_lazy('project:index')

    def get(self, request, slug):
        '''when the user executes a get request, display blank registration form'''
        form = self.form_class(request.GET or None, request.FILES or None)
        return render(request, self.template_name, {'form': form})

    # def get_object(self, queryset=None):
    #     obj = Post.objects.get(slug=self.kwargs['slug'])
    #     return obj

    # make it so you have to be staff or super-user to update blog
    def dispatch(self, request, *args, **kwargs):
        request = check_project_rights(request)
        return super(ProjectUpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        return super(ProjectUpdateView, self).form_valid(form)


class ProjectDeleteView(DeleteView):
    # template_name = 'blog/post_confirm_delete.html'
    model = Project
    # success_msg = 'Blog Deleted!'
    success_url = reverse_lazy('project:index')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        # print(reverse('project:detail', args=(self.object.slug)))
        return HttpResponseRedirect(reverse('project:detail', args=(self.object.slug)))

    # make it so you have to be a super-user or staff to delete
    def dispatch(self, request, *args, **kwargs):
        request = check_project_rights(request)
        return super(ProjectDeleteView, self).dispatch(request, *args, **kwargs)

# ---------- unused --------------- #

'''
class ProjectDetailGetView(DetailView):
    """This view will be used to GET the detail data"""
    # success_msg = 'Comment Added!'
    model = ProjectPost  # generic views need to know which model to act upon
    template_name = 'project/detail.html'  # tells the view to use this template instead of it's default
    success_url = reverse_lazy('project:index')
    form_class = CommentForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object = ProjectPost.votes.annotate(queryset=ProjectPost.objects.filter(slug=self.kwargs.get('slug')),
                               user_id=self.request.user.id)[0]

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
        return self.render_to_response(context)

    def get_object(self):
        # make it so only the admin can see items in the future or that are drafts
        instance = super(ProjectDetailGetView, self).get_object()
        if instance.draft or instance.publish_date > timezone.now():
            if not self.request.user.is_staff or not self.request.user.is_superuser:
                raise PermissionDenied
        return instance

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailGetView, self).get_context_data(**kwargs)
        # context['object'] provides the instance for us
        context['comments'] = context['object'].comments

        # context['comment_form'] = CommentForm()
        return context
'''

'''
class ProjectDetailPostView(SingleObjectMixin, FormView):
    """This view will be used to POST the detail data

    SingleObjectMixin = Provides a mechanism for looking up an object associated with the current HTTP request.
    """
    # template_name = 'project/detail.html'  # tells the view to use this template instead of it's default
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
            c_type = form.cleaned_data.get("content_type")
            content_type = ContentType.objects.get(model=c_type)
            object_id = form.cleaned_data.get("object_id")
            content_data = form.cleaned_data.get("content")
            parent_object = None
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
'''

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
            # view = ProjectDetailGetView.as_view()
            pass
        else:
            view = ProjectPostDetailGetView.as_view()

        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        qs = Project.objects.filter(slug=kwargs['slug'])

        if qs.exists():
            # Then it is a Project slug
            # view = ProjectDetailPostView.as_view()
            pass
        else:
            view = ProjectPostDetailPostView.as_view()

        return view(request, *args, **kwargs)


# ---------- PROJECT POST VIEW  ---------- #

class ProjectPostCreationPostView(FormView):

    project_form = ProjectForm
    post_form = ProjectPostForm

    # form_class = ProjectForm
    template_name = 'project/project_form.html'

    success_url = '/'

    def post(self, request, *args, **kwargs):

        # project_form = self.project_form(request.POST)

        project_form = self.request.session['project_form']

        post_form = self.post_form(request.POST or None)

        if post_form.is_valid():
            project_instance = project_form.save(commit=False)
            project_instance.save()
            project_instance.votes.up(request.user.id)  # up voting the project

            object_slug = project_instance.slug

            project_instance = Project.objects.get(slug=object_slug)

            instance_post = post_form.save(commit=False)
            # creates object from the form, doesn't save it to the database just yet

            if request.user.get_username() == 'admin':
                # instance_post.author = User.objects.get(username='Geoff')
                instance_post.author = request.user
                pass
            else:
                instance_post.author = request.user

            project_instance.authors.add(instance_post.author)
            project_instance.save()

            instance_post.post_order = 1  # set the default to the 1st post
            instance_post.content_type = project_instance.get_content_type
            instance_post.object_id = project_instance.id

            # project_instance.save()
            instance_post.save()

            instance_post.votes.up(request.user.id)  # up voting the project post

        else:

            # figure out what to do if this
            # return render_to_response(self.template_name, {'project_form': project_form, 'post_form': post_form})
            return render(request, self.template_name, {'project_form': project_form, 'post_form': post_form})

        return super(ProjectPostCreationPostView, self).form_valid(post_form)


class ProjectPostDetailGetView(DetailView):
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

        qs = ProjectPost.objects.filter(slug=self.kwargs.get('slug'))

        # instance = ProjectPost.votes.annotate(queryset=qs, user_id=self.request.user.id)[0]
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
    success_url = reverse_lazy('project:index')

    def get_initial(self):
        initial = super(ProjectPostUpdateView, self).get_initial()
        print('initial data', initial)

        # retrieve current object
        projectpost_object = self.get_object()

        initial['field1'] = projectpost_object.field1
        initial['field2'] = projectpost_object.field2
        return initial

    def get(self, request, slug):
        '''when the user executes a get request, display blank registration form'''
        form = self.form_class(request.GET or None, request.FILES or None)
        return render(request, self.template_name, {'form': form})

    # def get_object(self, queryset=None):
    #     obj = Post.objects.get(slug=self.kwargs['slug'])
    #     return obj

    # make it so you have to be staff or super-user to update blog
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
        return HttpResponseRedirect(reverse('project:detail', args=(self.object.slug)))

    # make it so you have to be a super-user or staff to delete
    def dispatch(self, request, *args, **kwargs):
        request = check_project_rights(request)
        return super(ProjectPostDeleteView, self).dispatch(request, *args, **kwargs)


class ProjectPostCreateView(ProjectActionMixin, CreateView):
    model = ProjectPost
    success_msg = 'Post Created!'
    form_class = ProjectPostForm
    # template_name = 'project/project_post_form2.html'
    template_name = 'project/project_post_form.html'
    # success_url = '/'  # if no success_url is given, it will use the get_absolute_url() on the object if available
    # Don't need to specify template name due to the html file being named ModelName_form.html

    # make it so you have to be staff or super-user to create blog
    def dispatch(self, request, *args, **kwargs):
        request = check_project_rights(request)

        return super(ProjectPostCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        return super(ProjectPostCreateView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        '''when the user executes a get request, display blank registration form'''
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

            # return HttpResponseRedirect(self.get_success_url())
            return super(ProjectPostCreateView, self).form_valid(form)

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
        user = self.request.user  # get the user
        updated = False
        liked = False

        if user.is_authenticated:
            # check if the user is authenticated
            # check if the user has already voted on this object
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
        user = self.request.user  # get the user
        updated = False
        disliked = False

        if user.is_authenticated:

            # check if the user is authenticated
            # check if the user has already voted on this object
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

    '''
    @method_decorator(login_required(login_url=reverse_lazy('core:signin')))
    def dispatch(self, *args, **kwargs):
        return super(ProjectLikeToggleAjax, self).dispatch(*args, **kwargs)
    '''

    def get(self, request, slug=None, format=None):
        # slug = self.kwargs.get("slug")
        obj = get_object_or_404(Project, slug=slug)
        # url_ = obj.get_absolute_url()  # get the url of the project post
        user = self.request.user  # get the user
        updated = False
        liked = False

        if user.is_authenticated:

            # check if the user is authenticated
            # check if the user has already voted on this object
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
        user = self.request.user  # get the user
        updated = False
        disliked = False

        if user.is_authenticated:

            # check if the user is authenticated
            # check if the user has already voted on this object
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
        user = self.request.user  # get the user
        updated = False
        published = False

        if user.is_authenticated:

            # check if the user is authenticated
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
        user = self.request.user  # get the user
        updated = False
        drafted = False

        if user.is_authenticated:

            # check if the user is authenticated
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
        user = self.request.user  # get the user
        updated = False
        published = False

        if user.is_authenticated:

            # check if the user is authenticated
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
        user = self.request.user  # get the user
        updated = False
        drafted = False

        if user.is_authenticated:

            # check if the user is authenticated
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