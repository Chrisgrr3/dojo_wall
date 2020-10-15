from django.contrib import messages
from django.shortcuts import redirect, render
from .models import *
import bcrypt
import datetime

# Create your views here.
def index(request):
    context = {
        'all_users': User.objects.all()
    }
    return render(request, 'index.html', context)

def process_user(request):
    errors = User.objects.validate_registration(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect('/')
    entered_password = request.POST['password']
    hash_pass = bcrypt.hashpw(entered_password.encode(), bcrypt.gensalt()).decode()
    User.objects.create(
        first_name= request.POST['first_name'],
        last_name= request.POST['last_name'],
        password = hash_pass,
        email = request.POST['email']
    )
    request.session['user_id'] = User.objects.get(email = request.POST['email']).id
    return redirect('/wall')

def success(request):
    context = {
        'logged_in_user': User.objects.get(id = request.session['user_id']),
        'all_messages': Message.objects.all()[::-1],
        'all_comments': Comment.objects.all(),
    }
    return render(request,'wall.html',context)

def login(request):
    errors = User.objects.validate_login(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return render (request,'index.html')
    request.session['user_id'] = User.objects.get(email = request.POST['email']).id
    return redirect('/wall')

def post_message(request):
    current_user = User.objects.get(id = request.session['user_id'])
    Message.objects.create(content= request.POST['message'], user = current_user)
    current_user.messages.add(Message.objects.last())
    return redirect('/wall')

def post_comment(request):
    current_user = User.objects.get(id = request.session['user_id'])
    Comment.objects.create(
        comment = request.POST['comment'],
        creator = current_user,
    )
    Comment.objects.last().message.add(Message.objects.get(id = request.POST['message_id']))
    return redirect('/wall')

def logout(request):
    request.session.flush()
    return redirect('/')