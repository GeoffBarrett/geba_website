from django.contrib import admin

from .models import Question, Choice

# Register your models here.


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]  # addds the choices to the admin
    list_display = ('question_text', 'pub_date', 'was_published_recently')  # adds these columns
    list_filter = ['pub_date']  # adds a filter section
    search_fields = ['question_text']  # adds search capability


admin.site.register(Question, QuestionAdmin)


