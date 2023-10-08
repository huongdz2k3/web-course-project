import datetime

import numpy as np
from django.shortcuts import redirect, render
from django.urls import reverse
import requests
import json
from .models import *
from django.template.loader import render_to_string
from django.http import JsonResponse, FileResponse
from django.db.models import Sum, Q
from django.contrib import messages
from . import candy
from django.contrib.auth.decorators import login_required
from .forms import InstructorCreateCourseForm, InstructorCreateLessonForm, InstructorCreateQuizzForm, \
    InstructorCreateVideoForm, PasswordResetForm, InstructorCreateQuestionForm, InstructorCreateAnswerForm, \
    InstructorCreateAnswerFormSet
from .generate_certification import generate_certificates
from .tokens import account_activation_token
from .decorators import user_not_authenticated
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from forum_app.models import Room


# Create your views here.



def BASE(request):
    return candy.render(request, 'app/base.html')


def BLOG(request):
    return render(request, 'app/registration/blog.html')


def EVENT(request):
    return render(request, 'app/Main/event_single.html')


def HOME(request):
    category = Categories.objects.all().order_by('id')[0:6]
    course = Course.objects.order_by('-id')
    instructor = Instructor.objects.all()
    context = {
        'category': category,
        'course': course,
        'instructor': instructor,
    }
    if str(request.user) == "AnonymousUser":
        return candy.render(request, 'app/Main/home.html', context)
    else:
        myRole = UserRole.objects.filter(user=request.user)
        if str(myRole[0]).split('-')[1].strip() == 'Instructor':
            return redirect('instructor-dashboard')
        else:

            user = request.user
            if user.id != None:
                role = UserRole.objects.filter(user=request.user)
            else:
                role = None
            context = {
                'category': category,
                'course': course,
                'user': user,
                'instructor': instructor,
                'role': role,
            }
            return candy.render(request, 'app/Main/home.html', context)


def SINGLE_COURSE(request):
    category = Categories.get_all_category(Categories)
    level = Level.objects.all()
    course = Course.objects.all()
    context = {
        'category': category,
        'level': level,
        'course': course,
    }
    return candy.render(request, 'app/Main/single_course.html', context)


def CONTACT_US(request):
    category = Categories.objects.all().order_by('id')[0:5]
    course = Course.objects.filter(status='PUBLISH').order_by('-id')

    context = {
        'category': category,
        'course': course,
    }
    return candy.render(request, 'app/Main/contact_us.html', context)


def ABOUT_US(request):
    # category = Categories.objects.all().order_by('id')[0:5]
    # course = Course.objects.filter(status='PUBLISH').order_by('-id')
    #
    # context = {
    #     'category': category,
    #     'course': course,
    # }
    return candy.render(request, 'app/Main/about_us.html')


def BECOME_AN_INSTRUCTOR(request):
    return candy.render(request, 'app/Main/become_instructor.html')


def COMING_SOON(request):
    return candy.render(request, 'app/Main/coming_soon.html')


def filter_data(request):
    categories = request.GET.getlist('category[]')
    level = request.GET.getlist('level[]')
    if categories:
        course = Course.objects.filter(
            category__id__in=categories).order_by('-id')
    elif level:
        course = Course.objects.filter(level__id__in=level).order_by('-id')
    else:
        course = Course.objects.all().order_by('-id')
    context = {
        'course': course
    }

    t = render_to_string('app/ajax/course.html', context)

    return JsonResponse({'data': t})


def SEARCH_COURSE(request):
    query = request.GET['query']
    category = Categories.get_all_category(Categories)
    course = Course.objects.filter(title__icontains=query)
    # try:
    #     status = request.GET['status']
    #     level = request.GET['level']
    #     category = request.GET['category']
    # except:
    #     return candy.render(request, 'search/search.html', context)

    context = {
        'course': course,
        'category': category,
    }
    return candy.render(request, 'app/search/search.html', context)


@login_required
def INSTRUCTOR_SEARCH_COURSE(request):
    query = request.GET['query']
    # levels = Level.objects.all()
    status = "All"
    # level = ""
    courses = Course.objects.filter(title__icontains=query, user=request.user)
    print("KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK: ", courses)
    try:
        status = request.GET['status']
        if status == "Confirmed":
            status = "PUBLISH"
        if status == "Pending":
            status = "DRAFT"
    except:
        pass

    # try:
    #     level = request.GET['level']
    #     print("LEVEL: ", level)
    #     print("LEVEL: ", levels["level"])
    # except:
    #     pass

    if status != "All":
        courses = Course.objects.filter(title__icontains=query, status=status, user=request.user)

    # if level == "All" and status != "All":
    #     courses = Course.objects.filter(title__icontains=query, status=status)
    # elif level != "All" and status == "All":
    #     courses = Course.objects.filter(title__icontains=query, level=level)
    # elif level != "All" and status != "All":
    #     if level == "Beginner":
    #         courses = Course.objects.filter(title__icontains=query, level=1, status=status)
    #     if level == "Beginner":
    #         courses = Course.objects.filter(title__icontains=query, level=2, status=status)
    #     if level == "Beginner":
    #         courses = Course.objects.filter(title__icontains=query, level=3, status=status)

    context = {
        'courses': courses,
    }

    return candy.render(request, 'app/instructor/course_search.html', context)


@login_required
def INSTRUCTOR_SEARCH_LESSON(request):
    query = request.GET['query']
    status = "All"
    try:
        status = request.GET['status']
        if status == "Confirmed":
            status = True
        if status == "Pending":
            status = False
    except:
        pass

    courses = Course.objects.filter(user=request.user)

    lessons = []
    if status != "All":
        for course in courses:
            temps = Lesson.objects.filter(name__icontains=query, course=course, status=status)
            lessons.append(temps)
    else:
        for course in courses:
            temps = Lesson.objects.filter(name__icontains=query, course=course)
            lessons.append(temps)

    context = {
        'lessons': lessons,
    }

    return candy.render(request, 'app/instructor/lesson_search.html', context)


