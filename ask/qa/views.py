from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator #1
from .models import Question, Answer #2
from django.shortcuts import get_object_or_404 #3
from .forms import AskForm, AnswerForm #6.0
from django.template.context import RequestContext #?6.1
from django.contrib.auth.models import User

def paginate(request, qs): #1
    try:
        page = int(request.GET.get('page', 1)) #Mining the requred page number
    except ValueError:
    	raise Http404()
    paginator = Paginator(qs, 10) #Create the paginator-object
    try:
        page = paginator.page(page) #Take the object consists of notes from DB for the requred page's number
    except EmptyPage:
        page = paginator.page(paginator.num_pages) #Take the object consists of notes from DB for the last page
    return page, paginator

def test(request, *args, **kwards):
    return HttpResponse('OK')

def main(request): #2
    page, paginator = paginate(request, Question.objects.new())
    return render(request, 'index.html', {
        'title': 'Свежие вопросы',
        'paginator': paginator,
        'page': page,         
    })
 
def question_details(request, id=None): #3 Controller to show details of a question    
    #form = ans(request) #?6.4 doesn't work
    if request.method == 'POST': #6.3        
        form = AnswerForm(request.POST)
        if form.is_valid():
            form.save()
            url_redirect = Question.objects.get(id=form['question'].data).get_absolute_url() #!!! question  - the name of a form's field, .data - a field with contain of this form's field
            return HttpResponseRedirect(url_redirect) # Open the page of details of the certain qetails
    else:
        form = AnswerForm(initial={'question': id}) #6.5!!! 'initial' automatically to set proper quiestion in answer form at once with opening page
    instance = get_object_or_404(Question, id=id)
    answers = Answer.objects.filter(question=id).order_by('added_at').reverse() #6.3 While did it beggining from newest answers
    #answer = instance.answer_set.all() #6.3 alternative, also works properly as answer = Answer.objects.filter(question=id)
    url = instance.get_absolute_url() #6.3 url for action in form
    return render(request, "question.html", {        
        "title": instance.title,
        "instance": instance,
        'form': form, #6.3
        'answers': answers, #6.3
        'url': url,
        #'test': test,
    })

def ask_form(request): #6.1
    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            question = form.save()
            url = question.get_absolute_url()
            return HttpResponseRedirect(url) # Redirect and open the page of details of the certain details
    else:
        form = AskForm()
    return render(request, 'ask_form.html', { # or return render(request, 'ask_form.html', RequestContext(request, {...})) # What is RequestContext?
        'title': 'Задайте новый вопрос',
        'form': form,
    })

def answer_form(request): #6.2
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save()            
            url = Question.objects.get(id=form['question'].data).get_absolute_url() #!!! question  - the name of a form's field, .data - a field with contain (id) of this form's field
            return HttpResponseRedirect(url) # Open the page of details of the certain details
    else:
        form = AnswerForm()
    return render(request, 'answer_form.html', { # or return render(request, 'ask_form.html', RequestContext(request, {...})) # What is RequestContext?
        'title': 'Ответ',
        'form': form,
    })

def ans(request): #?6.4 # !Doesn't work if used as a function in question_detail (takes a "request" and return "form")
    if request.method == 'POST':        
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save()            
            url = Question.objects.get(id=form['question'].data).get_absolute_url() #!!! question  - the name of a form's field, .data - a field with contain of this form's field
            return HttpResponseRedirect(url) # Open the page of details of the certain qetails
    else:
        form = AnswerForm()
    return form

def answer_details(request, id=None): #6.2 a controller to show details of a answers
    answer = get_object_or_404(Answer, id=id)
    form = AnswerForm(instance=answer) # To edit an answer
    return render(request, "answer.html", {
        "title": answer.question,
        "instance": answer,
        "form": form,
    })

 # Create your views here.