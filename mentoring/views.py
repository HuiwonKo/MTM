from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect

from .match import auction_algo
from .models import Post_By_Mentor, Post_By_Mentee, Bid_By_Mentee, Bid_By_Mentor, Comment, Like, Matched_Bid_By_Mentee, Matched_Bid_By_Mentor
from .forms import Post_By_MenteeForm, Post_By_MentorForm, Bid_By_MenteeForm, Bid_By_MentorForm, CommentForm
from datetime import timedelta

def index(request):
    return render(request, 'mentoring/index.html')


def mentor_list(request):
    mentor_list = Post_By_Mentor.objects.all()
    return render(request, 'mentoring/mentor_list.html',{
        'mentor_list' : mentor_list,
    })

def post_by_mentor_detail(request, pk):
    post_by_mentor = get_object_or_404(Post_By_Mentor, pk=pk)
    bid_by_mentee = Bid_By_Mentee.objects.filter(post_by_mentor=pk).count()
    comment_list = Comment.objects.filter(post=post_by_mentor)
    if request.user.is_authenticated():
        if request.method == "POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post_by_mentor
                comment.author = request.user
                comment.save()
                return redirect(post_by_mentor)
        else:
            form = CommentForm()
        return render(request, 'mentoring/post_by_mentor_detail.html', {
            'post_by_mentor' : post_by_mentor,
            'bid_by_mentee' : bid_by_mentee,
            'form' : form,
            'comment_list' : comment_list,
        })
    else:
        return render(request, 'mentoring/post_by_mentor_detail.html', {
            'post_by_mentor' : post_by_mentor,
            'bid_by_mentee' : bid_by_mentee,
            'form' : form,
            'comment_list' : comment_list,
        })

@login_required
def post_by_mentor_new(request):
    if request.method == "POST":
        form = Post_By_MentorForm(request.POST, request.FILES)
        if form.is_valid():
            post_by_mentor = form.save(commit=False)
            post_by_mentor.author = request.user
            post_by_mentor.save()
            return redirect('mentoring:mentor_list')
    else:
        form = Post_By_MentorForm()
    return render(request, 'mentoring/post_by_mentor_form.html', {
        'form' : form,
    })

@login_required
def post_by_mentor_edit(request, pk):
    post_by_mentor = get_object_or_404(Post_By_Mentor, pk=pk)
    if request.method == "POST":
        form = Post_By_MentorForm(request.POST, request.FILES, instance=post_by_mentor)
        if form.is_valid():
            post_by_mentor = form.save(commit=False)
            post_by_mentor.save()
            messages.success(request, '멘토링 포스트 정보가 수정되었습니다.')
            return redirect(post_by_mentor)
    else:
        form = Post_By_MentorForm(instance=post_by_mentor)
    return render(request, 'mentoring/post_by_mentor_edit.html', {
        'post_by_mentor' : post_by_mentor,
        'form' : form,
    })

@login_required
def post_by_mentor_delete(request, pk):
    post_by_mentor = get_object_or_404(Post_By_Mentor, pk=pk)
    if request.user != post_by_mentor.author:
        messages.error(request, "해당 멘토링을 삭제할 권한이 없습니다.")
        return redirect(post_by_mentor, pk=post_by_mentor.pk)
    post_by_mentor.delete()
    messages.error(request, "해당 멘토링 포스트가 삭제되었습니다.")
    return render(request, 'mentoring/post_by_mentor_detail.html', {
        'post_by_mentor' : post_by_mentor,
    })

@login_required
def bid_by_mentee_detail(request, post_pk, pk):
    post_by_mentor = get_object_or_404(Post_By_Mentor, pk=post_pk)
    bid_by_mentee = get_object_or_404(Bid_By_Mentee, pk=pk)
    return render(request, 'mentoring/bid_by_mentee_detail.html', {
        'post_by_mentor' : post_by_mentor,
        'bid_by_mentee' : bid_by_mentee,
    })

