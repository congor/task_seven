from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator #1
from .models import Question #2
from django.shortcuts import get_object_or_404 #3

def paginate(request, qs): #1
    try:
        page = int(request.GET.get('page', 1)) #Mining the requred page number
    except ValueError:
    	raise Http404()
    paginator = Paginator(qs, 10) #Create the paginator-object
    try:
        page = paginator.page(page) #Take the object consists of notes from DB for the requred page number
    except EmptyPage:
        page = paginator.page(paginator.num_pages) #Take the object consists of notes from DB for the last page
    return page, paginator

def test(request, *args, **kwards):
    return HttpResponse('OK')

def main(request): #2
    page, paginator = paginate(request, Question.objects.new())
    return render(request, 'index.html', {
        'paginator': paginator,
        'page': page,         
    })
 
def question_details(request, id=None): #3 Conntroller to show details of a question
    instance = get_object_or_404(Question, id=id)
    return render(request, "question.html", {
        "title": instance.title,
        "instance": instance,
    })
    
    
 # Create your views here.