from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

import bcrypt
# Create your views here.


def index(request):
    return render(request, 'users_app/index.html')


def register(request):
    f = request.POST
    valid = True

    if len(f['first_name']) < 3:
        valid = False
        messages.error(request, 'First name must be at least 3 characters.')
    if len(f['last_name']) < 3:
        valid = False
        messages.error(request, 'Last name must be at least 3 characters.')
    if len(f['email']) < 3:
        valid = False
        messages.error(request, 'Email must be at least 3 characters.')
    if len(f['password']) < 8:
        valid = False
        messages.error(request, 'Password must be at least 8 characters.')
    if not f['password'] == f['password_confirmation']:
        valid = False
        messages.error(
            request, 'Password and password confirmation do not match.')

    try:
        User.objects.get(email=f['email'])
        messages.error(request, "An account with that email already exists.")
        valid = False
        # pass
    except:
        # If there are any errors, I will catch them and prevent our program from crashing
        pass

    if valid:

        hashed_pw = bcrypt.hashpw(f['password'].encode(), bcrypt.gensalt())
        print(f"This is the hashed pw {hashed_pw}")
        User.objects.create(
            first_name=f['first_name'], last_name=f['last_name'], email=f['email'], password=hashed_pw)
        # Registration process here
        messages.success(request, "You registered. Please login.")
        return redirect('/')
    else:
        return redirect('/')


def login(request):
    f = request.POST
    valid = True

    try:
        user = User.objects.get(email=f['email'])

    except:
        messages.error(
            request, 'Could not find an account with this email. Please register.')
        return redirect('/')

    if bcrypt.checkpw(f['password'].encode(), user.password.encode()):
        request.session['user_id'] = user.id
        return redirect('/dashboard')
    else:
        messages.error(request, "Password and email didnot match.")
        return redirect('/')


def dashboard(request):
    if not 'user_id' in request.session:
        messages.error(request, "You need to login to view this page")
        return redirect('/')

    user = User.objects.get(id=request.session['user_id'])
    first = user.first_name
    last = user.last_name
    fullname = f"{first} {last}"
    all_jobs = Jobs.objects.all()
    my_list = user.jobs.all()

    context = {
        'logged_user': user,
        'jobs': all_jobs,
        'full': fullname,
        'list': my_list,
    }

    return render(request, 'users_app/dashboard.html', context)


def logout(request):
    messages.success(request, 'You have logged out succesfully.')
    request.session.clear()
    return redirect('/')


def add(request):
    u = User.objects.get(id=request.session['user_id'])
    context = {
        'user': u,
    }
    return render(request, 'users_app/addJob.html', context)


def add_job(request):
    context = {
        'user': User.objects.get(id=request.session['user_id']),
    }
    errors = Jobs.objects.basic_validator(request.POST)
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/addJob', context)
    else:
        f = request.POST
        Jobs.objects.create(
            job=f['job'], location=f['location'], description=f['description'], user_posted=f['user_posted'])
        return redirect('/dashboard')



def edit_job(request):
    num = int(request.POST['id_num'])
    context = {
        "job": Jobs.objects.get(id=num),
        'user': User.objects.get(id=request.session['user_id']),
    }
    edit_Job = Jobs.objects.get(id=num)
    errors = Jobs.objects.basic_validator(request.POST)
    if request.method == "POST":
        if len(errors) > 0:
            # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
            for key, value in errors.items():
                messages.error(request, value)
        # redirect the user back to the form to fix the errors
            return redirect(f'/edit/{num}', context)
        else:
            f = request.POST
            edit_Job.job = f['job']
            edit_Job.description = f['description']
            edit_Job.location = f['location']
            edit_Job.user_posted = f['user_posted']
            edit_Job.save()
            return redirect('/dashboard', context)


def job_info(request, my_val):
    id_num = int(my_val)
    context = {
        "job": Jobs.objects.get(id=id_num),
        'user': User.objects.get(id=request.session['user_id']),
    }
    return render(request, 'users_app/jobInfo.html', context)


def edit_info(request, my_val):
    id_num = int(my_val)
    context = {
        "job": Jobs.objects.get(id=id_num),
        'user': User.objects.get(id=request.session['user_id']),
    }
    return render(request, 'users_app/editJob.html', context)


def delete(request, my_val):
    id_num = int(my_val)
    d = Jobs.objects.get(id=id_num)
    d.delete()
    return redirect('/dashboard')


def job_list(request, my_val):
    id_num = int(my_val)
    this_job = Jobs.objects.get(id=id_num)
    this_user = User.objects.get(id=request.session['user_id'])
    this_user.jobs.add(this_job)
    this_job.users.add(this_user)
    return redirect('/dashboard')
