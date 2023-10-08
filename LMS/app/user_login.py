import re
# from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib import messages
# from django.urls import reverse
# from forms import InstructorSignUpForm, InstructorUserInfo, LearnerSignUpForm, LearnerUserInfo
from . import candy
from .EmailBackEnd import EmailBackEnd
from django.contrib.auth import login
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from .models import UserRole, Role, Learner, Instructor
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.contrib.auth.hashers import check_password

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('homepage')

def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("app/email/template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, mark_safe(f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
                received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.'))
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')

def save_draft_instructor_account(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        instructor = Instructor.objects.get(user=user)
        instructor.status = False
        instructor.save()

        messages.success(request, "Thank you for your email confirmation. To complete the registration process, please wait for the information to be confirmed by the system administrator")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('homepage')

def activateInstructorEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("app/email/template_active_account_instructor.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, mark_safe(f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
                received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.'))
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')

def REGISTER(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # check email
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already exist!')
            return redirect('register')

        # check username
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already exist!')
            return redirect('register')

        #check password
        if password1 != password2:
            messages.error(request, 'Your password does not match')
            return redirect('register')

        else:
            if len(password1) < 10 or not re.findall('[A-Z]', password1) or not re.findall('[@#$%!^&*]', password1):
                messages.error(request, mark_safe('<b>Your password is invalid, it must satisfy the following factors:<b\>'))
                messages.warning(request,
                               mark_safe('Containing at least 10 characters.<br/> Containing at least 1 uppercase letter.<br/> Containing at least 1 uppercase letter.<br/> Containing at least 1 special character'))
                return redirect('register')
        user = User(
            username=username,
            email=email,
        )
        user.set_password(password1)
        user.is_active = False
        user.save()
        # activateEmail(request, user, email)
        return redirect('login')

    return candy.render(request,'app/registration/register.html')

def DO_LOGIN(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')
        myUser = EmailBackEnd.authenticate(request,
                                         email=email,
                                         password=password)
        myRole = UserRole.objects.filter(user = myUser)

        if myUser != None and email != "" and password != "" and role != "":
                if myUser.is_active:
                    if str(myRole[0].role) == role:
                        if role == 'Learner':
                            login(request, myUser)
                            return redirect('home')
                        if role == 'Instructor':
                            try:
                                instructor = Instructor.objects.get(user=myUser)
                            except:
                                messages.error(request,
                                               'You tried to log in with the wrong permissions or your account still not be activated, please try again!')
                                return candy.render(request, 'app/registration/login.html')
                            if instructor.status == True:
                                login(request, myUser)
                            return redirect('instructor-dashboard')
                        else:
                            messages.error(request, 'You tried to log in with the wrong permissions or your account still not be activated, please try again!')
                            return candy.render(request,'app/registration/login.html')
                    else:
                        messages.error(request, 'You tried to log in with the wrong permissions !')
                        return candy.render(request,'app/registration/login.html')
                else:
                    messages.error(request, 'Your account has not been activated !')
                    return candy.render(request,'app/registration/login.html')
        else:
            messages.error(request, 'Email/Password Is Invalid !')
            return candy.render(request,'app/registration/login.html')
    else:
        return candy.render(request,'app/registration/login.html')


def PROFILE(request):
    user = User.objects.get(id=request.user.id)
    learner = Learner.objects.get(user=user)
    current_avatar = learner.avatar
    avatar = request.POST.get('avatar')
    context = {
        'user_id': request.user.id,
        'learner': learner,
        'avatar': avatar,
        'current_avatar': current_avatar
    }
    return candy.render(request,'app/registration/profile.html', context=context)

def PASSWORD(request):
    return candy.render(request,'app/registration/password.html')

def PROFILE_UPDATE(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        avatar = request.FILES.get('avatar')
        user_id = request.user.id

        user = User.objects.get(id = user_id)
        learner = Learner.objects.get(user=user)

        if first_name != None and first_name != "":
            user.first_name = first_name


        if last_name != None and last_name != "":
            user.last_name = last_name

        if avatar != None:
            learner.avatar = avatar

        if username != None and username != "":
            user.username = username

        user.save()
        learner.save()
        messages.success(request, 'Profile Are Successfully Updated')
        return redirect('profile')


def CHANGE_PASSWORD(request):
    user = User.objects.get(id=request.user.id)
    password = user.password
    if request.method == "POST":
        current_password = request.POST.get('password')
        new_password = request.POST.get('newPassword')
        re_new_password = request.POST.get('reNewPassword')

        if new_password != re_new_password:
            messages.error(request, 'New password does not match')
            return redirect('password')

        if not check_password(current_password, password):
            messages.error(request, 'Current password does not correct')
            return redirect('password')

        user.set_password(new_password)
        user.save()
        messages.success(request, 'Password Successfully Updated')
        return redirect('login')

@login_required
def INSTRUCTOR_PROFILE_UPDATE(request):
    if request.method == "POST":
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        cv = request.FILES.get('cv')
        avatar = request.FILES.get('avatar')
        user_id = request.user.id

        user = User.objects.get(id=user_id)
        instructor = Instructor.objects.get(user=user)

        if first_name != None and first_name != "":
            user.first_name = first_name
            instructor.First_Name = first_name
        if last_name != None and last_name != "":
            user.last_name = last_name
            instructor.Last_Name = last_name
        if phone != None and phone != "":
            instructor.phone = phone
        if gender != None and gender != "":
            instructor.gender = gender
        if cv != None:
            instructor.cv = cv
        if avatar != None:
            instructor.avatar = avatar

        user.save()
        instructor.save()

        messages.success(request, 'Profile Are Successfully Updated')
        return redirect('instructor-profile')


@login_required
def INSTRUCTOR_CHANGE_PASSWORD(request):
    user = User.objects.get(id=request.user.id)
    password = user.password
    if request.method == "POST":
        current_password = request.POST.get('currentPassword')
        new_password = request.POST.get('newPassword')
        re_new_password = request.POST.get('reNewPassword')

        if new_password != re_new_password:
            messages.error(request, 'New password does not match')
            return redirect('instructor-change-password')

        if not check_password(current_password, password):
            messages.error(request, 'Current password does not correct')
            return redirect('instructor-change-password')

        user.set_password(new_password)
        user.save()
        messages.success(request, 'Password Successfully Updated')
        return redirect('login')


def LEARNER_SIGNUP(request):

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        firstName = request.POST.get('First_Name')
        lastName = request.POST.get('Last_Name')
        password = request.POST.get('password1')
        re_password = request.POST.get('password2')
        gender = request.POST.get('gender')

        # check email
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already exist')
            return redirect('register')

        # check username
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already exist')
            return redirect('register')

        # check firstName and lastName
        if not firstName.isalpha() or not lastName.isalpha():
            messages.error(request, 'First and Last Name can only contain characters')
            return redirect('register')

        #check password
        if password != re_password:
            messages.error(request, 'Your password does not match')
            return redirect('register')

        else:
            if len(password) < 10 or not re.findall('[A-Z]', password) or not re.findall('[0-9]', password) or not re.findall('[@#$%!^&*]', password):
                messages.error(request, mark_safe('<b>Your password is invalid, it must satisfy the following factors:<b\>'))
                messages.warning(request,
                               mark_safe('Containing at least 10 characters.<br/> Containing at least 1 uppercase letter.<br/> Containing both letters and numbers.<br/> Containing at least 1 special character'))
                return redirect('register')

        user = User(
            first_name=firstName,
            last_name=lastName,
            username=username,
            email=email,
            is_active=False
        )

        user.set_password(password)
        user.save()

        learner = Learner(
            user=user,
            First_Name= firstName,
            Last_Name = lastName,
            gender = gender,
            role = Role.objects.get(role = "Learner")
        )
        learner.save()
        userRole = UserRole(
            user=user,
            role=learner.role
        )
        userRole.save()
        activateEmail(request ,user, email)
        return redirect('login')

    return candy.render(request,'app/registration/register.html')

def INSTRUCTOR_SIGNUP(request):

   if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        firstName = request.POST.get('First_Name')
        lastName = request.POST.get('Last_Name')
        password = request.POST.get('password1')
        re_password = request.POST.get('password2')
        gender = request.POST.get('gender')
        cv = request.FILES.get('cv')

        # check email
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already exist')
            return redirect('register')

        # check username
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already exist')
            return redirect('register')

        # check firstName and lastName
        if not firstName.isalpha() or not lastName.isalpha():
            messages.error(request, 'First and Last Name can only contain characters')
            return redirect('register')

        #check password
        if password != re_password:
            messages.error(request, 'Your password does not match')
            return redirect('register')

        else:
            if len(password) < 10 or not re.findall('[A-Z]', password) or not re.findall('[0-9]', password) or not re.findall('[@#$%!^&*]', password):
                messages.error(request, mark_safe('<b>Your password is invalid, it must satisfy the following factors:<b\>'))
                messages.warning(request,
                               mark_safe('Containing at least 10 characters.<br/> Containing at least 1 uppercase letter.<br/> Containing both letters and numbers.<br/> Containing at least 1 special character'))
                return redirect('register')

        user = User(
            username=username,
            email=email,
            is_active=False
        )
        user.set_password(password)
        user.save()

        instructor = Instructor(
            user=user,
            First_Name= firstName,
            Last_Name = lastName,
            gender = gender,
            phone = phone,
            cv = cv,
            role = Role.objects.get(role = "Instructor")
        )
        instructor.save()

        userRole = UserRole(
            user=user,
            role=instructor.role
        )
        userRole.save()
        activateInstructorEmail(request, user, email)
        return redirect('login')

   return candy.render(request,'app/registration/register.html')

    