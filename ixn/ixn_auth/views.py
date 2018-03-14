from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.urls import reverse
from uuid import uuid4
from requests import get
from urllib.parse import urlencode
from matchingsystem.models import Student
from .forms import ClientSignUp

def ucl_login(request):
    return redirect(get_authorisation_url(request))

def get_authorisation_url(request):
    state = str(uuid4())
    request.session['state'] = state # Store to mitigate CSRF attacks
    params = {
        'client_id': '3191669878317281.9925116223526035', # TODO store securely
        'state': state
    }
    authorisation_url = 'https://uclapi.com/oauth/authorise?' + urlencode(params) # TODO store url somewhere
    return authorisation_url

def ucl_callback_url(request):
    state = request.GET.get('state')
    code = request.GET.get('code')

    if(state != request.session.get('state')): # Check for CSFR attacks
        raise Exception('Invalid OAuth state')
    if(code):
        student_code = get_student_code(request, code, state)
        try:
            student = Student.objects.get(pk=student_code) # Get student
        except KeyError:
            raise Exception('Not available for matching')
            # TODO Redirect to error page here? Otherwise create a student account
        except Student.DoesNotExist:
            raise Exception('Not available for matching')
            # Redirect here as well - Student not available in modules for matching

    user = authenticate(request, username=student_code, password='')
    if(user):
        print('user exists')
        login(request, user) # Attach user to current session
    else:
        user = User.objects.create_user(student_code, password='') # Create a non accessible user account
        user.save()
        login(request, user)

    request.session['state'] = None
    return redirect(student.get_absolute_url())

def get_student_code(request, code, state):
    token_params = { # These are the parameters required for UCL API
        'client_id': '3191669878317281.9925116223526035', 
        'code': code,
        'client_secret': '3089442b13bfd0f2ebe924c77d348da644d62a8a56c11aedf3560fee46fda04b'
    }
    token_url = 'https://uclapi.com/oauth/token'
    r_token = get(token_url, params=token_params).json()
    if(state != request.session.get('state')): # Check for CSFR attacks
        raise Exception('Invalid OAuth state')

    user_params = {
        'token': r_token['token'],
        'client_secret': '3089442b13bfd0f2ebe924c77d348da644d62a8a56c11aedf3560fee46fda04b'

    }
    user_data_url = 'https://uclapi.com/oauth/user/studentnumber'
    r_user_data = get(user_data_url, params = user_params)

    if(state != request.session.get('state')):
        raise Exception('Invalid OAuth state')

    r_user_data = r_user_data.json() # Json file of student data
    student_code = r_user_data['student_number']

    return student_code[1:] # Student code should be 8 digits not 9

def ucl_logout(request):
    logout(request) # Detatch user from session
    return redirect('matchingsystem:index')

def client_signup(request):
    if(request.method == 'POST'):
        form = ClientSignUp(request.POST)
        if(form.is_valid()):
            form.save()
#client.first_name = request.POST['first_name']
#client.last_name = request.POST['last_name']
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(reverse('matchingsystem:client', args=[str(username)]))
    else:
        form = ClientSignUp()
    context = {
        'form': form
    }
    return render(request, 'ixn_auth/signup.html', context)

def client_login(request):
    if(request.method == 'POST'):
        form = AuthenticationForm(data=request.POST)
        if(form.is_valid()):
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(reverse('matchingsystem:client', args=[str(username)]))
    else:
        form = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'ixn_auth/login.html', context)


