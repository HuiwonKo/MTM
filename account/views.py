from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from .models import Profile,MentorInfo
from .forms import ProfileForm, ProfileUpdateForm, MentorInfoForm


def sign_up(request):
    form = ProfileForm(request.POST)
    #register to users
    if request.user.is_anonymous():
        if request.method == "POST":
            if form.is_valid():
                user = form.save()
                authenticated_user = authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password1'])
                login(request,authenticated_user)
                messages.success(request,'환영합니다') #로그인 완료
                return redirect('/')
        else:
            form = ProfileForm()

        return render(request,"account/sign_up.html",{'form':form,})
    else:
        messages.info(request,'이미 로그인되어있습니다. 로그아웃 이후 실행해주세요.')
        return redirect('/')


@login_required
def profile(request):
    user = get_object_or_404(User, pk=request.user.pk)
    profile = get_object_or_404(Profile, pk=request.user.profile.pk)
    if request.method == 'POST':
        if  user.profile.mentor_info:
            form = MentorInfoForm(request.POST, request.FILES, instance=user.profile.mentor_info)
            if form.is_valid():
                mentor_info=form.save(commit=False)
                mentor_info.profile=profile
                mentor_info.save()
            return redirect("profile")
        else:
            form = MentorInfoForm(request.POST, request.FILES)
            if form.is_valid():
                mentor_info=form.save(commit=False)
                mentor_info.profile=profile
                mentor_info.save()
            return redirect("profile")
    else:
        form = MentorInfoForm(instance = user.profile.mentor_info)

    return render(request, 'account/profile.html', {
        'user':user,
        'profile' : profile,
        'form' : form,
    })

@login_required
def profile_edit(request):
    user = get_object_or_404(User, pk=request.user.pk)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance = user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance = user.profile)
    return render(request, 'account/profile_edit.html',{'user':user,'form':form,})