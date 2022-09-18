from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from dashboard.models import Courses
from .forms import PostCreateForm
from django.contrib import messages
from .models import post


@login_required
def add_post(request, Enroll_key):
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        course = get_object_or_404(Courses, Enroll_key=Enroll_key)

        if form.is_valid():
            post = form.save(commit=False)
            post.course = course
            post.save()
            messages.success(request, f'Your post has been created successfully !')
            return redirect('course-detail', Enroll_key)
    else:
        form = PostCreateForm()
    return render(request, 'posts/post_form.html', {'form': form})

@login_required
def delete_post(request, post_id):
    Post = get_object_or_404(post, id=post_id)
    course = Post.course.Enroll_key
    Post.delete()
    messages.danger(request, f'Your post has been deleted successfully !')
    return redirect('course-detail', course)


@login_required
def update_post(request, post_id):
    Post = get_object_or_404(post, id=post_id)
    course = Post.course.Enroll_key
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES, instance=Post)
        form.instance.attachment = request.FILES
        if form.is_valid():
            form.save()
            messages.success(request, f'Your post has been created successfully !')
            return redirect('course-detail', course)
    else:
        form = PostCreateForm(instance=Post)
    return render(request, 'posts/post_form.html', {'form': form})