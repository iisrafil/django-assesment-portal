from django.urls import path

from PdfConverter.views import upload_pdf_image
from announcement.views import announcements, view, createAnnouncement
from assignment.views import add_Assignment, submit_assignment, assignment_submission, delete_assignment, \
    update_assignment
from quiz.views import add_quiz, add_question, update_quiz, delete_question, delete_quiz, take_quiz, review_quiz, \
    finis_quiz, edit_ans, quiz_result
from todo.views import task_list, create_task, mark
from . import views
from posts.views import add_post, delete_post, update_post

urlpatterns = [
    path('', views.dashboard, name='dashboard-home'),
    path('about/', views.about, name='dashboard-about'),
    #---------->
    path('course/new/', views.add_course, name='add-course'),
    path('course/<str:Enroll_key>/', views.CourseDetailView, name='course-detail'),
    #---------->
    path('<str:Enroll_key>/new-post/', add_post, name='add-post'),
    path('<str:post_id>/delete-post/', delete_post, name='delete-post'),
    path('<str:post_id>/update-post/', update_post, name='update-post'),
    #---------->
    path('<str:Enroll_key>/new-assignment/', add_Assignment, name='add-assignment'),
    path('assignment/<int:assignment_id>/submit', submit_assignment, name='assignment-submit'),
    path('assignment/<int:assignment_id>/submission', assignment_submission, name='assignment-submission'),
    path('<str:assignment_id>/delete-assignment/', delete_assignment, name='delete-assignment'),
    path('<str:assignment_id>/update-assignment/', update_assignment, name='update-assignment'),
    #---------->
    path('<str:Enroll_key>/new-quiz/', add_quiz, name='add-quiz'),
    path('<str:quiz_id>/add-question/', add_question, name='add-question'),
    path('<str:quiz_id>/update/', update_quiz, name='update-quiz'),
    path('<str:question_id>/question-delete/', delete_question, name='delete-question'),
    path('<str:quiz_id>/delete-quiz/', delete_quiz, name='delete-quiz'),
    path('<str:pk>/attempt-quiz/', take_quiz, name='attempt-quiz'),
    path('<str:pk>/review-quiz/', review_quiz, name='review-quiz'),
    path('<str:pk>/edit-ans/', edit_ans, name='edit-ans'),
    path('<str:pk>/finis-quiz/', finis_quiz, name='finis-quiz'),
    path('<str:pk>/quiz-result/', quiz_result, name='quiz-result'),
    #---------->
    path('convert/image-pdf', upload_pdf_image, name='pdf-convert'),
    #---------->
    path('announcement', announcements, name='announcements'),
    path('announcement/view/<str:pk>', view, name='view'),
    path('announcement/create', createAnnouncement, name='createAnnouncement'),
    #---------->
    path('todo', task_list, name='todo'),
    path('todo/create', create_task, name='create_task'),
    path('todo/change-status/<str:pk>', mark, name='mark'),
]

