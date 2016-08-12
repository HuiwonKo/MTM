from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import Q

from .models import Profile,MentorInfo
from .forms import ProfileForm, ProfileUpdateForm, MentorInfoForm

from mentoring.models import Bid_By_Mentee, Bid_By_Mentor, Matched_Bid_By_Mentee, Matched_Bid_By_Mentor, Post_By_Mentee, Post_By_Mentor


def sign_up(request):
    #register to users
    if request.user.is_anonymous():
        if request.method == "POST":
            form = ProfileForm(request.POST)
            if form.is_valid():
                user = form.save()
                authenticated_user = authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password1'])
                login(request,authenticated_user)
                messages.success(request,'환영합니다') #로그인 완료
                return redirect('/')
        else:
            form = ProfileForm()
            return render(request,"account/sign_up.html",{
                'form':form,
               })
    else:
        messages.info(request,'이미 로그인되어있습니다. 로그아웃 이후 실행해주세요.')
        return redirect('/')


@login_required
def profile(request):
    user = get_object_or_404(User, pk=request.user.pk)
    profile = get_object_or_404(Profile, pk=request.user.profile.pk)
    return render(request, 'account/profile.html', {
        'user':user,
        'profile' : profile,
    })

@login_required
def profile_edit(request):
    user = get_object_or_404(User, pk=request.user.pk)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance = user.profile)
        if form.is_valid():
            form.save()
            return render(request, 'account/profile.html',{'user':user,'form':form,})
    else:
        form = ProfileUpdateForm(instance = user.profile)
    return render(request, 'account/profile_edit.html',{'user':user,'form':form,})

@login_required
def mentor_info(request):
    user = get_object_or_404(User, pk=request.user.pk)
    profile = get_object_or_404(Profile, pk=request.user.profile.pk)
    mentor_info = MentorInfo.objects.get(profile=profile)
    return render(request, 'account/mentor_info.html',{
        'user':user,
        'mentor_info':mentor_info,
    })

@login_required
def mentor_info_edit(request):
    user = get_object_or_404(User, pk=request.user.pk)
    profile = get_object_or_404(Profile, pk=request.user.profile.pk)
    try:
        mentor_info = MentorInfo.objects.get(profile=profile)

    except MentorInfo.DoesNotExist:
        mentor_info = None
    if request.method == 'POST':
        form = MentorInfoForm(request.POST, instance = mentor_info)
        if form.is_valid():
            form.save()
            return render(request, 'account/profile.html',{
                'user':user, 'form':form,
                })
    else:
        form = MentorInfoForm(request.POST, instance = mentor_info)
    return render(request, 'account/mentor_info_edit.html',{'user':user, 'form':form,})

@login_required
def matched_list(request):
    user = get_object_or_404(User, pk=request.user.pk)
    matched_list=[]
    matched_list += Matched_Bid_By_Mentee.objects.filter(Q(mentor=user.profile.name)|Q(mentee=user.profile.name))
    matched_list += Matched_Bid_By_Mentor.objects.filter(Q(mentor=user.profile.name)|Q(mentee=user.profile.name))
    return render(request,'account/matched_list.html',{'user':user,'matched_list':matched_list,})

