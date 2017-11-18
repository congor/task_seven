from qa.models import Session #7.3
from qa.models import SessionsForUnloggedUsers #7.7
from qa.models import UnloggedUsers #7.7
from random import randint #7.7

def generate_unlogged(): # a function for creation an unlogged user and his session
    
    new_unlogged_user = UnloggedUsers()
    new_unlogged_user.save()

    session_trial = SessionsForUnloggedUsers()
    session_trial.key = 'trial' + str(randint(10,99)) + str(randint(10,99)) + str(randint(10,99))
    session_trial.user = new_unlogged_user
    #session_trial.expires = datetime.now() + timedelta(days = 1)
    session_trial.save()

    return session_trial


class CheckSessionMiddleware(object): #7.3 order of design to see /home/firstuser/task7/myenv5/lib/python3.5/site-packages/django/contrib/auth/middlware.py - class AuthenticationMiddleware(object)
    def process_request(self, request): 

        try: # For logged users
            sessid = request.COOKIES.get('sessid') # take a session id
            session = Session.objects.get(key = sessid) # take a session-object from DB            

        except: # For unlogged users
            try:
                sessid_trial = request.COOKIES.get('sessidtrial') # take a session id
                session = SessionsForUnloggedUsers.objects.get(key = sessid_trial) # take a session-object from DB                
            except:  #if a user is here at first time
                session_trial = generate_unlogged()

                request.session = session_trial.key
                request.user = session_trial.user
            else:
                request.session = session  # set a session-object as a field of request
                request.user = session.user # set a user from a session-object as a field of request

        else:
            request.session = session  # set a session-object as a field of request
            request.user = session.user # set a user from a session-object as a field of request                

    def process_response(self, request, response):

        if 'trial' in str(request.session):
            session_trial = request.session           
            response.set_cookie('sessidtrial', session_trial)
            return response
        else:            
            return response #response is an object of the class HttpResponse
