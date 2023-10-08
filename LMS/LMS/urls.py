from django.contrib import admin
from django.urls import path, include
from app import views as app_views, user_login
from forum_app import views as forum_views
from django.conf import settings
from django.conf.urls.static import static
from . import candy

urlpatterns = [

    path('admin/', admin.site.urls),

    *candy.path('base', app_views.BASE,name='base'),

    *candy.path('404', app_views.PAGE_NOT_FOUND, name='404'),

    *candy.path('', app_views.HOME,name='home'),

    *candy.path('courses', app_views.SINGLE_COURSE,name='single_course'),

    *candy.path('courses/filter-data',app_views.filter_data,name="filter-data"),

    *candy.path('course/<slug:slug>',app_views.COURSE_DETAILS,name='course_details'),

    *candy.path('search',app_views.SEARCH_COURSE,name='search_course'),

    *candy.path('contact', app_views.CONTACT_US,name='contact_us'),

    *candy.path('about', app_views.ABOUT_US,name='about_us'),

    *candy.path('become-an-instructor', app_views.BECOME_AN_INSTRUCTOR,name='become_an_instructor'),

    *candy.path('coming_soon', app_views.COMING_SOON,name='coming_soon'),

    *candy.path('event', app_views.EVENT,name='event'),

    *candy.path('accounts/register', user_login.REGISTER, name='register'),

    *candy.path('accounts/learner-register', user_login.LEARNER_SIGNUP, name='learner_register'),

    *candy.path('accounts/instructor-register', user_login.INSTRUCTOR_SIGNUP, name='instructor_register'),

    path('accounts/', include('django.contrib.auth.urls')),

    *candy.path('password_reset', app_views.PASSWORD_RESET,name='password_reset'),

    *candy.path('doLogin', user_login.DO_LOGIN, name='doLogin'),

    *candy.path('accounts/profile', user_login.PROFILE, name='profile'),
    *candy.path('accounts/password', user_login.PASSWORD, name='password'),

    *candy.path('accounts/profile/update', user_login.PROFILE_UPDATE, name='profile_update'),
    *candy.path('accounts/password/update', user_login.CHANGE_PASSWORD, name='password-update'),

    *candy.path('my-course',app_views.MY_COURSE,name='my-course'),

    path('course/watch-course/<slug:slug>',app_views.WATCH_COURSE,name='watch-course'),

    *candy.path('course/<slug:course_slug>/<slug:quizz_slug>',app_views.QUIZ,name='quiz'),

    path('course/<slug:course_slug>/<slug:quizz_slug>/data', app_views.quiz_data_view, name='quiz-data-view'),

    path('course/<slug:course_slug>/<slug:quizz_slug>/save',
         app_views.save_quiz_view, name='save_quiz_view'),

    path('download_avatar/<int:user_id>/', app_views.download_avatar, name='download_avatar'),

    #INSTRUCTOR
    *candy.path('instructor-dashboard', app_views.INSTRUCTOR_SITE, name='instructor-dashboard'),
    *candy.path('instructor-course', app_views.INSTRUCTOR_COURSE, name='instructor-course'),
    *candy.path('instructor-lesson', app_views.INSTRUCTOR_LESSON, name='instructor-lesson'),
    *candy.path('instructor-video', app_views.INSTRUCTOR_VIDEO, name='instructor-video'),
    *candy.path('instructor-quiz', app_views.INSTRUCTOR_QUIZZ, name='instructor-quiz'),
    *candy.path('instructor-question', app_views.INSTRUCTOR_QUESTION, name='instructor-question'),
    *candy.path('instructor-profile', app_views.INSTRUCTOR_PROFILE, name="instructor-profile"),
    *candy.path('instructor-change-password', app_views.INSTRUCTOR_CHANGE_PASSWORD, name="instructor-change-password"),

    #INSTRUCTOR CREATE
    *candy.path('create_course_form', app_views.InstructorCreateCourse, name="create_course_form"),
    *candy.path('create_lesson_form', app_views.InstructorCreateLesson, name="create_lesson_form"),
    *candy.path('create_quiz_form', app_views.InstructorCreateQuiz, name="create_quiz_form"),
    *candy.path('create_video_form', app_views.InstructorCreateVideo, name="create_video_form"),
    *candy.path('create_question_form', app_views.create_question_with_answers, name="create_question_form"),
    *candy.path('create_answer_form', app_views.InstructorCreateQuestion, name="create_answer_form"),
    *candy.path('video-lecture/details/<slug:slug>/',app_views.InstructorUpdateVideo,name='video_lecture_details'),
    *candy.path('lesson/details/<slug:slug>/',app_views.InstructorUpdateLesson,name='lesson_details'),
    *candy.path('instructor-course/details/<slug:slug>/',app_views.InstructorUpdateCourse ,name='instructor_course_details'),
    *candy.path('quiz/details/<slug:slug>/',app_views.InstructorUpdateQuiz ,name='quiz_details'),
    *candy.path('question/details/<slug:slug>/',app_views.InstructorUpdateQuestion ,name='question_details'),

    #INSTRUCTOR UPDATE
    *candy.path('update_course_form', app_views.InstructorUpdateCourse, name="update_course_form"),
    *candy.path('update_lesson_form', app_views.InstructorUpdateLesson, name="update_lesson_form"),
    *candy.path('update_quiz_form', app_views.InstructorUpdateQuiz, name="update_quiz_form"),
    *candy.path('update_video_form', app_views.InstructorUpdateVideo, name="update_video_form"),

    #INSTRUCTOR SEARCH
    *candy.path('instructor/search/course',app_views.INSTRUCTOR_SEARCH_COURSE,name='instructor_search_course'),
    *candy.path('instructor/search/lesson',app_views.INSTRUCTOR_SEARCH_LESSON,name='instructor_search_lesson'),
    *candy.path('instructor/search/quiz',app_views.INSTRUCTOR_SEARCH_QUIZZ,name='instructor_search_quiz'),
    *candy.path('instructor/search/question',app_views.INSTRUCTOR_SEARCH_QUESTION,name='instructor_search_question'),
    *candy.path('instructor/search/video-lecture',app_views.INSTRUCTOR_SEARCH_VIDEO_LECTURE,name='instructor_search_video_lecture'),

    #INSTRUCTOR UPDATE INFORMATION
    *candy.path('instructor/accounts/profile/update', user_login.INSTRUCTOR_PROFILE_UPDATE, name='instructor_profile_update'),
    *candy.path('instructor/accounts/change-password', user_login.INSTRUCTOR_CHANGE_PASSWORD, name='instructor_change_password'),

    #NOTE
    *candy.path('edit-note',app_views.EDIT_NOTE,name='edit_note'),
    *candy.path('create-note',app_views.CREATE_NOTE,name='create_note'),
    *candy.path('delete-note',app_views.DELETE_NOTE,name='delete_note'),

    # email activate
    path('activate/<uidb64>/<token>', user_login.activate, name='activate'),
    path('instructor/activate/<uidb64>/<token>', user_login.save_draft_instructor_account, name='save_draft_instructor_account'),

    #FORUM
    path('forum', forum_views.forum_home, name="forum_home"),
    path('room/<str:pk>/', forum_views.room, name="room"),
    path('profile/<str:pk>/', forum_views.userProfile, name="user-profile"),
    path('topics/', forum_views.topicsPage, name="topics"),
    path('activity/', forum_views.activityPage, name="activity"),
    path('delete-message/<str:pk>/', forum_views.deleteMessage, name="delete-message"),
    path('create-room/', forum_views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', forum_views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', forum_views.deleteRoom, name="delete-room"),

    #PAYMENT
    path('paypal/', include('paypal.standard.ipn.urls')),
    *candy.path('payment-success/<slug:slug>', app_views.PAYMENT_SUCCESS,name='payment-success'),
    *candy.path('payment-failed/<slug:slug>', app_views.PAYMENT_FAILED,name='payment-failed'),
    *candy.path('checkout/<slug:slug>',app_views.CHECKOUT,name='checkout'),
    *candy.path('checkout_free_course/<slug:slug>',app_views.CHECKOUT_FREE_COURSE,name='checkout_free_course'),
    # *candy.path('create_payment',app_views.CREATE_PAYMENT,name='create_payment'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