@login_required
def INSTRUCTOR_SEARCH_QUIZZ(request):
    query = request.GET['query']
    # category = Categories.get_all_category(Categories)
    courses = Course.objects.filter(user=request.user)
    status = "All"
    try:
        status = request.GET['status']
        if status == "Confirmed":
            status = True
        if status == "Pending":
            status = False
    except:
        pass
    quizzes = []
    if status != "All":
        for course in courses:
            temps = Quizzes.objects.filter(topic__icontains=query, course=course, status=status)
            quizzes.append(temps)
    else:
        for course in courses:
            temps = Quizzes.objects.filter(topic__icontains=query, course=course)
            quizzes.append(temps)
    context = {
        'quizzes': quizzes,
    }

    return candy.render(request, 'app/instructor/quizz_search.html', context)

@login_required
def INSTRUCTOR_SEARCH_QUESTION(request):
    query = request.GET['query']
    # category = Categories.get_all_category(Categories)
    courses = Course.objects.filter(user=request.user)

    status = "All"
    try:
        status = request.GET['status']
        if status == "Confirmed":
            status = True
        if status == "Pending":
            status = False
    except:
        pass
    quizzes = []
    if status != "All":
        for course in courses:
            temps = Quizzes.objects.filter(topic__icontains=query, course=course, status=status)
            quizzes.append(temps)
    else:
        for course in courses:
            temps = Quizzes.objects.filter(topic__icontains=query, course=course)
            quizzes.append(temps)

    context = {
        'quizzes': quizzes,
    }

    return candy.render(request, 'app/instructor/quizz_search.html', context)

@login_required
def INSTRUCTOR_SEARCH_VIDEO_LECTURE(request):
    query = request.GET['query']
    courses = Course.objects.filter(user=request.user)
    try:
        status = request.GET['status']
        if status == "Confirmed":
            status = True
        if status == "Pending":
            status = False
    except:
        pass
    videos = []
    if status != "All":
        for course in courses:
            temps = Video.objects.filter(title__icontains=query, course=course, status=status)
            videos.append(temps)
    else:
        for course in courses:
            temps = Video.objects.filter(title__icontains=query, course=course)
            videos.append(temps)
    context = {
        'videos': videos,
    }

    return candy.render(request, 'app/instructor/video_search.html', context)


def COURSE_DETAILS(request, slug):
    courses = Course.objects.all()
    category = Categories.get_all_category(Categories)
    time_duration = Video.objects.filter(course__slug=slug).aggregate(sum=Sum('time_duration'))
    course_id = Course.objects.get(slug=slug)
    comments = Comment.objects.all()
    quizzes = Quizzes.objects.filter(course=course_id, status=True)
    result = None

    try:
        result = Result.objects.filter(user=request.user)
    except:
        pass

    certificate = None
    user = request.user
    if user.id == None:
        check_enroll = None
    else:
        try:
            check_enroll = UserCourse.objects.get(
                user=request.user, course=course_id)
        except UserCourse.DoesNotExist:
            check_enroll = None

    course = Course.objects.filter(slug=slug)
    if course.exists():
        course = course.first()
    else:
        return redirect('404')
    action = request.GET.get('action')

    try:
        user = User.objects.get(id=request.user.id)
        results = []
        for quiz in quizzes:
            result = Result.objects.get(user=request.user, course=course_id, passed=True, quiz=quiz)
            results.append(result)
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA: ", results)
        certificate = Certificate.objects.get(userID=user, courseID=course_id)
    except:
        pass

    if check_enroll is not None:
        date_text = datetime.datetime.now().strftime("%d-%m-%Y")
        if result is not None and len(results) == quizzes.count() and certificate is None and course_id.has_certificate and quizzes.count() > 0:
            Certificate.objects.create(userID=user, courseID=course_id)
            certificate = Certificate.objects.get(userID=user, courseID=course_id)
            generate_certificates(user.first_name + " " + user.last_name, course_id.title, date_text, certificate.id, course.user.username)

    context = {
        'courses': courses,
        'course': course,
        'category': category,
        'time_duration': time_duration,
        'check_enroll': check_enroll,
        'comments': comments,
        'quizzes': quizzes,
        'result': result,
        'user': user,
        'certificate': certificate,
        'generated_certificate_file': '/Media/certificate/generated-certificates/' + str(
            certificate.id) + '.jpeg' if certificate is not None else None,
        'certificate_file': '/Media/certificate/certificate-template2222.jpeg'
    }


    if action == 'comment':
        print("REQUEST")
        print(request)
        if request.method == 'POST':
            title = request.POST.get('title')
            content = request.POST.get('content')
            # course = request.POST.get('courseTitle')
            print(title, content, course)
            commented = Comment(
                user=request.user,
                course_review=title,
                comment=content,
                course=course
            )
            commented.save()
            messages.success(request, 'Comment successfully')

    return candy.render(request, 'app/course/course_details.html', context)


def PAGE_NOT_FOUND(request):
    return render(request, 'error/404.html')


@login_required
def PAYMENT_SUCCESS(request, slug):
    payment = Payment.objects.get(order_id=slug)
    user_course = UserCourse(
        user=request.user,
        course=payment.course
    )
    user_course.save()
    payment.is_paid = True
    payment.user_course=user_course
    payment.save()
    total = payment.course.price - payment.course.price * payment.course.discount * 0.01
    messages.success(request, 'Enrolled Successfully!')
    current_datetime = datetime.datetime.now()
    formatted_date = current_datetime.strftime("%A, %B %d, %Y")
    context = {
        'payment': payment,
        'total': total,
        'subtotal': payment.course.price * payment.course.discount * 0.01,
        'formatted_date': formatted_date
    }
    return candy.render(request, 'app/checkout/order_completed.html', context)

