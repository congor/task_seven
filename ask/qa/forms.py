from django.forms import ModelForm
from .models import Question
from .models import Answer

class AskForm(ModelForm):
    class Meta:
        fields = ['title', 'text']
        model = Question

class AnswerForm(ModelForm):
    class Meta:
        fields = ['text', 'question']
        #exclude = ['author'] #to hide this filed in a HTML-form
        model = Answer