@login_required
def bid_by_mentee_new(request, post_pk):
    post_by_mentor = get_object_or_404(Post_By_Mentor, pk=post_pk)
    if request.method == "POST":
        form = Bid_By_MenteeForm(request.POST, request.FILES)
        if form.is_valid():
            bid_by_mentee = form.save(commit=False)
            bid_by_mentee.author = request.user
            bid_by_mentee.post_by_mentor = post_by_mentor
            bid_by_mentee.save()
            messages.success(request, '멘토링 지원이 완료되었습니다.')
            return redirect(post_by_mentor)
    else:
        form = Bid_By_MenteeForm()
    return render(request, 'mentoring/bid_by_mentee_form.html', {
        'form' : form,
    })

@login_required
def bid_by_mentee_edit(request, post_pk, pk):
    post_by_mentor = get_object_or_404(Post_By_Mentor, pk=post_pk)
    bid_by_mentee = get_object_or_404(Bid_By_Mentee, pk=pk)
    if request.method == "POST":
        form = Bid_By_MenteeForm(request.POST, request,FILES, instance=bid_by_mentee)
        if form.is_valid():
            bid_by_mentee = form.save(commit=False)
            bid_by_mentee.author = request.user
            bid_by_mentee.save()
            messages.success(request, '수정이 완료되었습니다.')
            return redirect(bid_by_mentee)
    else:
        form = Bid_By_MenteeForm()
    return render(request, 'mentoring/bid_by_mentee_form.html', {
        'bid_by_mentee_form' : form,
    })

@login_required
def bid_by_mentee_delete(request, post_pk, pk):
    post_by_mentor = get_object_or_404(Post_By_Mentor, pk=post_pk)
    bid_by_mentee = get_object_or_404(Bid_By_Mentee, pk=pk)
    if request.user != bid_by_mentee.author:
        messages.error(request, "자신이 작성한 멘토링 신청서만 삭제할 수 있습니다.")
        return redirect(bid_by_mentee)
    bid_by_mentee.delete()
    messages.error(request, "멘토링 신청서가 삭제되었습니다.")
    return redirect(post_by_mentor)

def mentee_list(request):
    mentee_list = Post_By_Mentee.objects.all()
    return render(request, 'mentoring/mentee_list.html', {
        'mentee_list' : mentee_list,
    })

def post_by_mentee_detail(request, pk):
    post_by_mentee = get_object_or_404(Post_By_Mentee, pk=pk)

    bid_by_mentor = Bid_By_Mentor.objects.filter(post_by_mentee=pk).count()

    if request.user.is_authenticated():
        return render(request, 'mentoring/post_by_mentee_detail.html', {
            'post_by_mentee' : post_by_mentee,
            'bid_by_mentor' : bid_by_mentor,
        })
    else:
        return render(request, 'mentoring/post_by_mentee_detail.html', {
            'post_by_mentee' : post_by_mentee,
            'bid_by_mentor' : bid_by_mentor,
        })




@login_required
def post_by_mentee_new(request):
    if request.method == "POST":
        form = Post_By_MenteeForm(request.POST, request.FILES)
        if form.is_valid():
            post_by_mentee = form.save(commit=False)
            post_by_mentee.author = request.user
            post_by_mentee.save()
            return redirect('mentoring:mentee_list')
    else:
        form = Post_By_MenteeForm()
    return render(request, 'mentoring/post_by_mentee_form.html', {
        'form' : form,
    })

@login_required
def post_by_mentee_edit(request, pk):
    post_by_mentee = get_object_or_404(Post_By_Mentee, pk=pk)
    if request.method == "POST":
        form = Post_By_MenteeForm(request.POST, request.FILES, instance=post_by_mentee)
        if form.is_valid():
            post_by_mentee = form.save(commit=False)
            post_by_mentee.author = request.user
            post_by_mentee.save()
            messages.success(request, '멘토링 포스트 정보가 수정되었습니다.')
            return redirect(post_by_mentee)
    else:
        form = MentorDetailForm(instance=post_by_mentee)
    return render(request, 'mentoring/post_by_mentor_form.html', {
        'form' : form,
    })

@login_required
def post_by_mentee_delete(request,pk):
    post_by_mentee = get_object_or_404(Post_By_Mentee, pk=pk)
    if request.user != post_by_mentee.author:
        messages.error(request, "해당 멘토링을 삭제할 권한이 없습니다.")
        return redirect(post_by_mentee, pk=post_by_mentee.pk)
    post_by_mentee.delete()
    messages.error(request, "해당 멘토링 포스트가 삭제되었습니다.")
    return redirect(mentee_list)