@login_required
def PAYMENT_FAILED(request, slug):
    try:
        payment = Payment.objects.get(order_id=slug)
        payment.delete()
        # If the payment is successfully deleted, you can redirect to a success page or display a success message.
        messages.success(request, "Enrolled Failed!")
    except Payment.DoesNotExist:
        # If the payment with the given order_id doesn't exist, you can redirect to an error page or display an error message.
        messages.error(request, "Payment not found.")

    return candy.render(request, 'app/course/my-course.html')

@login_required
def CHECKOUT_FREE_COURSE(request, slug):
    course = Course.objects.get(slug=slug)
    user_course = UserCourse(
            user=request.user,
            course=course)
    user_course.save()
    try:
        room = Room.objects.get(course=course)
        room.participants.add(request.user)
        room.save()
    except:
        pass
    messages.success(request, 'Enrolled Successfully!')
    return redirect('my-course')

@login_required
def CHECKOUT(request, slug):
    course = Course.objects.get(slug=slug)
    host = request.get_host()
    paypal_payment_button = None
    rand_id= np.random.randint(100000, 999999)
    if request.method == 'POST':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            country = request.POST.get('country')
            address_1 = request.POST.get('address_1')
            address_2 = request.POST.get('address_2')
            city = request.POST.get('billing_city')
            state = request.POST.get('state')
            postcode = request.POST.get('postcode')
            phone = request.POST.get('phone')
            email = request.POST.get('billing_email')
            order_comments = request.POST.get('order_comments')

            payment = Payment(
                    course=course,
                    user=request.user,
                    order_id=rand_id,
                    country=country,
                    address_1=address_1,
                    address_2=address_2,
                    city=city,
                    state=state,
                    postcode=postcode,
                    phone=phone,
                    email=email,
                    order_comments=order_comments,
                    total=(course.price - course.price * course.discount*0.01),
                    is_paid=False
            )
            payment.save()

            paypal_dict = {
                    'business': settings.PAYPAL_RECEIVER_EMAIL,
                    'amount': course.price - course.price * course.discount * 0.01,
                    'item_name': course.title,
                    'invoice': rand_id,
                    'currency_code': 'USD',
                    'notify_url': 'http://{}{}'.format(host, reverse("paypal-ipn")),
                    'return_url': 'http://{}{}'.format(host, reverse("payment-success", args=[rand_id])),
                    'cancel_url': 'http://{}{}'.format(host, reverse("payment-failed",  args=[rand_id])),
            }
            paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)

    context = {
        'course': course,
        'paypal_payment_button': paypal_payment_button,
    }
    return candy.render(request, 'app/checkout/checkout.html', context)

        #
        #     amount = course.price * 100
        #     currency = 'USD'
        #     notes = {
        #         'name': f'{first_name} {last_name}',
        #         'country': country,
        #         'address': f'{address_1} {address_2}',
        #         'city': city,
        #         'state': state,
        #         'postcode': postcode,
        #         'phone': phone,
        #         'email': email,
        #         'order_comments': order_comments,
        #     }
        #
        #     receipt = f'Course-{int(time())}'
        #     payment = Payment(
        #         course=course,
        #         user=request.user,
        #         order_id=np.random.randint(100000, 999999)
        #     )
        #     payment.save()
        #
        #     course = UserCourse(
        #         user=request.user,
        #         course=course
        #     )
        #     course.save()
        #     messages.success(request, 'Enrolled Successfully!')
        #     return candy.redirect('success')

    # context = {
    #     'course': course,
    # }
    # return candy.render(request, 'app/checkout/checkout.html', context)


@login_required
def MY_COURSE(request):
    category = Categories.get_all_category(Categories)
    course = UserCourse.objects.filter(user=request.user)

    context = {
        'course': course,
        'category': category,
    }
    return candy.render(request, 'app/course/my-course.html', context)


@login_required
def WATCH_COURSE(request, slug):
    course = Course.objects.filter(slug=slug)
    lecture = request.GET.get('lecture')
    notes = Note.objects.filter(user=request.user)
    result = Result.objects.all()
    video = None
    if lecture:
        video = Video.objects.get(id=lecture)
    if course.exists():
        course = course.first()
    else:
        return redirect('404')

    user = request.user
    if user.id == None:
        check_enroll = None
        return redirect('coming_soon')
    else:
        try:
            check_enroll = UserCourse.objects.get(
                user=request.user, course=course)
        except UserCourse.DoesNotExist:
            check_enroll = None
            return redirect('coming_soon')
    if course.course_type == 'PAID':
        url = f"https://dev.vdocipher.com/api/videos/{video.youtube_id}/otp"
        payloadStr = json.dumps({
            'ttl': 300
        })
        headers = {
            'Authorization': "Apisecret fzIhvO1lV5iypxfdpY7sxa6crsWZtJRAzIZeaCWpFQV7toiiF7E7haAXWwHDYNXK",
            'Content-Type': "application/json",
            'Accept': "application/json"
        }

        response = requests.request("POST", url, data=payloadStr, headers=headers)

        json_data = json.loads(response.text)

        otp_value = json_data.get('otp')
        playback_info_value = json_data.get('playbackInfo')
        context = {
            'course': course,
            'video': video,
            'check_enroll': check_enroll,
            'result': result,
            'notes': notes,
            'totalNotes': notes.count(),
            'otp_value': otp_value,
            'playback_info_value': playback_info_value
        }
        return render(request, 'app/course/watch-course.html', context)
    context = {
        'course': course,
        'video': video,
        'check_enroll': check_enroll,
        'result': result,
        'notes': notes,
        'totalNotes': notes.count()
    }
    return render(request, 'app/course/watch-course.html', context)


