from django.contrib import admin
from .models import *
# Register your models here.

class what_you_learn_TabularInline(admin.TabularInline):
    model = What_you_learn

class Requirements_TabularInline(admin.TabularInline):
    model = Requirements

class Video_TabularInline(admin.TabularInline):
    model = Video

class Lesson_TabularInline(admin.TabularInline):
    model = Lesson

class create_question(admin.TabularInline):
    model = Question

class create_answer(admin.TabularInline):
    model = Answer

class course_admin(admin.ModelAdmin):
    inlines = (what_you_learn_TabularInline, Requirements_TabularInline, Lesson_TabularInline, Video_TabularInline,)
    list_display = ('title', 'user', 'status')
    ordering = ('status', )
    search_fields = ('title',)

class lesson_admin(admin.ModelAdmin):
    list_display = ('name', 'course', 'status')
    ordering = ('status', )
    search_fields = ('name', 'course')

class quiz_admin(admin.ModelAdmin):
    inlines = (create_question,)
    list_display = ('topic', 'lesson', 'course', 'status')
    ordering = ('status',)
    search_fields = ('topic', 'course')

class question_admin(admin.ModelAdmin):
    inlines = (create_answer,)
    list_display = ('text', 'quizzes', 'point', 'status')
    ordering = ('quizzes',)
    search_fields = ('text', 'quizzes',)

class video_admin(admin.ModelAdmin):
    list_display = ('title', 'course', 'lessson', 'status')
    ordering = ('status',)
    search_fields = ('title', 'course',)

admin.site.register(Categories)
admin.site.register(Author)
admin.site.register(Course, course_admin)
admin.site.register(Comment)
admin.site.register(Level)
admin.site.register(Language)
admin.site.register(What_you_learn)
admin.site.register(Requirements)
admin.site.register(Lesson, lesson_admin)
admin.site.register(UserCourse)
admin.site.register(Payment)
admin.site.register(Question, question_admin)
admin.site.register(Quizzes, quiz_admin)
admin.site.register(Result)
admin.site.register(Note)
admin.site.register(Role)
admin.site.register(UserRole)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Video, video_admin)
admin.site.register(Watch_Duration)
admin.site.register(Certificate)

