from django.contrib import admin
from .models import Question

# Register your models here.
class QuestionModelAdmin(admin.ModelAdmin):
    list_display = ["title", "rating", "added_at"]
    list_display_links = ["added_at"]
    list_filter = ["added_at"]
    
    class Meta:
        model = Question

admin.site.register(Question, QuestionModelAdmin)