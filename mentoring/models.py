from __future__ import unicode_literals

import re
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django import forms
from django.utils import timezone
from django.forms import ValidationError

from account.models import GENDER_CHOICES, MAJOR_CHOICES, GRADE_CHOICES, Profile



GPA_CHOICES = (
    ('아주 높은 편','아주 높은 편'),
    ('높은 편','높은 편'),
    ('중간 정도','중간 정도'),
    ('낮은 편','낮은 편'),
    ('아주 낮은 편','아주 낮은 편'),
)

YEAR_CHOICES = (
    ('초등 1학년', '초등 1학년'),
    ('초등 2학년', '초등 2학년'),
    ('초등 3학년', '초등 3학년'),
    ('초등 4학년', '초등 4학년'),
    ('초등 5학년', '초등 5학년'),
    ('초등 6학년', '초등 6학년'),
    ('중등 1학년', '중등 1학년'),
    ('중등 2학년', '중등 2학년'),
    ('중등 3학년', '중등 3학년'),
    ('고등 1학년', '고등 1학년'),
    ('고등 2학년', '고등 2학년'),
    ('고등 3학년', '고등 3학년'),
    ('N수생', 'N수생'),
)

class Post_By_Mentee(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=300, verbose_name='제목')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    gender = models.CharField(max_length=20,choices=GENDER_CHOICES,default='',verbose_name='원하는 멘토 성별')
    major = models.CharField(max_length=20, choices=MAJOR_CHOICES, default='',verbose_name='원하는 멘토 전공')
    year = models.CharField(max_length=40, choices=YEAR_CHOICES, default='', verbose_name='학년')
    GPA = models.CharField(max_length=40, choices=GPA_CHOICES,default='',verbose_name='성취도')
    hours = models.IntegerField(default=0, verbose_name='멘토링 진행시간')
    date = models.DateTimeField(default='yyyy-mm-dd 형식으로 써주세요.', verbose_name='멘토링 날짜')
    price = models.IntegerField(default=0, verbose_name='희망 수업료')
    intro = models.TextField(max_length=300, verbose_name='기타 소개')

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('mentoring:post_by_mentee_detail', args=[self.pk])

class Post_By_Mentor(models.Model):
    title = models.CharField(max_length=300, verbose_name='제목')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    #gender = models.CharField(max_length=20,choices=GENDER_CHOICES,default='',verbose_name='멘토 성별')
    #lnglat = models.CharField(max_length=20, verbose_name='멘토 위치')
    capacity = models.IntegerField(default=0,verbose_name='멘토링 인원')
    hours = models.IntegerField(default=0,verbose_name='멘토링 시간')
    date = models.DateTimeField(default='yyyy-mm-dd 형식으로 써주세요.',verbose_name='멘토링 날짜')
    lowest_price = models.IntegerField(default=0,verbose_name='최저 멘토링비')
    like_count = models.IntegerField(default=0, verbose_name='좋아요 수')
    intro = models.TextField(max_length=300, verbose_name='기타 소개')
    photo1 = models.ImageField()
    photo2 = models.ImageField(blank=True)
    photo3 = models.ImageField(blank=True)
    #matching_time = DateTimeField()

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('mentoring:post_by_mentor_detail', args=[self.pk])

class Bid_By_Mentor(models.Model):
    post_by_mentee = models.ForeignKey(Post_By_Mentee)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    plan = models.TextField(verbose_name='멘토링 커리큘럼')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='멘토')

    def __str__(self):
        return self.author
    def get_absolute_url(self):
        return reverse('mentoring:bid_by_mentor_detail', args=[self.post_by_mentee.pk, self.pk])


class Bid_By_Mentee(models.Model):
    post_by_mentor = models.ForeignKey(Post_By_Mentor)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='멘티')
    price = models.IntegerField(default=0)

    def __str__(self):
        return str(self.author)
    def get_absolute_url(self):
        return reverse('mentoring:bid_by_mentee_detail', args=[self.post_by_mentor.pk, self.pk])

class Like(models.Model):
    like_post = models.ForeignKey(Post_By_Mentor)
    like_user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    post = models.ForeignKey(Post_By_Mentor)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.TextField(max_length=300,verbose_name='댓글 내용')
    secret = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Matched_Bid_By_Mentor(models.Model):
    bid = models.ForeignKey(Bid_By_Mentor)
    mentor = models.CharField(max_length=20, verbose_name='멘토 이름')
    mentee = models.CharField(max_length=20, verbose_name='멘티 이름')
    price = models.IntegerField(default=0, verbose_name='가격')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Matched_Bid_By_Mentee(models.Model):
    bid = models.ForeignKey(Bid_By_Mentee)
    mentor = models.CharField(max_length=20, verbose_name='멘토 이름')
    mentee = models.CharField(max_length=20, verbose_name='멘티 이름')
    price = models.IntegerField(default=0, verbose_name='가격')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)