from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView, FormView, View
# Create your views here.
from .models import ForumPost
from django.db.models import Q


class ForumIndexView(ListView):
    template_name = 'forum/index.html'  # tells the view to use this template instead of it's default
    context_object_name = 'object_list'  # tell the view to use this context_object_name instead of the default

    def get_queryset(self, *args, **kwargs):
        """
        Excludes any questions that aren't published yet.
        """
        # current_active_posts = Post.objects.filter(published__lte=timezone.now()).order_by("-published")[:]
        # return Post.objects.filter(draft=False).filter(publish_date=timezone.now()).order_by("-publish_date")[:]
        if self.request.user.is_staff or self.request.user.is_superuser:
            query_set_list = ForumPost.objects.all().order_by("-publish_date")[:]
        else:
            query_set_list = ForumPost.objects.active()[:]

        # now we must pass this query_set into the annotate (or voted_by) method to get the is_voted_up or is_voted_down

        query = self.request.GET.get("q")

        if query:
            # this is for searching using the search bar
            query_set_list = query_set_list.filter(
                Q(title__icontains=query)|
                Q(author__username__icontains=query)
                #Q(body__text__icontains=query)
            ).distinct()

        query_set_list = ForumPost.votes.annotate(queryset=query_set_list, user_id=self.request.user.id)

        return query_set_list
