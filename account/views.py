from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect,get_object_or_404

from .models import Profile,MentorInfo
from .forms import ProfileForm, ProfileUpdateForm, MentorInfoForm


def signup(request):
    #register to users
    if request.user.is_anonymous():
        if request.method == "POST":
            form = ProfileForm(request.POST)
            if form.is_valid():
                user = form.save()
                authenticated_user = authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password1'])
                login(request,authenticated_user)
                messages.success(request,'환영합니다') #로그인 완료
                return redirect(settings.LOGIN_URL)
        else:
            form = ProfileForm()
            return render(request,"account/sign_up.html",{
                'form':form,
                'user':user,
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

@login_required
def mentor_info(request):
    user = get_object_or_404(User, pk=request.user.pk)
    profile = get_object_or_404(Profile, pk=request.user.profile.pk)
    mentor_info = MentorInfo.objects.filter(profile=profile)
    return render(request, 'account/mentor_info.html',{
        'user':user,
        'mentor_info':mentor_info,
    })

@login_required
def mentor_info_edit(request):
    user = get_object_or_404(User, pk=request.user.pk)

    if request.method == 'POST':
        form = MentorInfoUpdateForm(request.POST, instance = user.profile)
        if form.is_valid():
            form.save()
            return redirect('mentor_info_edit')
    else:
        form = MentorUpdateForm(request.POST, instance = user.profile)
    return render(request, 'account/mentor_info_edit.html',{'user':user, 'form':form,})

@login_required
def matched_list(request):
    user = get_object_or_404(User, pk=request.user.pk)
    matched_list=[]
    matched_list += Matched_Bid_By_Mentee.objects.filter(mentor=request.user or mentee=request.user)
    matched_list += Matched_Bid_By_Mentor.objects.filter(mentor=request.user or mentee=request.user)
    return render(request,'account/matched_list.html',{'user':user,'matched_list':matched_list,})

