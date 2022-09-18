from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.datetime_safe import datetime
from django.views.generic import CreateView

from chat.models import Room
from .forms import CourseForm
from .models import Courses, CourseEnrolled
from django.contrib import messages


@login_required
def dashboard(request):
    if request.method == 'POST':
        query = request.POST.get('key')
        try:
            course = Courses.objects.get(Enroll_key=query)
            try:
                course.courseenrolled.Students.add(request.user.profile)
            except ObjectDoesNotExist:
                CourseEnrolled.objects.create(Course=course)
                course.courseenrolled.Students.add(request.user.profile)
        except Courses.DoesNotExist:
            messages.warning(request, f'Course Not Found')

    if request.user.profile.is_student:
        context = {
            'courses': request.user.profile.courseenrolled_set.all()
        }
    else:
        context = {
            'courses': request.user.profile.teacher.courses_set.all()
        }
    return render(request, 'dashboard/home.html', context)


@login_required
def CourseDetailView(request, Enroll_key):
    course = get_object_or_404(Courses, Enroll_key=Enroll_key)
    posts = course.post_set.all().order_by('-date_posted')
    if request.user.profile.is_student:
        assignments = course.assignment_set.filter(last_date_of_submission__gte=datetime.now())
    else:
        assignments = course.assignment_set.all()
    if request.user.profile.is_student:
        quiz = course.quiz_set.filter(Make_Public=True)
    else:
        quiz = course.quiz_set.all()
    context = {
        'posts': posts,
        'assignments': assignments,
        'quiz': quiz,
        'Enroll_key': course.Enroll_key,
        'course': course.Title
    }
    return render(request, 'dashboard/detail.html', context)


def home(request):
    return render(request, 'landing/index.html', )

@login_required
def about(request):

    return render(request, 'dashboard/about.html', )


# class add_course(LoginRequiredMixin, CreateView):
#     model = Courses
#     fields = ['Title', 'Course_code', 'Enroll_key']
#
#     def form_valid(self, form):
#         form.instance.Teacher = self.request.user.profile.teacher
#         return super().form_valid(form)


@login_required
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)

        if form.is_valid():
            course = form.save(commit=False)
            course.Teacher = request.user.profile.teacher
            course.save()
            chat = Room(name=course.Title, slug=course.Enroll_key)
            chat.save()
            messages.success(request, f'Your Course has been created successfully !')
            return redirect('dashboard-home')
    else:
        form = CourseForm()
    return render(request, 'dashboard/courses_form.html', {'form': form})
