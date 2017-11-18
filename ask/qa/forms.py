from django.forms import ModelForm, PasswordInput, HiddenInput
from .models import Question
from .models import Answer
from django.contrib.auth.models import User

class AskForm(ModelForm):
    class Meta:
        fields = ['title', 'text', 'author']
        model = Question
        widgets = {
            'author': HiddenInput(), #make the input in the field hidden
        }

class AnswerForm(ModelForm):
    class Meta:
        fields = ['text', 'question', 'author']
        #exclude = ['author'] #to hide this filed in a HTML-form
        model = Answer
        widgets = {
            'author': HiddenInput(), #make the input in the field hidden
            'question': HiddenInput(),
        }

class SignUp(ModelForm):
    class Meta:
    	fields = ['username', 'email', 'password']
    	model = User
    	widgets = {
            'password': PasswordInput(), #make the input in the field hidden
        }

class Login(ModelForm):
    class Meta:
    	fields = ['username', 'password']
    	model = User
    	widgets = {
            'password': PasswordInput(), #make the input in the field hidden
        }
