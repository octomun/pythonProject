from django.contrib import admin
from .models import Question


class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']
    
    #fields = ['author','subject','modify_date','voter']
    fieldsets = [
        ('Question Statement', {'fields':['author','subject','content','modify_date','voter']}),
        ('Create_Date Setting', {'fields' : ['create_date'],'classes':['collapse']}),
        
    ]


admin.site.register(Question, QuestionAdmin)