
from django.shortcuts import render
from django.http import HttpResponse
#from django.template import RequestContext, loader

from polls.models import Question

# Create your views here.

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
#    template = loader.get_template('polls/index.html')
#    context = RequestContext(request, {
#        'latest_question_list' : latest_question_list,
#        })
    return render(request, 'polls/index.html', context)
#    return HttpResponse(template.render(context))

### tutorial 2
#def detail(request, question_id):
#    return HttpResponse("You're looking at question %s" % question_id)

def results(request, question_id):
    response = "You are looking at the results of question %s."
    return HttpResponse(response % question_id)

#def vote(request, question_id):
#    return HttpResponse("You're voting on question %s." % question_id)


### Raising a 404 error
#from django.http import Http404
from django.shortcuts import get_object_or_404, render

from polls.models import Question

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

#    try:
#        question = Question.objects.get(pk=question_id)
#    except Question.DoesNotExist:
#        raise Http404("Question does not exist")
#    return render(request, 'polls/detail.html', {'question' = question})

    return render(request, 'polls/detail.html', {'question':question})

### implement vote()
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from polls.models import Choice, Question

def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        #Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': "You didn't select a choice.",
            })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        #Always return an HttpResponseRedirect after successfully dealing with POST data.
        #This prevents data from being posted twice if a user hits the Back Button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))

### result view
from django.shortcuts import get_object_or_404, render

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

### tutorial 4 apply generic view
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
### tutorial 5 apply checking of "future" posts
from django.utils import timezone

from polls.models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
            ).order_by('pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

# def vote(request, question_id):
# same as before
