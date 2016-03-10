from django.shortcuts import render
from django.http import  HttpResponse
from django.template import  RequestContext,loader
from .models import Question
# Create your views here.

def index(request):
    last_question_list=Question.objects.order_by("-pub_date")[:5]
    template=loader.get_template("mysite/index.html")
    context=RequestContext(request,{'last_question_list':last_question_list})
    return HttpResponse(template.render(context))


def detail(request,question_id):
    return HttpResponse("you're looking at question:%s" % question_id)

def results(request,question_id):
    response="your'are looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request,question_id):
    return HttpResponse("Your'are voting on question %s." % question_id)