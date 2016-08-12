import re
from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

from .models import Profile, MentorInfo


def phone_validator(value):
    number = ''.join(re.findall(r'\d+', value))
    return RegexValidator(r'^01[016789]\d{7,8}$', message='번호를 입력해주세요')(number)


class ProfileForm(UserCreationForm):
    username = forms.CharField(label='아이디')
    password1 = forms.CharField(label='비밀번호', widget=forms.PasswordInput)
    password2 = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput)
    name = forms.CharField(label='이름')
    phone = forms.CharField(label='휴대폰 번호', widget=forms.TextInput(attrs={'placeholder': 'ex) 010-1234-5678'}), validators=[phone_validator])

    error_messages = {
        'password_mismatch': ("비밀번호가 일치하지 않습니다."),
    }

    def save(self, commit=True):
        user = super(ProfileForm, self).save(commit=False)
        if commit:
            user.save()
            user.profile.name = self.cleaned_data['name']
            user.profile.phone = self.cleaned_data['phone']
            user.profile.save()
        return user


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['name', 'phone', ]


class MentorInfoForm(forms.ModelForm):
    class Meta:
        model = MentorInfo
        fields = ['age', 'gender', 'highschool', 'university', 'major', 'grade', 'career', 'intro', 'image']

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='아이디')
    password = forms.CharField(label='비밀번호', widget=forms.PasswordInput())