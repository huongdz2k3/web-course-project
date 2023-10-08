from django import forms
from django.contrib.auth.models import User
from django.forms import inlineformset_factory, modelformset_factory

from .models import *
from django.contrib.auth.forms import PasswordResetForm
# from captcha.fields import ReCaptchaField
# from captcha.widgets import ReCaptchaV2Checkbox


class LearnerUserInfo(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())  # hash out the password

    class Meta():
        model = User
        fields = ('username', 'email', 'password')


class LearnerSignUpForm(forms.ModelForm):
    class Meta():
        model = Learner
        fields = ('First_Name', 'Last_Name', 'gender')
    # _____________________________________________________________________________________________________________________


class InstructorUserInfo(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())  # hash out the password

    class Meta():
        model = User
        fields = ('email', 'password')


class InstructorSignUpForm(forms.ModelForm):
    class Meta():
        model = Instructor
        fields = ('First_Name', 'Last_Name', 'gender', 'level', 'cv')


# _____________________________________________________________________________________________________________________

class InstructorCreateCourseForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Categories.objects.all(), to_field_name="name")
    level = forms.ModelChoiceField(queryset=Level.objects.all(), to_field_name="name")
    language = forms.ModelChoiceField(queryset=Language.objects.all(),  to_field_name="id")

    class Meta:
        model = Course
        fields = ['featured_video', 'title', 'description', 'price', 'discount', 'deadline', 'slug', 'has_certificate']

class InstructorCreateVideoForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(InstructorCreateVideoForm, self).__init__(*args, **kwargs)

        # Filter the 'course' queryset based on the 'user'
        self.fields['course'].queryset = Course.objects.filter(user=user)

        # Check if 'course' field has been selected, and filter 'lesson' queryset accordingly
        if 'course' in self.data:
            try:
                course_id = int(self.data.get('course'))
                self.fields['lessson'].queryset = Lesson.objects.filter(course_id=course_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['lessson'].queryset = self.instance.course.lesson_set.all()

    class Meta:
        model = Video
        fields = ['lessson', 'course', 'serial_number', 'title', 'description', 'youtube_id', 'time_duration', 'preview']

class InstructorCreateLessonForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(InstructorCreateLessonForm, self).__init__(*args, **kwargs)

        # Filter the 'course' queryset based on the 'user'
        self.fields['course'].queryset = Course.objects.filter(user=user)

    class Meta:
        model = Lesson
        fields = ['course', 'name']

class InstructorCreateQuizzForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(InstructorCreateQuizzForm, self).__init__(*args, **kwargs)

        # Filter the 'course' queryset based on the 'user'
        self.fields['course'].queryset = Course.objects.filter(user=user)

        # Check if 'course' field has been selected, and filter 'lesson' queryset accordingly
        if 'course' in self.data:
            try:
                course_id = int(self.data.get('course'))
                self.fields['lesson'].queryset = Lesson.objects.filter(course_id=course_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['lesson'].queryset = self.instance.course.lesson_set.all()

    class Meta:
        model = Quizzes
        fields = ['course', 'lesson', 'slug', 'topic', 'number_of_questions', 'time_duration', 'require_passing_score', 'total_attempts', 'difficulty_level']


class InstructorCreateQuestionForm(forms.ModelForm):
    quiz = forms.ModelChoiceField(queryset=Quizzes.objects.all(), to_field_name="id")
    class Meta:
        model = Question
        fields = ['quiz', 'text', 'point']

class InstructorCreateAnswerForm(forms.ModelForm):
    question = forms.ModelChoiceField(queryset=Question.objects.all(), to_field_name="id")
    class Meta:
        model = Answer
        fields = ['text', 'correct']

InstructorCreateAnswerFormSet = modelformset_factory(Answer, fields=('text', 'correct'), extra=4)

class InstructorCreateVideoForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(InstructorCreateVideoForm, self).__init__(*args, **kwargs)

        # Filter the 'course' queryset based on the 'user'
        self.fields['course'].queryset = Course.objects.filter(user=user)

        # Check if 'course' field has been selected, and filter 'lesson' queryset accordingly
        if 'course' in self.data:
            try:
                course_id = int(self.data.get('course'))
                self.fields['lessson'].queryset = Lesson.objects.filter(course_id=course_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['lessson'].queryset = self.instance.course.lesson_set.all()

    class Meta:
        model = Video
        fields = ['lessson', 'course', 'serial_number', 'title', 'description', 'youtube_id', 'time_duration', 'preview']


class PasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)

    # captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
