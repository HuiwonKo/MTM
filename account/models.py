from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User

from mtm.utils import thumbnail, random_name_upload_to


GENDER_CHOICES = (
    ('남', '남'),
    ('여', '여'),
)

MAJOR_CHOICES = (
    ('간호대학', '간호대학'),
    ('건축학과', '건축학과'),
    ('경영대학', '경영대학'),
    ('농경제사회학부', '농경제사회학부'),
    ('사회과학계열', '사회과학계열'),
    ('심리학과', '심리학과'),
    ('소비자아동학부', '소비자아동학부'),
    ('의류학과', '의류학과'),
    ('인문계열', '인문계열'),
    ('언어학과', '언어학과'),
    ('교육학과', '교육학과'),
    ('국어교육과', '국어교육과'),
    ('물리교육과', '물리교육과'),
    ('사회교육과', '사회교육과'),
    ('생물교육과', '생물교육과'),
    ('역사교육과', '역사교육과'),
    ('영어교육과', '영어교육과'),
    ('지구과학교육과', '지구과학교육과'),
    ('지리교육과', '지리교육과'),
    ('체육교육과', '체육교육과'),
    ('화학교육과', '화학교육과'),
    ('수학교육과', '수학교육과'),
    ('물리천문학부', '물리천문학부'),
    ('바이오시스템소재학부', '바이오시스템소재학'),
    ('산림과학부', '산림과학부'),
    ('생명과학부', '생명과학부'),
    ('수리과학부', '수리과학부'),
    ('식물생산과학부', '식물생산과학부'),
    ('식품영양학과', '식품영양학과'),
    ('응용생물화학부', '응용생물화학부'),
    ('화학부', '화학부'),
    ('건설환경공학부', '건설환경공학부'),
    ('기계항공공학부', '기계항공공학부'),
    ('산업공학과', '산업공학과'),
    ('식품동물생명공학부', '식품동물생명공학부'),
    ('재료공학부', '재료공학부'),
    ('전기정보공학부', '전기정보공학부'),
    ('조경지역시스템공학부', '조경지역시스템공학부'),
    ('조선해양공학과', '조선해양공학과'),
    ('컴퓨터공학부', '컴퓨터공학부'),
    ('화학생물공학부', '화학생물공학부'),
    ('의예과', '의예과'),
)

GRADE_CHOICES = (
    ('1학년', '1학년'),
    ('2학년','2학년'),
    ('3학년','3학년'),
    ('4학년 이상','4학년 이상'),
)



class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #mentor_info = models.OneToOneField(MentorInfo, null=True)
    name = models.CharField(max_length=20, verbose_name='이름')
    phone = models.CharField(max_length=20, verbose_name='전화번호')

    def __str__(self):
        return self.name + " ( ID : "+self.user.username+" )"


class MentorInfo(models.Model):
    profile = models.OneToOneField(Profile, null=True)
    age = models.IntegerField(default=0)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='', verbose_name='성별')
    highschool = models.CharField(max_length=40, verbose_name='출신 고등학교')
    university = models.CharField(max_length=40, verbose_name='재학중인 대학교')
    major = models.CharField(max_length=40, choices=MAJOR_CHOICES, default='', verbose_name='전공')
    grade = models.CharField(max_length=40, choices=GRADE_CHOICES, default='', verbose_name='학년')
    career = models.TextField(verbose_name='약력')
    intro = models.TextField(verbose_name='기타 소개')
    image = models.ImageField(blank=True, null=True, upload_to=random_name_upload_to, verbose_name='멘토 소개 사진')

def pre_on_mentorimage_save(sender, **kwargs):
    mentor_image = kwargs['instance']
    if mentor_image.image:
        max_width = 800
        if mentor_image.image.width > max_width or mentor_image.image.height > max_width:
            processed_file = thumbnail(mentor_image.image.file, max_width, max_width)
            mentor_image.image.save(mentor_image.image.name, File(processed_file))

pre_save.connect(pre_on_mentorimage_save, sender=MentorInfo)

def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        profile = Profile(user=user)
        profile.save()

post_save.connect(create_profile, sender=User)

