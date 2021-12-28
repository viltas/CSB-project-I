from django.http.response import Http404
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import Lunch, Choice
from django.views import generic
from django.utils import timezone

class IndexView(generic.ListView):
    template_name = 'lunch_app/index.html'
    context_object_name = 'next_lunch'

    def get_queryset(self):
        return Lunch.objects.filter(date__day=timezone.now().day)


class DetailView(generic.DetailView):
    model = Lunch
    template_name = 'lunch_app/detail.html'


class ResultsView(generic.DetailView):
    model = Lunch
    template_name = 'lunch_app/results.html'

def vote(request, lunch_id):
    lunch = get_object_or_404(Lunch, pk=lunch_id)
    try:
        selected_choice = lunch.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the lunch voting form.
        return render(request, 'lunch_app/detail.html', {
            'lunch': lunch,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('lunch_app:results', args=(lunch.id,)))  
  