@login_required
def bid_by_mentor_detail(request, post_pk, pk):
    post_by_mentee = get_object_or_404(Post_By_Mentee, pk=post_pk)
    bid_by_mentor = get_object_or_404(Bid_By_Mentor, pk=pk)
    return render(request, 'mentoring/bid_by_mentor_detail.html', {
        'post_by_mentee' : post_by_mentee,
        'bid_by_mentor' : bid_by_mentor,
    })

@login_required
def bid_by_mentor_new(request, post_pk):
    post_by_mentee = get_object_or_404(Post_By_Mentee, pk=post_pk)
    if request.method == "POST":
        form = Bid_By_MentorForm(request.POST, request,FILES)
        if form.is_valid():
            bid_by_mentor = form.save(commit=False)
            bid_by_mentor.author = request.user
            bid_by_mentor.save()
            messages.success(request, '멘토링 지원이 완료되었습니다.')
            return redirect(bid_by_mentor)
    else:
        form = Bid_By_MentorForm()
    return render(request, 'mentoring/bid_by_mentor_form.html', {
        'form' : form,
    })

@login_required
def bid_by_mentor_edit(request, post_pk, pk):
    post_by_mentee = get_object_or_404(Post_By_Mentee, pk=post_pk)
    bid_by_mentor = get_object_or_404(Bid_By_Mentor, pk=pk)
    if request.method == "POST":
        form = Bid_By_MentorForm(request.POST, request,FILES, instance=bid_by_mentor)
        if form.is_valid():
            bid_by_mentor = form.save(commit=False)
            bid_by_mentor.author = request.user
            bid_by_mentor.save()
            messages.success(request, '수정이 완료되었습니다.')
            return redirect(bid_by_mentor)
    else:
        form = Bid_By_MentorForm()
    return render(request, 'mentoring/bid_by_mentor_detail.html', {
        'form' : form,
    })

@login_required
def bid_by_mentor_delete(request, post_pk, pk):
    post_by_mentee = get_object_or_404(Post_By_Mentee, pk=post_pk)
    bid_by_mentor = get_object_or_404(Bid_By_Mentor, pk=pk)
    if request.user != bid_by_mentor.author:
        messages.error(request, "자신이 작성한 멘토링 신청서만 삭제할 수 있습니다.")
        return redirect(bid_by_mentor)
    bid_by_mentor.delete()
    messages.error(request, "멘토링 신청서가 삭제되었습니다.")
    return redirect(post_by_mentee)


def matched_bid_by_mentor(request, post_pk, pk):
    bid_by_mentor = get_object_or_404(Bid_By_Mentor, pk=pk)
    Matched_Bid_By_Mentor.objects.create(bid=bid_by_mentor, mentor=bid_by_mentor.author.profile.name, mentee=bid_by_mentor.post_by_mentee.author.profile.name,
        price=bid_by_mentor.post_by_mentee.price)
    return redirect("/")

@login_required
def comment_new(request, post_pk):
    post = get_object_or_404(Post_By_Mentor, pk=post_pk)
    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, '새로운 댓글이 등록되었습니다.')
            return redirect(post)
    else:
        form = CommentForm()
    return render(request, 'mentoring/comment_form.html', {
        'form' : form,
    })

@login_required
def comment_edit(request, post_pk, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES, instance=comment)
        if form.is_valid:
            comment = form.save(commit=False)
            comment.post = get_object_or_404(Post_By_Mentor, pk=post_pk)
            comment.author = request.user
            comment.save()
            messages.success(request, '댓글 내용이 수정되었습니다.')
            return redirect(comment.post)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'mentoring/comment_form.html', {
        'form' : form,
        })

@login_required
def comment_delete(request, post_pk, pk):
    post = get_object_or_404(Post_By_Mentor, pk=post_pk)
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.author:
        messages.error(request, "자신이 작성한 댓글만 삭제할 수 있습니다.")
        return redirect(post)
    comment.delete()
    messages.error(request, "해당 댓글이 삭제되었습니다.")
    return redirect(post)

