from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from assignment.forms import AssignmentCreateForm, AssignmentAnsForm
from assignment.models import Assignment
from dashboard.models import Courses
from django.contrib import messages


# @login_required
# def AssignmentDetailView(request, assignment_id):
#     assignment = get_object_or_404(Assignment, id=assignment_id)
#     context = {
#         'assignment': assignment,
#     }
#     return render(request, 'assignment/assignment_detail.html', context)


@login_required
def add_Assignment(request, Enroll_key):
    if request.method == 'POST':
        form = AssignmentCreateForm(request.POST)
        course = get_object_or_404(Courses, Enroll_key=Enroll_key)

        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.course = course
            assignment.save()
            messages.success(request, f'Your assignment has been created successfully !')
            return redirect('course-detail', Enroll_key)
    else:
        form = AssignmentCreateForm()
    return render(request, 'assignment/assignment_form.html', {'form': form})


@login_required
def submit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    student = request.user.profile
    if student.assignmentans_set.filter(assignment=assignment).exists():
        messages.warning(request, f'You have already submitted this Assignment successfully !')
        return redirect('course-detail', assignment.course.Enroll_key)

    if request.method == 'POST':
        form = AssignmentAnsForm(request.POST, request.FILES)
        form.instance.assignment = assignment
        form.instance.submited_by = request.user.profile
        if form.is_valid():
            form.save()
            messages.success(request, f'Your assignment has been submitted successfully !')
            return redirect('course-detail', assignment.course.Enroll_key)
    else:
        form = AssignmentAnsForm()
    context = {
        'assignment': assignment,
        'form': form,
    }
    return render(request, 'assignment/assignment_submission_form.html', context)


@login_required
def assignment_submission(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    submissions = assignment.assignmentans_set.all()
    context = {
        'submissions': submissions,
        'assignment': assignment,
    }
    return render(request, 'assignment/assignment_submission.html', context)


@login_required
def delete_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    course = assignment.course.Enroll_key
    assignment.delete()
    messages.error(request, f'Your assignment has been deleted successfully !')
    return redirect('course-detail', course)


@login_required
def update_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    course = assignment.course.Enroll_key
    if request.method == 'POST':
        form = AssignmentCreateForm(request.POST, request.FILES, instance=assignment)
        form.instance.attachment = request.FILES
        if form.is_valid():
            form.save()
            messages.success(request, f'Your Assignment has been created successfully !')
            return redirect('course-detail', course)
    else:
        form = AssignmentCreateForm(instance=assignment)
    return render(request, 'posts/post_form.html', {'form': form})

