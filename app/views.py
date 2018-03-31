from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from .models import UserProfile
from django.http import HttpResponseRedirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


def register(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile_url = '/user_profile/' + str(user_profile.id)
        return HttpResponseRedirect(user_profile_url)
    else:
        if request.method == 'POST':
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            email = request.POST.get('email', '')
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            bio = request.POST.get('bio', '')
            mobileNo = request.POST.get('mobileNo', '')
            gender = request.POST.get('gender', '')

            if User.objects.filter(username=username).exists():
                error = 'The Sap_id is already in use by another account.'
                return render(request, 'app/registration.html', {'error': error})

            else:
                user = User.objects.create_user(username=username, email=email, first_name=first_name,
                                                last_name=last_name)
                user.set_password(password)
                user.save()
                Name = first_name + " " + last_name
                student = UserProfile.objects.create(user=user, Name=Name, bio=bio, mobileNo=mobileNo, gender=gender)
                student.save()
                auth_login(request, user)
                student_profile_url = '/user_profile/' + str(student.id)
                return HttpResponseRedirect(student_profile_url)
                # return render(request, 'user_profile/profile.html', {"student": student})
        else:
            return render(request, 'app/registration.html', {})


def login(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        student_profile_url = '/user_profile/' + str(user_profile.id)
        return HttpResponseRedirect(student_profile_url)
    else:
        if request.method == 'POST':
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    auth_login(request, user)
                    student_profile = UserProfile.objects.get(
                        user=request.user, )
                    student_profile_url = '/user_profile/' + str(student_profile.id)
                    return HttpResponseRedirect(student_profile_url)
                else:
                    error = 'Your account is disabled.'
                    return render(request, 'app/login.html', {'error': error})
            else:
                error = 'Incorrect Username or Password'
                return render(request, 'app/login.html', {'error': error})
        else:
            return render(request, 'app/login.html', {})


def logout(request):
    auth_logout(request)
    return redirect(reverse('app:login'))


@login_required(login_url='app:login')
def user_profile(request, id):
    client = get_object_or_404(UserProfile, id=id)

    return render(request, 'app/user_profile.html', {'client': client})
