from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from random import randint #7.2
#from datetime import datetime, timedelta

class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-added_at')
    def popular(self):
        return self.order_by('-rating')

class Question(models.Model):
    objects = QuestionManager()
    title = models.CharField(max_length=255)
    text = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(User, related_name="question_author", null=True) #6 Set 'null=True' due to have an ability to have the author field with Null-value (can contain Null) in !database!, P.S. default=0 also works
    likes = models.ManyToManyField(User, related_name="question_like", blank=True) # 'blank=True' means the a field can be unfilled, it's not necessary to fill this field, !for user data checking! in an input form

    class Meta:
        ordering = ('-added_at') # Default ordering in Django-admin interface
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return self.title

    def get_absolute_url(self): #reverse-routing to call in a template index.html
        return reverse('details', kwargs={'id': self.id}) #4. 'details' means the name of a url-route (see urls.py) 'id' is also from 'details'

class Answer(models.Model):
    text = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question)
    author = models.ForeignKey(User, null=True) #6

    class Meta:
        ordering = ('added_at',)

    def __str__(self):
        return 'Answer by {}'.format(self.author)

    def get_absolute_url(self): #6.2!
        return reverse('answer_details', kwargs={'id': self.id}) #6.2!

class Session(models.Model): #7.3
    key = models.CharField(max_length=255)
    user = models.ForeignKey(User, null=True)
    start = models.DateTimeField(auto_now_add=True)
    finish = models.DateTimeField(null=True)
    
    def __str__(self):
        return self.key

def do_login(login, password): #7.4
    try:
        user = User.objects.get(username = login)
    except User.DoesNotExist:
        return None
    hashed_pass = password #do something - encoding

    if user.password != hashed_pass:
        return None

    session = Session() #
    session.key = str(randint(10,99)) + str(randint(10,99)) + str(randint(10,99)) #
    session.user = user
    #session.expires = datetime.now() + timedelta(days = 1)
    session.save()
    return session.key
