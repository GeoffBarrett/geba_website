import json
# from django.shortcuts import render
from django.contrib import messages
from .models import Comment
from .forms import CommentForm
from django.views.generic import DetailView, DeleteView, FormView, View, RedirectView
from django.core import serializers
from ..core.models import ModelFormFailureHistory
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponseForbidden, HttpResponseRedirect, Http404, HttpResponse
from django.contrib.contenttypes.models import ContentType
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
# Create your views here.


class CommentActionMixin(object):
    # the fields that geba_auth will be able to type in the forms for CreateView
    # fields = ('published', 'title', 'body')

    @property
    def success_msg(self):
        return NotImplemented

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super(CommentActionMixin, self).form_valid(form)

    def form_invalid(self, form):
        """saves invalid form and model data for later reference."""
        form_data = json.dumps(form.cleaned_data)
        model_data = serializers.serialize("json",
                                           [form.instance])[1:-1]
        ModelFormFailureHistory.objects.create(form_data=form_data, model_data=model_data)
        return super(CommentActionMixin, self).form_invalid(form)


class CommentThreadGetView(DetailView):
    """This view will be used to GET the detail data"""
    # success_msg = 'Comment Added!'
    model = Comment  # generic views need to know which model to act upon
    template_name = 'comments/detail.html'  # tells the view to use this template instead of it's default
    form_class = CommentForm

    def get(self, request, *args, **kwargs):
        # self.object = get_object_or_404(Comment, pk=kwargs['pk'])
        try:
            self.object = Comment.objects.get(pk=kwargs['pk'])
        except:
            response = HttpResponse("You do not have permission to do this.")
            response.status_code = 403
            return response

        if not self.object.is_parent:
            # if the object isn't a parent, get the parent object
            self.object = self.object.parent

        # the original get defines self.object, this is required otherwise you get an error stating that there is no
        # attribute 'object' in this DetailView
        context = self.get_context_data(object=self.object)
        context['comment'] = self.object

        instance = self.object

        context = self.get_context_data(object=self.object)

        initial_data = {
            'content_type': instance.content_type,
            'object_id': instance.id,
        }
        comment_form = self.form_class(request.POST or None, initial=initial_data)

        context['comment_form'] = comment_form
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(CommentThreadGetView, self).get_context_data(**kwargs)

        # context['object'] provides the instance for us
        context['comments'] = context['object']
        # context['comment_form'] = CommentForm()
        return context


class CommentThreadPostView(SingleObjectMixin, FormView):
    """This view will be used to POST the detail data

    SingleObjectMixin = Provides a mechanism for looking up an object associated with the current HTTP request.
    i.e. using get_object()
    """
    template_name = 'comments/detail.html'  # tells the view to use this template instead of it's default
    form_class = CommentForm
    model = Comment  # generic views need to know which model to act upon

    def post(self, request, *args, **kwargs):
        # comment_form = self.form_class(request.POST, request.FILES)
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        # self.object = self.get_object()
        try:
            self.object = Comment.objects.get(pk=kwargs['pk'])
        except:
            response = HttpResponse("You do not have permission to do this.")
            response.status_code = 403
            return response

        if not self.object.is_parent:
            # if the object isn't a parent, get the parent object
            self.object = self.object.parent

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
        # return HttpResponseRedirect(self.new_comment.content_object.get_absolute_url())
        return reverse('comments:thread', kwargs={'pk': self.object.pk})


class CommentThreadView(View):
    """This view will be used to ensure that one is for GET and the other for POST"""

    def get(self, request, *args, **kwargs):
        view = CommentThreadGetView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentThreadPostView.as_view()
        return view(request, *args, **kwargs)


class CommentDeleteView(CommentActionMixin, DeleteView):

    model = Comment
    success_msg = 'Comment Deleted!'
    success_url = reverse_lazy('blog:index')

    # make it so you have to be a super-geba_auth or staff to delete
    def dispatch(self, request, *args, **kwargs):
        # request = check_comment_rights(request)
        object = Comment.objects.get(pk=kwargs['pk'])

        if object.author != request.user:
            # messages.success(request, "You do not have permission to view this!")
            response = HttpResponse("You do not have permission to do this.")
            response.status_code = 403
            return response

        return super(CommentDeleteView, self).dispatch(request, *args, **kwargs)

    def post(self, *args, **kwargs):
        try:
            object = Comment.objects.get(pk=kwargs['pk'])

        except:
            raise Http404

        parent_obj_url = object.content_object.get_absolute_url()
        object.delete()
        messages.success(self.request, "Comment has been deleted.")
        return HttpResponseRedirect(parent_obj_url)


UP = 0
DOWN = 1


class CommentLikeToggle(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs.get("pk")
        obj = Comment.objects.get(pk=pk)
        # obj = get_object_or_404(Comment, pk=pk)
        url_ = obj.get_absolute_url()  # get the url of the project post
        user = self.request.user  # get the geba_auth

        if user.is_authenticated:

            if obj.votes.exists(user.id, action=UP):
                obj.votes.delete(user.id)
            else:
                # upvote the object
                obj.votes.up(user.id)

        return url_


class CommentLikeToggleAjax(APIView):

    authentication_classes = (authentication.SessionAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, pk=None, format=None):
        pk = self.kwargs.get("pk")

        # the get_object_or_404 won't work on the reply comments
        # obj = get_object_or_404(Comment, pk=pk)
        obj = Comment.objects.get(pk=pk)

        # url_ = obj.get_absolute_url()  # get the url of the project post
        user = self.request.user  # get the geba_auth
        updated = False
        liked = False

        if user.is_authenticated:

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


class CommentDislikeToggleAjax(APIView):

    authentication_classes = (authentication.SessionAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, pk=None, format=None):
        # slug = self.kwargs.get("slug")
        pk = self.kwargs.get("pk")

        # the get_object_or_404 won't work on the reply comments
        # obj = get_object_or_404(Comment, pk=pk)
        obj = Comment.objects.get(pk=pk)

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