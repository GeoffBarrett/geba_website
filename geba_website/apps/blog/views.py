from django.utils import timezone
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView, FormView, View
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.core import serializers
from .utils import check_blog_rights
import json
from django.shortcuts import render, render_to_response, get_object_or_404
from .models import Post
from ..core.models import ModelFormFailureHistory, User
from .forms import BlogPostForm
from ..comments.forms import CommentForm
from ..comments.models import Comment
from django.core.urlresolvers import reverse
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
# from ..vote.models import Vote


class BlogActionMixin(object):
    # the fields that user will be able to type in the forms for CreateView
    # fields = ('published', 'title', 'body')

    @property
    def success_msg(self):
        return NotImplemented

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super(BlogActionMixin, self).form_valid(form)

    def form_invalid(self, form):
        """saves invalid form and model data for later reference."""
        form_data = json.dumps(form.cleaned_data)
        model_data = serializers.serialize("json",
                                           [form.instance])[1:-1]
        ModelFormFailureHistory.objects.create(form_data=form_data, model_data=model_data)
        return super(BlogActionMixin, self).form_invalid(form)

'''
class AjaxTemplateMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(self, 'ajax_template_name'):
            split = self.template_name.split('.html')
            split[-1] = '_inner'
            split.append('.html')
            self.ajax_template_name = ''.join(split)
        if request.is_ajax():
            self.template_name = self.ajax_template_name

        return super(AjaxTemplateMixin, self).dispatch(request, *args, **kwargs)
'''


class BlogIndexView(ListView):
    template_name = 'blog/index.html'  # tells the view to use this template instead of it's default
    context_object_name = 'object_list'  # tell the view to use this context_object_name instead of the default

    def get_queryset(self, *args, **kwargs):
        """
        Excludes any questions that aren't published yet.
        """
        # current_active_posts = Post.objects.filter(published__lte=timezone.now()).order_by("-published")[:]
        # return Post.objects.filter(draft=False).filter(publish_date=timezone.now()).order_by("-publish_date")[:]
        if self.request.user.is_staff or self.request.user.is_superuser:
            query_set_list = Post.objects.all().order_by("-publish_date")[:]
        else:
            query_set_list = Post.objects.active()[:]

        # now we must pass this query_set into the annotate (or voted_by) method to get the is_voted_up or is_voted_down

        query = self.request.GET.get("q")

        if query:
            # this is for searching using the search bar
            query_set_list = query_set_list.filter(
                Q(title__icontains=query)|
                Q(author__username__icontains=query)
                #Q(body__text__icontains=query)
            ).distinct()
        '''
        paginator = Paginator(query_set_list, 5)  # shows 25 posts per page
        page_request_var = 'page'
        page = self.request.GET.get(page_request_var)
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)
        '''

        query_set_list = Post.votes.annotate(queryset=query_set_list, user_id=self.request.user.id)

        return query_set_list