@login_required
def QUIZ(request, course_slug, quizz_slug):
    category = Categories.get_all_category(Categories)
    course = Course.objects.filter(slug=course_slug)
    if course.exists():
        course = course.first()
    else:
        return redirect('404')

    user = request.user
    if user.id == None:
        check_enroll = None
        return redirect('coming_soon')
    else:
        try:
            check_enroll = UserCourse.objects.get(
                user=request.user, course=course)
        except UserCourse.DoesNotExist:
            check_enroll = None
            return redirect('coming_soon')

    quiz = Quizzes.objects.get(slug=quizz_slug)

    course_id = Course.objects.get(slug=course_slug)
    context = {
        'course': course_id,
        'quiz': quiz,
        'category': category,
    }
    try:
        print("LLLLLLLLLLLLLLLLLLLLLL: ", Result.objects.get(quiz=quiz, user=user))
    except:
        Result.objects.create(quiz=quiz, user=request.user, course=course, attempt=1, score=0)
        return candy.render(request, 'app/quizzes/quizz_detail.html', context)
    try:
        print("PPPPPPPPPPPPPPPPPPPPPPP: ", Result.objects.get(quiz=quiz, user=user).attempt)
        print("PPPPPPPPPPPPPPPPPPPPPPP: ", quiz.total_attempts)
        if (Result.objects.get(quiz=quiz, user=user).attempt < quiz.total_attempts):
            user = user
            attempts = Result.objects.get(quiz=quiz, user=user).attempt + 1
            Result.objects.filter(quiz=quiz, user=user, course=course).update(attempt=attempts)
            quiz_data_view(request, course_slug, quizz_slug)
            return candy.render(request, 'app/quizzes/quizz_detail.html', context)
        else:
            return redirect('home')
    except:
        pass
    quiz_data_view(request, course_slug, quizz_slug)
    return candy.render(request, 'app/quizzes/quizz_detail.html', context)


