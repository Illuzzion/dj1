from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, get_object_or_404
from django.template import RequestContext
from django.template import loader
# from django.urls import reverse
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views import generic

from .models import Questions, Choice


# old
# def index(request):
#     latest_question_list = Questions.objects.order_by('-pub_date')[:5]

# http://djbook.ru/rel1.9/intro/tutorial03.html#a-shortcut-render
# return render(request, 'polls/index.html',
#               {
#                   'latest_question_list': latest_question_list,
#               })

class IndexView(generic.ListView):
    model = Questions
    context_object_name = 'latest_question_list'

    template_name = 'polls/index.html'

    def get_queryset(self):
        # return Questions.objects.order_by('-pub_date')[:5]
        return Questions.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


# old
# def detail(request, question_id):
#     question = get_object_or_404(Questions, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})


class DetailView(generic.DetailView):
    model = Questions
    context_object_name = 'question'

    template_name = 'polls/detail.html'


# old
# def results(request, question_id):
#     res = get_object_or_404(Questions, pk=question_id)

# return render(request, 'polls/results.html', {'question': res})


class ResultsView(generic.DetailView):
    model = Questions
    context_object_name = 'question'

    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Questions, pk=question_id)
    try:
        choise = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html',
                      {
                          'question': question,
                          'error_message': 'choice not selected'
                      })
    else:
        choise.votes += 1
        choise.save()

        return HttpResponseRedirect(
            # http://djbook.ru/rel1.9/ref/urlresolvers.html#reverse
            reverse('polls:results', args=(question.id,))
        )
