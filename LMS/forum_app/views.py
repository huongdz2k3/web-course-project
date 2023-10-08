from django.shortcuts import redirect, render

from .forms import RoomForm
from .models import *
from django.http import HttpResponse
from django.db.models import Sum, Q
from django.contrib.auth.decorators import login_required

from app.models import UserRole


@login_required
def forum_home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q),
        Q(host=request.user) | Q(participants__in=[request.user])).distinct()
    topics = Categories.objects.all()[0:]
    room_count = rooms.count()

    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q))[0:3]
    role = UserRole.objects.filter(user = request.user).first().role
    avatar = 'Media/avatar/cat_YZyyv2g.jpg'
    if role == "Learner":
        learner = Learner.objects.get(user=request.user)
        avatar = learner.avatar
    if role == "Instructor":
        instructor = Instructor.objects.get(user=request.user)
        avatar = instructor.avatar
    context = {'rooms': rooms,
               'topics': topics,
               'room_count': room_count,
               'room_messages': room_messages,
               'role': str(role),
               'avatar': avatar}

    return render(request, 'forum_app/forum/home.html', context=context)

@login_required
def createRoom(request):
    form = RoomForm(request.user, request.POST)
    topics = Categories.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Categories.objects.get_or_create(name=topic_name)
        course_id = request.POST.get('course')
        course = Course.objects.get(id=course_id)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            course=course,
            description=request.POST.get('description'),
        )
        return redirect('forum_home')

    context = {'form': form, 'topics': topics}
    return render(request, 'forum_app/forum/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(request.user, request.POST, instance=room)
    topics = Categories.objects.all()
    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Categories.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('forum_home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'forum_app/forum/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        room.delete()
        return redirect('forum_home')
    return render(request, 'forum_app/forum/delete.html', {'obj': room})

@login_required
def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages,
               'participants': participants}
    return render(request, 'forum_app/forum/room.html', context)

@login_required
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    # rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Categories.objects.all()
    context = {'user': user,
               'room_messages': room_messages, 'topics': topics}
    return render(request, 'forum_app/forum/profile.html', context)

@login_required
def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Categories.objects.filter(name__icontains=q)
    return render(request, 'forum_app/forum/topics.html', {'topics': topics})

@login_required
def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'forum_app/forum/activity.html', {'room_messages': room_messages})

@login_required
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('forum_home')
    return render(request, 'forum_app/forum/delete.html', {'obj': message})

