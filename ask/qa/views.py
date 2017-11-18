from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator #1
from .models import Question, Answer #2
from .models import do_login #7.2
from .models import Session #7.3
from django.shortcuts import get_object_or_404 #3
from .forms import AskForm, AnswerForm #6.0
from .forms import SignUp, Login #7.1, 7.2
from django.template.context import RequestContext #?6.1
from django.contrib.auth.models import User
from datetime import datetime

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
        'request': request,        
        'title': 'Свежие вопросы',
        'paginator': paginator,
        'page': page,
    })

def question_details(request, id=None): #3 Controller to show details of a question    

    # If take a POST-request - check and save the answer

    if request.method == 'POST': #6.3
        form = AnswerForm(request.POST)
        if form.is_valid():
            form.save()
            url_redirect = Question.objects.get(id=form['question'].data).get_absolute_url() #!!! question  - the name of a form's field, .data - a field with contain of this form's field
            return HttpResponseRedirect(url_redirect) # Open the page of details of the certain qetails
    
    else: # If take a GET-request and render a full page constists of 3 parts:           
        
        current_user = request.user # To extract an user name from a request object (set this request's field in middleware.py in /ask/ask)
        
        #Part 1. Render a question's definition
        question = get_object_or_404(Question, id=id)    
        url = question.get_absolute_url() #6.3 create url for action in POST-form with a methon in Question data model
        
        #Part 2. Render an Answer form
        form = AnswerForm(initial={'question': id,'author': current_user}) #6.5!!! 'initial' automatically sets a proper quiestion in an answer form at once with opening page #

        #Part 3. Render a list of answers have been saved in a DB
        answers = Answer.objects.filter(question=id).order_by('added_at').reverse() #6.3 While did it beggining from newest answers
        #answer = question.answer_set.all() #6.3 alternative, also works properly as 'answer = Answer.objects.filter(question=id)'
    
    return render(request, "question.html", {
        "title": question.title,
        "question": question,
        'form': form, #6.3
        'answers': answers, #6.3
        'url': url,
    })

def ask_form(request): #6.1
    
    # If take a POST-request - check and save the question

    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            question = form.save()
            url = question.get_absolute_url()
            return HttpResponseRedirect(url) # Redirect and open the page of details of the certain details
    
    else: # If take a GET-request and render a ask form in a page:
        current_user = request.user
        form = AskForm(initial={'author': current_user}) # Create a form-object
        
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
        current_user = request.user
        form = AnswerForm(initial={'author': current_user})
    return render(request, 'answer_form.html', { # or return render(request, 'ask_form.html', RequestContext(request, {...})) # What is RequestContext?
        'title': 'Ответ',
        'form': form,
    })

def t(request):
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
        'form': for1m,
    })

# def ans(request): #?6.4 # !Doesn't work if used as a function in question_detail (takes a "request" and return "form")
#     if request.method == 'POST':        
#         form = AnswerForm(request.POST)
#         if form.is_valid():
#             answer = form.save()            
#             url = Question.objects.get(id=form['question'].data).get_absolute_url() #!!! question  - the name of a form's field, .data - a field with contain of this form's field
#             return HttpResponseRedirect(url) # Open the page of details of the certain qetails
#     else:
#         form = AnswerForm()
#     return form

def answer_details(request, id=None): #6.2 a controller to show details of a answers
    answer = get_object_or_404(Answer, id=id)
    form = AnswerForm(instance=answer) # To edit an answer
    return render(request, "answer.html", {
        "title": answer.question,
        "instance": answer,
        "form": form,
    })

def signup(request): #7.1
    if request.method == 'POST':
        url = request.POST.get('continue', '/')
        form = SignUp(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(url)
    else:
        form = SignUp()
    return render(request, 'signup.html', {
        "title": 'Регистрация',
        "form": form
        })

def login(request): #7.2
    if request.method == 'POST':
        error = []
        if request.POST.get('username') == '':
            error.append('Login не был введен')
        else:
            login = request.POST.get('username')
        if request.POST.get('password') == '':
            error.append('Password не был введен')
        else:
            password = request.POST.get('password')

        if len(error) == 0:

            url = request.POST.get('continue', '/')

            sessid = do_login(login, password)

            if sessid:
                response = HttpResponseRedirect(url)
                response.set_cookie('sessid', sessid)
                return response
            else:
                error.append('Login or password is wrong')
                form = Login()
        else:            
            form = Login()
    else:
        error = None
        form = Login()        

    return render(request, 'login.html', {
        'title': 'Войти',
        'error': error,
        'form': form,
    })

def logout(request):
    try:
        sessid = request.COOKIES.get('sessid')
    except:
        return HttpResponse("Сессия на может быть закончена, так как система на может распознать пользователя")

    Session.objects.filter(key=sessid).update(finish=datetime.now()) #update works only with .filter, doedn't work with .get
    
    url = request.META.get('HTTP_REFERER')#url = request.GET.get('continue', '/') 
    response = HttpResponseRedirect(url)
    response.delete_cookie('sessid')
    return response

 # Create your views here.