@login_required
def quiz_data_view(request, course_slug, quizz_slug):
    course = Course.objects.filter(slug=course_slug)
    if course.exists():
        course = course.first()
    else:
        return redirect('404')
    quiz = Quizzes.objects.get(slug=quizz_slug)
    questions = []
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.text)
        questions.append({str(q): answers})
    return JsonResponse({'data': questions,
                         'time': quiz.time_duration})


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@login_required
def save_quiz_view(request, course_slug, quizz_slug):
    course = Course.objects.get(slug=course_slug)
    if is_ajax(request):

        questions = []
        data = request.POST
        print("DATA: ", data)
        data_ = dict(data.lists())
        print("DATA_: ", data_)
        data_.pop('csrfmiddlewaretoken')

        for k in data_.keys():
            question = Question.objects.get(text=k)
            questions.append(question)

        user = request.user
        quiz = Quizzes.objects.get(slug=quizz_slug)

        score = 0
        results = []
        correct_answer = None

        for q in questions:
            a_selected = request.POST.get(q.text)

            if a_selected != "":
                question_answers = Answer.objects.filter(question=q).order_by("?")
                for a in question_answers:
                    if a_selected == a.text:
                        if a.correct:
                            score += q.point
                            correct_answer = a.text
                    else:
                        if a.correct:
                            correct_answer = a.text

                results.append(
                    {str(q): {'correct_answer': correct_answer, 'answered': a_selected}})
            else:
                results.append({str(q): {'not_answered': None}})
        if score >= (quiz.require_passing_score):
            passed = True
        else:
            passed = False

        already_done = False
        add_new = False
        attempt = 0
        try:
            print("TRYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY: ", course)
            print("TRYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY: ", quiz)
            print("TRYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY: ", user)
            a = Result.objects.get(quiz=quiz, user=user, course=course)
            print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA: ", a)
            attempt = a.attempt
            already_done = True
            if a.score <= score:
                add_new = True
            else:
                add_new = False
        except:
            print("EXCEPTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
            attempt = 1
            pass

        if add_new == True and already_done == True:
            a.delete()
            Result.objects.create(quiz=quiz, user=user,
                                  score=score, course=course, passed=passed, attempt=attempt)

        if already_done == False:
            Result.objects.create(quiz=quiz, user=user,
                                  score=score, course=course, passed=passed, attempt=attempt)

        if score >= quiz.require_passing_score:
            return JsonResponse({'passed': True, 'score': score, 'results': results}, safe=False)
        else:
            return JsonResponse({'passed': False, 'score': score, 'results': results}, safe=False)


@login_required()
def INSTRUCTOR_SITE(request):
    if str(request.user) == "AnonymousUser" or str(request.user) == 'admin':
        return candy.render(request, 'app/registration/login.html')
    else:
        myRole = UserRole.objects.filter(user=request.user)
        if str(myRole[0]).split('-')[1].strip() == 'Learner':
            return redirect('home')
        else:
            courses = Course.objects.all().filter(user=request.user)
            pendingCourses = Course.objects.all().filter(status="DRAFT", user=request.user)

            lessons = []
            lessonsCount = 0
            for course in courses:
                lesson = Lesson.objects.all().filter(course=course)
                lessons.append(lesson)

            for lesson in lessons:
                lessonsCount = lessonsCount + lesson.count()

            pendingLessons = []
            plessonsCount = 0
            for course in courses:
                lesson = Lesson.objects.all().filter(course=course, status=False)
                pendingLessons.append(lesson)

            for lesson in pendingLessons:
                plessonsCount = plessonsCount + lesson.count()

            quizzes = []
            quizzesCount = 0
            for course in courses:
                quiz = Quizzes.objects.all().filter(course=course)
                quizzes.append(quiz)

            for quiz in quizzes:
                quizzesCount = quizzesCount + quiz.count()

            pendingQuizzes = []
            pQuizzesCount = 0
            for course in courses:
                quiz = Quizzes.objects.all().filter(course=course, status=False)
                pendingQuizzes.append(quiz)
            for quiz in pendingQuizzes:
                pQuizzesCount = pQuizzesCount + quiz.count()

            videos = []
            videosCount = 0
            for course in courses:
                video = Video.objects.all().filter(course=course)
                videos.append(video)

            for video in videos:
                videosCount = videosCount + video.count()

            pendingVideos = []
            pVideosCount = 0
            for course in courses:
                vid = Video.objects.all().filter(course=course, status=False)
                pendingVideos.append(vid)
            for vid in pendingVideos:
                pVideosCount = pVideosCount + vid.count()

            current_datetime = datetime.datetime.now()
            formatted_date = current_datetime.strftime("%A, %B %d, %Y")
            context = {
                'courses': courses,
                'pendingCourses': pendingCourses,
                'lessons': lessons,
                'plessonsCount': plessonsCount,
                'quizzes': quizzes,
                'pQuizzesCount': pQuizzesCount,
                'videos': videos,
                'pVideosCount': pVideosCount,
                'lessonsCount': lessonsCount,
                'quizzesCount': quizzesCount,
                'videosCount': videosCount,
                'formatted_date': formatted_date
            }
            return candy.render(request, 'app/instructor/instructor_dashboard.html', context=context)


@login_required
def INSTRUCTOR_COURSE(request):
    courses = Course.objects.all().filter(user=request.user)
    categories = Categories.objects.all()
    levels = Level.objects.all()
    context = {
        'courses': courses,
        'categories': categories,
        'levels': levels
    }
    print("COURSES: ", courses)
    print("LEVELS: ", levels)
    return candy.render(request, 'app/instructor/course.html', context=context)


@login_required
def INSTRUCTOR_LESSON(request):
    courses = Course.objects.all().filter(user=request.user)
    lessons = []
    for course in courses:
        lesson = Lesson.objects.all().filter(course=course)
        lessons.append(lesson)
    context = {
        'lessons': lessons
    }
    return candy.render(request, 'app/instructor/lesson.html', context=context)


@login_required
def INSTRUCTOR_VIDEO(request):
    courses = Course.objects.all().filter(user=request.user)
    videos = []
    for course in courses:
        video = Video.objects.all().filter(course=course)
        videos.append(video)

    context = {
        'videos': videos
    }
    return candy.render(request, 'app/instructor/video.html', context=context)


@login_required
def INSTRUCTOR_QUIZZ(request):
    courses = Course.objects.all().filter(user=request.user)
    quizzes = []
    for course in courses:
        quiz = Quizzes.objects.all().filter(course=course)
        quizzes.append(quiz)
    context = {
        'quizzes': quizzes
    }
    return candy.render(request, 'app/instructor/quizz.html', context=context)

@login_required
def INSTRUCTOR_QUESTION(request):
    courses = Course.objects.all().filter(user=request.user)
    questions = []
    for course in courses:
        lessons = Lesson.objects.all().filter(course=course)
        for lesson in lessons:
            quizzes = Quizzes.objects.all().filter(lesson=lesson)
            for quiz in quizzes:
                question = Question.objects.all().filter(quizzes=quiz)
                questions.append(question)
    context = {
        'questions': questions
    }
    return candy.render(request, 'app/instructor/question.html', context=context)

@login_required
def INSTRUCTOR_PROFILE(request):
    instructor = Instructor.objects.filter(user=request.user).get()
    email = request.user.email
    cv = str(instructor.cv).split('/')[-1]
    context = {
        'instructor': instructor,
        'email': email,
        "cv": cv
    }
    return candy.render(request, 'app/instructor/instructor_profile.html', context=context)


@login_required
def InstructorCreateCourse(request):
    createCourseForm = InstructorCreateCourseForm()
    author = User.objects.get(username=request.user)
    message = None
    mydict = {'createCourseForm': createCourseForm,
              'author': author, 'message': message}

    if request.method == 'POST':
        createCourseForm = InstructorCreateCourseForm(request.POST, request.FILES)
        if createCourseForm.is_valid():
            newCourse = createCourseForm.save(commit=False)
            newCourse.user = author
            newCourse.level = Level.objects.get(name=request.POST.get('level'))
            newCourse.category = Categories.objects.get(name=request.POST.get('category'))
            newCourse.language = Language.objects.get(id=request.POST.get('language'))
            newCourse.status = 'DRAFT'
            newCourse.save()
            return redirect('instructor-course')
        else:
            print(createCourseForm.errors)

    else:  # no POST yet
        createCourseForm = InstructorCreateCourseForm()
    return candy.render(request, 'app/instructor/create_course_form.html', context=mydict)


@login_required
def InstructorCreateLesson(request):
    createLessonForm = InstructorCreateLessonForm(request.user, request.POST)
    author = User.objects.get(username=request.user)
    message = None
    mydict = {'createLessonForm': createLessonForm,
              'author': author, 'message': message}

    if request.method == 'POST':
        createLessonForm = InstructorCreateLessonForm(request.user, request.POST)
        if createLessonForm.is_valid():
            newLesson = createLessonForm.save(commit=False)
            newLesson.course = Course.objects.get(id=request.POST.get('course'))
            newLesson.status = False
            newLesson.save()
            return redirect('instructor-lesson')
        else:
            print(createLessonForm.errors)

    else:  # no POST yet
        createLessonForm = InstructorCreateLessonForm(request.user, request.POST)
    return candy.render(request, 'app/instructor/create_lesson_form.html', context=mydict)


@login_required
def InstructorCreateQuiz(request):
    createQuizForm = InstructorCreateQuizzForm(request.user, request.POST)
    author = User.objects.get(username=request.user)
    message = None
    mydict = {'createQuizForm': createQuizForm,
              'author': author, 'message': message}

    if request.method == 'POST':
        createQuizForm = InstructorCreateQuizzForm(request.user, request.POST)
        if createQuizForm.is_valid():
            newQuiz = createQuizForm.save(commit=False)
            newQuiz.course = Course.objects.get(id=request.POST.get('course'))
            newQuiz.lesson = Lesson.objects.get(id=request.POST.get('lesson'))
            newQuiz.status = False
            newQuiz.save()
            return redirect('instructor-quiz')
        else:
            print(createQuizForm.errors)

    else:  # no POST yet
        createQuizForm = InstructorCreateQuizzForm(request.user, request.POST)
    return candy.render(request, 'app/instructor/create_quiz_form.html', context=mydict)

@login_required
def InstructorCreateQuestion(request):
    createQuestionForm = InstructorCreateQuestionForm(request.POST)
    author = User.objects.get(username=request.user)
    message = None
    mydict = {'createQuestionForm': createQuestionForm,
              'author': author, 'message': message}

    if request.method == 'POST':
        createQuestionForm = InstructorCreateQuestionForm(request.POST)
        if createQuestionForm.is_valid():
            newQuestion= createQuestionForm.save(commit=False)
            newQuestion.quizzes = Quizzes.objects.get(id=request.POST.get('quiz'))
            newQuestion.status = False
            newQuestion.save()
            return redirect('instructor-question')
        else:
            print(createQuestionForm.errors)

    else:  # no POST yet
        createQuestionForm = InstructorCreateQuestionForm(request.POST)
    return candy.render(request, 'app/instructor/create_question_form.html', context=mydict)

@login_required
def InstructorCreateAnswer(request):
    createAnswerForm = InstructorCreateAnswerForm(request.POST)
    author = User.objects.get(username=request.user)
    message = None
    mydict = {'createAnswerForm': createAnswerForm,
              'author': author, 'message': message}

    if request.method == 'POST':
        createAnswerForm = InstructorCreateAnswerForm(request.POST)
        if createAnswerForm.is_valid():
            newAnswer= createAnswerForm.save(commit=False)
            newAnswer.question = Question.objects.get(id=request.POST.get('question'))
            newAnswer.status = False
            newAnswer.save()
            return redirect('instructor-answer')
        else:
            print(createAnswerForm.errors)

    else:  # no POST yet
        createAnswerForm = InstructorCreateAnswerForm(request.POST)
    return candy.render(request, 'app/instructor/create_answer_form.html', context=mydict)

def create_question_with_answers(request):
    author = User.objects.get(username=request.user)
    message = None

    if request.method == 'POST':
        createQuestionForm = InstructorCreateQuestionForm(request.POST)
        answer_formset = InstructorCreateAnswerFormSet(request.POST, queryset=Answer.objects.none())

        if createQuestionForm.is_valid() and answer_formset.is_valid():
            newQuestion = createQuestionForm.save(commit=False)
            newQuestion.quizzes = Quizzes.objects.get(id=request.POST.get('quiz'))
            newQuestion.status = False
            newQuestion.save()

            for form in answer_formset:
                answer = form.save(commit=False)
                answer.question = newQuestion
                answer.save()

            return redirect('instructor-question')
        else:
                print(createQuestionForm.errors)
                print(answer_formset.errors)
    else:
        createQuestionForm = InstructorCreateQuestionForm()
        answer_formset = InstructorCreateAnswerFormSet(queryset=Answer.objects.none())

    mydict = {'createQuestionForm': createQuestionForm, 'author': author, 'message': message,
              'answer_formset': answer_formset}
    return candy.render(request, 'app/instructor/create_question_form.html', context=mydict)

@login_required
def InstructorCreateVideo(request):
    createVideoForm = InstructorCreateVideoForm(request.user, request.POST)
    author = User.objects.get(username=request.user)
    message = None
    mydict = {'createVideoForm': createVideoForm,
              'author': author, 'message': message}

    if request.method == 'POST':
        createVideoForm = InstructorCreateVideoForm(request.user, request.POST)
        if createVideoForm.is_valid():
            newVideo = createVideoForm.save(commit=False)
            newVideo.course = Course.objects.get(id=request.POST.get('course'))
            newVideo.lesson = Lesson.objects.get(id=request.POST.get('lessson'))
            newVideo.status = False
            newVideo.save()
            return redirect('instructor-video')
        else:
            print(createVideoForm.errors)

    else:  # no POST yet
        createVideoForm = InstructorCreateVideoForm(request.user, request.POST)
    return candy.render(request, 'app/instructor/create_video_form.html', context=mydict)


def InstructorUpdateCourse(request, slug):
    course = Course.objects.get(slug=slug)
    updateCourseForm = InstructorCreateCourseForm(initial={
        "language": course.language,
        "category": course.category,
        "level": course.level,
        "description": course.description
    })
    # Override the empty_label for the language field
    updateCourseForm.fields['language'].empty_label = None
    updateCourseForm.fields['category'].empty_label = None
    updateCourseForm.fields['level'].empty_label = None
    author = User.objects.get(username=request.user)
    message = None
    mydict = {'updateCourseForm': updateCourseForm,
              'course': course,
              'author': author,
              'message': message,
              'featured_video': course.featured_video,
              'title': course.title,
              'description': course.description,
              'price': course.price,
              'discount': course.discount,
              'deadline': course.deadline,
              'has_certificate': course.has_certificate
              }

    if request.method == 'POST':
        updateCourseForm = InstructorCreateCourseForm(request.POST)
        if updateCourseForm.is_valid():
            course_updated = Course.objects.get(title=course.title)
            course_updated.featured_video = request.POST.get('featured_video')
            course_updated.title = request.POST.get('title')
            course_updated.description = request.POST.get('description')
            course_updated.price = request.POST.get('price')
            course_updated.discount = request.POST.get('discount')
            course_updated.deadline = request.POST.get('deadline')
            course_updated.has_certificate = request.POST.get('has_certificate')
            course_updated.level = Level.objects.get(name=request.POST.get('level'))
            course_updated.category = Categories.objects.get(name=request.POST.get('category'))
            course_updated.language = Language.objects.get(id=request.POST.get('language'))
            course_updated.status = 'DRAFT'

            course_updated.save()
            return redirect('instructor-course')
        else:
            print(updateCourseForm.errors)

    else:  # no POST yet
        updateCourseForm = InstructorCreateCourseForm(request.user)
    return candy.render(request, 'app/instructor/update_course_form.html', context=mydict)

def InstructorUpdateLesson(request, slug):
    lesson = Lesson.objects.get(id=slug)
    updateLessonForm = InstructorCreateLessonForm(request.user, initial={
        "course": lesson.course,
    })
    updateLessonForm.fields['course'].empty_label = None
    author = User.objects.get(username=request.user)
    message = None
    mydict = {'updateLessonForm': updateLessonForm,
              'author': author,
              'message': message,
              'name': lesson.name,
              }

    if request.method == 'POST':
        updateLessonForm = InstructorCreateLessonForm(request.user, request.POST)
        if updateLessonForm.is_valid():
            lesson_updated = Lesson.objects.get(id=lesson.id)
            lesson_updated.name = request.POST.get('name')
            lesson_updated.course = Course.objects.get(id=request.POST.get('course'))
            lesson_updated.status = False

            lesson_updated.save()
            return redirect('instructor-lesson')
        else:
            print(updateLessonForm.errors)

    else:  # no POST yet
        updateLessonForm = InstructorCreateLessonForm(request.user)
    return candy.render(request, 'app/instructor/update_lesson_form.html', context=mydict)

def InstructorUpdateQuiz(request, slug):
    quiz = Quizzes.objects.get(slug=slug)
    updateQuizForm = InstructorCreateQuizzForm(request.user, initial={
        "course": quiz.course,
        "lesson": quiz.lesson,
    })
    updateQuizForm.fields['course'].empty_label = None
    updateQuizForm.fields['lesson'].empty_label = None
    author = User.objects.get(username=request.user)
    message = None
    mydict = {'updateQuizForm': updateQuizForm,
              'author': author,
              'message': message,
              'topic': quiz.topic,
              'number_of_questions': quiz.number_of_questions,
              'time_duration': quiz.time_duration,
              'require_passing_score': quiz.require_passing_score,
              'difficulty_level': quiz.difficulty_level,
              'total_attempts': quiz.total_attempts
              }

    if request.method == 'POST':
        updateQuizForm = InstructorCreateQuizzForm(request.user, request.POST)
        if updateQuizForm.is_valid():
            quiz_updated = Quizzes.objects.get(topic=quiz.topic)
            quiz_updated.topic = request.POST.get('topic')
            quiz_updated.number_of_questions = request.POST.get('number_of_questions')
            quiz_updated.time_duration = request.POST.get('time_duration')
            quiz_updated.require_passing_score = request.POST.get('require_passing_score')
            quiz_updated.total_attempts = request.POST.get('total_attempts')
            quiz_updated.difficulty_level = request.POST.get('difficulty_level')
            quiz_updated.course = Course.objects.get(id=request.POST.get('course'))
            quiz_updated.lesson = Lesson.objects.get(id=request.POST.get('lesson'))
            quiz_updated.status = False

            quiz_updated.save()
            return redirect('instructor-quiz')
        else:
            print(updateQuizForm.errors)

    else:  # no POST yet
        updateQuizForm = InstructorCreateQuizzForm(request.user)
    return candy.render(request, 'app/instructor/update_quiz_form.html', context=mydict)


def InstructorUpdateQuestion(request, slug):
    question = Question.objects.get(id=slug)
    updateQuestionForm = InstructorCreateQuestionForm(initial={
        "quiz": question.quizzes.id,
    })
    updateQuestionForm.fields['quiz'].empty_label = None

    answers = Answer.objects.filter(question=question)

    author = User.objects.get(username=request.user)
    message = None
    answer_formset = InstructorCreateAnswerFormSet(queryset=Answer.objects.none())

    if request.method == 'POST':

        # answer_formset = InstructorCreateAnswerFormSet(request.POST, queryset=Answer.objects.none())

        update_Question = Question.objects.get(id=question.id)
        update_Question.text = request.POST.get('ques_text')
        update_Question.point = request.POST.get('point')
        update_Question.quizzes = Quizzes.objects.get(id=request.POST.get('quiz'))
        update_Question.status = False

        update_Question.save()
        update_Answers = Answer.objects.filter(question=update_Question)

        for ans in update_Answers:
                  ans.text = request.POST.get(f"{ans.id}")
                  print("GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG: ", request.POST.get(f"is_correct_{ans.id}"))
                  # ans.correct = request.POST.get(f"is_correct_{ans.id}")
                  ans.save()
        #         answer = form.save(commit=False)
        #         answer.question = update_Question
        #         answer.text = request.POST.get('ans_text')
        #         answer.correct = request.POST.get('is_correct')
        #         answer.save()

        return redirect('instructor-question')
    else:  # no POST yet
        updateQuestionForm = InstructorCreateQuestionForm()
        # answer_formset = InstructorCreateAnswerFormSet(queryset=Answer.objects.none())

    mydict = {'updateQuestionForm': updateQuestionForm,
              'author': author,
              'message': message,
              'ques_text': question.text,
              'point': question.point,
              'answers': answers,
              'answer_formset': answer_formset}
    return candy.render(request, 'app/instructor/update_question_form.html', context=mydict)

def InstructorUpdateVideo(request, slug):
    video = Video.objects.get(youtube_id=slug)
    # updateVideoForm = InstructorCreateVideoForm(request.user)
    updateVideoForm = InstructorCreateVideoForm(request.user, initial={
        "course": video.course,
        "lessson": video.lessson,
        "description": video.description
    })
    # Override the empty_label for the language field
    updateVideoForm.fields['course'].empty_label = None
    updateVideoForm.fields['lessson'].empty_label = None
    author = User.objects.get(username=request.user)
    message = None
    mydict = {'updateVideoForm': updateVideoForm,
              'author': author,
              'message': message,
              'serial_number': video.serial_number,
              'title': video.title,
              'description': video.description,
              'youtube_id': video.youtube_id,
              'time_duration': video.time_duration,
              'preview': video.preview,
              'video_file': video.video_file,
              }

    if request.method == 'POST':
        updateVideoForm = InstructorCreateVideoForm(request.user, request.POST)
        if updateVideoForm.is_valid():
            video_updated = Video.objects.get(serial_number=video.serial_number)
            video_updated.course = Course.objects.get(id=request.POST.get('course'))
            video_updated.lessson = Lesson.objects.get(id=request.POST.get('lessson'))
            video_updated.serial_number = request.POST.get('serial_number')
            video_updated.title = request.POST.get('title')
            video_updated.description = request.POST.get('description')
            video_updated.youtube_id = request.POST.get('youtube_id')
            video_updated.video_file = request.POST.get('video_file')
            video_updated.time_duration = request.POST.get('time_duration')
            video_updated.preview = request.POST.get('preview')
            video_updated.status = False
            video_updated.save()
            return redirect('instructor-video')
        else:
            print(updateVideoForm.errors)

    else:  # no POST yet
        updateCourseForm = InstructorCreateVideoForm(request.user)
    return candy.render(request, 'app/instructor/update_video_form.html', context=mydict)

@login_required
def VIDEO_LECTURE_DETAILS(request, slug):
    video = Video.objects.get(youtube_id=slug)

    context = {
        'video': video,
    }

    return candy.render(request, 'app/instructor/update_video_form.html', context)

@login_required
def LESSON_DETAILS(request, slug):
    lesson = Lesson.objects.get(id=slug)

    context = {
        'lesson': lesson,
    }

    return candy.render(request, 'app/instructor/update_lesson_form.html', context)

@login_required
def INSTRUCTOR_COURSE_DETAILS(request, slug):
    course = Course.objects.get(slug=slug)

    context = {
        'course': course,
    }

    return candy.render(request, 'app/instructor/update_course_form.html', context)


@login_required
def UPDATE_INSTRUCTOR_PROFILE(request):
    first_name = request.POST().get('fname')
    last_name = request.POST().get('lname')
    phone = request.POST().get('phone')
    gender = request.POST().get('gender')
    cv = request.POST().get('cv')
    user_id = request.user.id

    instructor = Instructor.objects.get(id=user_id)
    instructor.First_Name = first_name
    instructor.Last_Name = last_name
    instructor.phone = phone
    instructor.gender = gender
    instructor.cv = cv

    instructor.save()
    messages.success(request, 'Profile Are Successfully Updated.')
    return candy.render(request, 'app/instructor/instructor_profile.html')


@login_required
def INSTRUCTOR_CHANGE_PASSWORD(request):
    instructor = User.objects.filter(username=request.user).get()
    password = instructor.password

    context = {
        'password': password,
    }
    return candy.render(request, 'app/instructor/instructor_change_password.html', context=context)


@login_required
def EDIT_NOTE(request):
    noteId = request.POST.get("noteId")
    if request.method == "POST":
        noteContent = request.POST.get("note")
        Note.objects.filter(id=int(noteId)).update(body=noteContent, updated_at=datetime.datetime.now())
        Note.objects.filter(id=1).delete
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def CREATE_NOTE(request):
    # noteId = request.POST.get("noteId")
    if request.method == "POST":
        note = request.POST.get("note")
        Note.objects.create(user=request.user, body=note)
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def DELETE_NOTE(request):
    noteId = request.POST.get("noteId")
    if request.method == "POST":
        note = Note.objects.get(user=request.user, id=int(noteId))
        note.delete()
    return redirect(request.META.get('HTTP_REFERER'))


def PASSWORD_RESET(request):
    # if request.method == 'POST':
    #     email = request.POST.get('email')
    #     # check email
    #     if User.objects.filter(email=email).exists():
    #         #send link reset password
    #         pass
    return candy.render(request, 'app/registration/password_reset_form.html')
    # return render(request, 'Main/event_single.html')




@user_not_authenticated
def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = "Password Reset request"
                message = render_to_string("template_reset_password.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(subject, message, to=[associated_user.email])
                if email.send():
                    messages.success(request,
                                     """
                        <h2>Password reset sent</h2><hr>
                        <p>
                            We've emailed you instructions for setting your password, if an account exists with the email you entered. 
                            You should receive them shortly.<br>If you don't receive an email, please make sure you've entered the address 
                            you registered with, and check your spam folder.
                        </p>
                        """
                                     )
                else:
                    messages.error(request, "Problem sending reset password email, <b>SERVER PROBLEM</b>")

            return redirect('home')

        for key, error in list(form.errors.items()):
            if key == 'captcha' and error[0] == 'This field is required.':
                messages.error(request, "You must pass the reCAPTCHA test")
                continue

    form = PasswordResetForm()
    return candy.render(
        request=request,
        template_name='app/registration/password_reset_form.html',
        context={"form": form}
    )


def download_avatar(request, user_id):
    user = User.objects.get(id=user_id)
    learner = Learner.objects.get(user=user)

    response = FileResponse(learner.avatar, content_type='image/jpeg')  # Change content type as needed
    response['Content-Disposition'] = f'attachment; filename="{learner.avatar}"'

    return response

