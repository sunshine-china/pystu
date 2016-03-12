from django.shortcuts import render,get_object_or_404
from django.http import  HttpResponse,Http404,HttpResponseRedirect
from django.template import  RequestContext,loader
from .models import Question,Choice
from django.core.urlresolvers import reverse
from django.views import  generic
# Create your views here.

def index(request):
    last_question_list=Question.objects.order_by("-pub_date")[:5]
    template=loader.get_template("mysite/index.html")
    context=RequestContext(request,{'last_question_list':last_question_list})
    return HttpResponse(template.render(context))

class IndexView(generic.ListView):
    template_name = 'mysite/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        :return: the last five published question.
        """
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'mysite/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'mysite/results.html'

def detail(request,question_id):
    try:
        question=Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise  Http404("question does not found")
    return render(request,'mysite/detail.html',{'question':question})

def results(request,question_id):
    response="your'are looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request,question_id):
    p=get_object_or_404(Question,pk=question_id)
    try:
        selected_choice=p.choice_set.get(pk=request.POST['choice'])
    except(KeyError ,Choice.DoesNotExist):
        return render(request,'mysite/detail.html',{'question':p,'error_message':'your did not select a choice'})
    else:
        selected_choice.votes=1
        selected_choice.save()
        return HttpResponseRedirect(reverse('mysite:results',args=(p.id,)))