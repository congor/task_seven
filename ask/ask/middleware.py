from qa.models import Session #7.3
#to del - from qa.models import SessionsForUnloggedUsers #7.7
#to del - from qa.models import UnloggedUsers #7.7
from random import randint #7.7
from django.contrib.auth.models import User  #7.7

def generate_unlogged(): # a function for creation an unlogged unregistrated user and his session
    
    try:
        User.objects.filter(username__contains='Аноним ')[0] # Try whether just one record exists
    except: # If it doesn't - create the first one
        first_unlogged_username = 'Аноним ' + str(1)        
        new_unlogged_user = User()
        new_unlogged_user.username = first_unlogged_username
        new_unlogged_user.save()
    else: #If it does - create the next one with increment + 1
        last_unlogged_user = User.objects.filter(username__contains='Аноним ').order_by('-id')[0]
        current_unlogged_username = 'Аноним ' + str(int(last_unlogged_user.username[last_unlogged_user.username.find(' ')+1:]) + 1)
        new_unlogged_user = User()
        new_unlogged_user.username = current_unlogged_username
        new_unlogged_user.save()

    session_trial = Session()
    session_trial.key = 'trial' + str(randint(10,99)) + str(randint(10,99)) + str(randint(10,99))
    session_trial.user = new_unlogged_user
    #session_trial.expires = datetime.now() + timedelta(days = 1)
    session_trial.save()

    return session_trial


class CheckSessionMiddleware(object): #7.3 order of design to see /home/firstuser/task7/myenv5/lib/python3.5/site-packages/django/contrib/auth/middlware.py - class AuthenticationMiddleware(object)
    def process_request(self, request): 

        try: # Try whether a registrated user is logged
            sessid = request.COOKIES.get('sessid') # take a session id
            session = Session.objects.get(key = sessid) # take a session-object from DB

        except: 
            try: # Try whether a unregistrated user is logged as Аноним
                sessid_trial = request.COOKIES.get('sessidtrial') # take a session id for unlogged users
                session = Session.objects.get(key = sessid_trial) # take a session-object from DB for unlogged users          
            except:  # For an unregistrated user who is unlogged and doesn't have a cookie with the 'sessidtrial'-key 'cause he is here at first time 
                session_trial = generate_unlogged()
                request.session = session_trial.key # Because an unlogged unregistrated has just gotten the trial login Аноним and his session but haven't received a cookie with the 'sessidtrial'-key,
                request.user = session_trial.user   # we should give this information via certain fileds in a request-object for rendering html-page at once we do it at first user's request
                request.user_firstentering = True # set for an unlogged unregistrated user to know about for setting a cookie with the 'sessidtrial'-key
                request.user_registrated = False # set for a unlogged unregistrated user
            else: # For a logged as Аноним unregistrated user who has been logged automatically through cookie with the 'sessidtrial'-key
                request.session = session  # set a session-object as a field of request
                request.user = session.user # set a user from a session-object as a field of request
                request.user_registrated = False # set for a logged as Аноним unregistrated user

        else: # For a logged registrated user
            request.session = session  # set a session-object as a field of request
            request.user = session.user # set a user from a session-object as a field of request
            request.user_registrated = True # set for a logged registrated user


    def process_response(self, request, response):

        try:
            request.user_firstentering
        except:
            return response # There will be an user without any logging if can't create a trial name for an unlogged unregistrated user and his sesion and this way to log him
        else:
            if request.user_firstentering == True:
                session_trial = request.session           
                response.set_cookie('sessidtrial', session_trial)
                return response
            else:
                return response #response is an object of the class HttpResponse
