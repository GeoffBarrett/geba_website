from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
# Create your views here.

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/detail.html'  # tells the view to use this template instead of it's default
    context_object_name = 'latest_question_list'  # tell the view to use this context_object_name instead of the default

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class DetailView(generic.DetailView):
    model = Question  # generic views need to know which model to act upon
    template_name = 'polls/detail.html'  # tells the view to use this template instead of it's default


class ResultsView(generic.DetailView):
    model = Question  # generic views need to know which model to act upon
    template_name = 'polls/results.html'  # tells the view to use this template instead of it's default


def vote(request, question_id):
    # requests are like dictionaries so request.POST['choice'] provides us with the vote as a string if selected
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))