class BlogCreateView(BlogActionMixin, CreateView):
    model = Post
    success_msg = 'Blog Created!'
    form_class = BlogPostForm
    template_name = 'blog/post_form.html'
    # success_url = '/'
    # Don't need to specify template name due to the html file being named ModelName_form.html

    # make it so you have to be staff or super-user to create blog
    def dispatch(self, request, *args, **kwargs):
        request = check_blog_rights(request)
        return super(BlogCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        return super(BlogCreateView, self).form_valid(form)

    def get(self, request):
        '''when the user executes a get request, display blank registration form'''
        form = self.form_class(request.GET or None, request.FILES or None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """performs a post request"""
        form = self.form_class(request.POST or None, request.FILES or None)

        if form.is_valid():

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
            return render_to_response(self.template_name, {'form': form})


class BlogUpdateView(BlogActionMixin, UpdateView):
    model = Post
    success_msg = 'Blog Updated!'
    form_class = BlogPostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:index')

    def get(self, request, slug):
        '''when the user executes a get request, display blank registration form'''
        form = self.form_class(request.GET or None, request.FILES or None)
        return render(request, self.template_name, {'form': form})

    # def get_object(self, queryset=None):
    #     obj = Post.objects.get(slug=self.kwargs['slug'])
    #     return obj

    # make it so you have to be staff or super-user to update blog
    def dispatch(self, request, *args, **kwargs):
        request = check_blog_rights(request)
        return super(BlogUpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        return super(BlogUpdateView, self).form_valid(form)


class BlogDeleteView(DeleteView):
    # template_name = 'blog/post_confirm_delete.html'
    model = Post
    # success_msg = 'Blog Deleted!'
    success_url = reverse_lazy('blog:index')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return HttpResponseRedirect(reverse('blog:detail', args=(self.object.slug)))

    # make it so you have to be a super-user or staff to delete
    def dispatch(self, request, *args, **kwargs):
        request = check_blog_rights(request)
        return super(BlogDeleteView, self).dispatch(request, *args, **kwargs)


class BlogDetailGetView(DetailView):
    """This view will be used to GET the detail data"""
    # success_msg = 'Comment Added!'
    model = Post  # generic views need to know which model to act upon
    template_name = 'blog/detail.html'  # tells the view to use this template instead of it's default
    success_url = reverse_lazy('blog:index')
    form_class = CommentForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        # returning the object with the vote status included (is_voted_up/is_voted_down)
        self.object = Post.votes.annotate(queryset=Post.objects.filter(slug=self.kwargs.get('slug')),
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
        instance = super(BlogDetailGetView, self).get_object()
        if instance.draft or instance.publish_date > timezone.now():
            if not self.request.user.is_staff or not self.request.user.is_superuser:
                raise PermissionDenied
        return instance

    def get_context_data(self, **kwargs):
        context = super(BlogDetailGetView, self).get_context_data(**kwargs)
        # context['object'] provides the instance for us

        comments_qs = context['object'].comments
        context['comments'] = Comment.votes.annotate(queryset=comments_qs, user_id=self.request.user.id)  # getting the vote info
        # context['comments'] = context['object'].comments

        # context['comment_form'] = CommentForm()
        return context


class BlogDetailPostView(SingleObjectMixin, FormView):
    """This view will be used to POST the detail data

    SingleObjectMixin = Provides a mechanism for looking up an object associated with the current HTTP request.
    """
    template_name = 'blog/detail.html'  # tells the view to use this template instead of it's default
    form_class = CommentForm
    model = Post  # generic views need to know which model to act upon

    def post(self, request, *args, **kwargs):
        # comment_form = self.form_class(request.POST, request.FILES)
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        self.object = self.get_object()
        self.object = Post.votes.annotate(queryset=Post.objects.filter(slug=self.kwargs.get('slug')),
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
        return reverse('blog:detail', kwargs={'slug': self.object.slug})


class BlogDetailView(View):
    """This view will be used to ensure that one is for GET and the other for POST"""

    def get(self, request, *args, **kwargs):
        view = BlogDetailGetView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = BlogDetailPostView.as_view()
        return view(request, *args, **kwargs)


UP = 0
DOWN = 1


class PostLikeToggleAjax(APIView):

    authentication_classes = (authentication.SessionAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, slug=None, format=None):
        # slug = self.kwargs.get("slug")
        obj = get_object_or_404(Post, slug=slug)
        # url_ = obj.get_absolute_url()  # get the url of the project post
        user = self.request.user  # get the user
        updated = False
        liked = False

        if user.is_authenticated():

            # check if the user is authenticated
            # check if the user has already voted on this object
            # obj.votes.vote_by(user.id)

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


class PostDislikeToggleAjax(APIView):

    authentication_classes = (authentication.SessionAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, slug=None, format=None):
        # slug = self.kwargs.get("slug")
        obj = get_object_or_404(Post, slug=slug)
        # url_ = obj.get_absolute_url()  # get the url of the project post
        user = self.request.user  # get the user
        updated = False
        disliked = False

        if user.is_authenticated():

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
