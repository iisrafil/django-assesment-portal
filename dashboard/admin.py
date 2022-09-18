from django.contrib import admin
from .models import Courses, Teacher, CourseEnrolled

# Register your models here.
admin.site.register(Courses)
admin.site.register(Teacher)
admin.site.register(CourseEnrolled)
