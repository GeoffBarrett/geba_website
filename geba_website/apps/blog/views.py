from django.utils import timezone
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView, FormView, View
from django.core.exceptions import PermissionDenied
from .utils import check_blog_rights
from django.shortcuts import render, render_to_response, get_object_or_404
from .models import Post
from .forms import BlogPostForm
from ..comments.forms import CommentForm
from ..comments.models import Comment
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .mixins import BlogActionMixin
from ..geba_analytics.mixins import ObjectViewMixin
from ..geba_auth.forms import UserCreationForm


class BlogIndexView(ListView):
    template_name = 'blog/index.html'  # tells the view to use this template instead of it's default
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
            query_set_list = Post.objects.all().order_by("-publish_date")[:]
        else:
            query_set_list = Post.objects.active()[:]

        query = self.request.GET.get("query")
        if query:
            # this is for searching using the search bar
            query_set_list = Post.objects.search(qs=query_set_list, query=query)

        author_query = self.request.GET.get("author")
        if author_query:
            # filter query list by author
            query_set_list = Post.objects.search_author(qs=query_set_list, query=author_query)

        tag_query = self.request.GET.get("tag")
        if tag_query:
            # filter query list by keyword/tag
            query_set_list = Post.objects.search_tags(qs=query_set_list, query=tag_query)

        # now we must pass this query_set into the annotate (or voted_by) method to get the is_voted_up or is_voted_down
        query_set_list = Post.votes.annotate(queryset=query_set_list, user_id=self.request.user.id)

        return query_set_list


class BlogCreateView(BlogActionMixin, CreateView):
    model = Post
    success_msg = 'Blog Created!'
    form_class = BlogPostForm
    template_name = 'blog/post_form.html'
    # Don't need to specify template name due to the html file being named ModelName_form.html

    # make it so you have to be staff or super-geba_auth to create blog
    def dispatch(self, request, *args, **kwargs):
        request = check_blog_rights(request)
        return super(BlogCreateView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        """when the geba_auth executes a get request, display blank registration form"""
        form = self.form_class(request.GET or None, request.FILES or None)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        """performs a post request"""
        form = self.form_class(request.POST or None, request.FILES or None)

        if form.is_valid():
            instance = form.save(commit=False)  # creates object from the form, doesn't save it to the database just yet

            if request.user.get_username() == 'admin':
                # instance.author = User.objects.get(username='Geoff')
                instance.author = request.user
            else:
                instance.author = request.user

            instance.save()
            instance.votes.up(request.user.id)

            return HttpResponseRedirect(reverse_lazy('blog:detail', kwargs={'slug': instance.slug}))
        else:
            return render_to_response(self.template_name, {'form': form})


class BlogUpdateView(BlogActionMixin, UpdateView):
    model = Post
    success_msg = 'Blog Updated!'
    form_class = BlogPostForm
    template_name = 'blog/post_form_update.html'

    def get(self, request, slug):
        """when the geba_auth executes a get request, display blank registration form"""
        self.object = self.get_object()
        self.sucess_url = reverse_lazy('blog:detail', kwargs={'slug': self.object.slug})
        form = self.form_class(request.GET or None, request.FILES or None, instance=self.object)
        return render(request, self.template_name, {'form': form})

    # make it so you have to be staff or super-geba_auth to update blog
    def dispatch(self, request, *args, **kwargs):
        request = check_blog_rights(request)
        return super(BlogUpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        return super(BlogUpdateView, self).form_valid(form)


class BlogDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('blog:index')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return HttpResponseRedirect(reverse('blog:detail', args=self.object.slug))

    # make it so you have to be a super-geba_auth or staff to delete
    def dispatch(self, request, *args, **kwargs):
        request = check_blog_rights(request)
        return super(BlogDeleteView, self).dispatch(request, *args, **kwargs)


class BlogDetailGetView(ObjectViewMixin, DetailView):
    """This view will be used to GET the detail data"""
    model = Post  # generic views need to know which model to act upon
    template_name = 'blog/detail.html'  # tells the view to use this template instead of it's default
    success_url = reverse_lazy('blog:index')
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
        instance = super(BlogDetailGetView, self).get_object()
        if instance.draft or instance.publish_date > timezone.now():
            if not self.request.user.is_staff or not self.request.user.is_superuser:
                raise PermissionDenied

        # don't use annotate, use vote_by in this case, annotate only works when __iter__ is called
        instance = Post.votes.vote_by(self.request.user.id, ids=[instance.id])[0]

        return instance

    def get_context_data(self, **kwargs):
        context = super(BlogDetailGetView, self).get_context_data(**kwargs)

        comments_qs = context['object'].comments
        # getting the vote info
        context['comments'] = Comment.votes.annotate(queryset=comments_qs, user_id=self.request.user.id)

        return context


class BlogDetailPostView(SingleObjectMixin, FormView):
    """
    This view will be used to POST the detail data

    SingleObjectMixin = Provides a mechanism for looking up an object associated with the current HTTP request.
    """
    template_name = 'blog/detail.html'  # tells the view to use this template instead of it's default
    form_class = CommentForm
    model = Post  # generic views need to know which model to act upon

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        self.object = self.get_object()
        self.object = Post.votes.vote_by(self.request.user.id, ids=[self.object.id])[0]

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
        obj = get_object_or_404(Post, slug=slug)
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


class PostDislikeToggleAjax(APIView):

    authentication_classes = (authentication.SessionAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, slug=None, format=None):
        obj = get_object_or_404(Post, slug=slug)
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


class PublishPostAjax(APIView):

    authentication_classes = (authentication.SessionAuthentication, )
    permission_classes = (permissions.IsAdminUser, )

    def get(self, request, slug=None, format=None):
        obj = get_object_or_404(Post, slug=slug)
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
                published = True

            updated = True

        data = {'updated': updated,
                'published': published}

        return Response(data)


class MakeDraftPostAjax(APIView):

    authentication_classes = (authentication.SessionAuthentication, )
    permission_classes = (permissions.IsAdminUser, )

    def get(self, request, slug=None, format=None):
        obj = get_object_or_404(Post, slug=slug)
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
