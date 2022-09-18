from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from dashboard.models import Courses
from quiz.forms import QuizForm, QuestionForm, AnswerFormset, TakeQuizForm
from quiz.models import Answer, Quiz, Question, QuizTaker, UsersAnswer


@login_required
def add_quiz(request, Enroll_key):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        course = get_object_or_404(Courses, Enroll_key=Enroll_key)
        form.instance.course = course
        if form.is_valid():
            quiz = form.save()
            messages.success(request, f'Your Quiz has been created successfully !')
            return redirect('add-question', quiz.id)
    else:
        form = QuizForm()
    return render(request, 'quiz/quiz_form.html', {'form': form,'Course_code': Enroll_key})

@login_required
def add_question(request, quiz_id):
    template_name = 'quiz/question_form.html'
    if request.method == 'GET':
        bookform = QuestionForm(request.GET or None)
        formset = AnswerFormset(queryset=Answer.objects.none())
    elif request.method == 'POST':
        bookform = QuestionForm(request.POST)
        formset = AnswerFormset(request.POST)
        if bookform.is_valid() and formset.is_valid():
            # first save this book, as its reference will be used in `Author`
            quiz = get_object_or_404(Quiz, id=quiz_id)
            bookform.instance.quiz = quiz
            book = bookform.save()
            for form in formset:
                # so that `book` instance can be attached.
                author = form.save(commit=False)
                author.question = book
                author.save()
            messages.success(request, f'Your question has been created successfully !')
            return redirect('add-question', quiz.id)
        else:
            messages.warning(request, f'Mark at least one answer as correct!')
    return render(request, template_name, {'bookform': bookform, 'formset': formset, 'quiz_id': quiz_id})

@login_required
def update_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.question_set.all()
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        course = get_object_or_404(Courses, Enroll_key=quiz.course.Enroll_key)
        form.instance.course = course
        if form.is_valid():
            quiz = form.save()
            messages.success(request, f'Your Quiz has been Updated successfully !')
            return redirect('course-detail', quiz.course.Enroll_key)
    else:
        form = QuizForm(instance=quiz)
    return render(request, 'quiz/quiz_update_form.html', {'form': form, 'Course_code': quiz.course.Course_code,'questions': questions,'quiz_id': quiz_id})


def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    quiz = question.quiz.id
    question.delete()
    return redirect('update-quiz', quiz)


# @login_required
# def update_question(request, question_id):
#     template_name = 'quiz/question_form.html'
#     question = get_object_or_404(Question, id=question_id)
#     quiz_id = question.quiz.id
#     if request.method == 'GET':
#         bookform = QuestionForm(instance=question)
#         formset = AnswerFormset(queryset=question.answer_set.all())
#     elif request.method == 'POST':
#         bookform = QuestionForm(request.POST, instance=question)
#         formset = AnswerFormset(request.POST, queryset=question.answer_set.all())
#         if bookform.is_valid() and formset.is_valid():
#             # first save this book, as its reference will be used in `Author`
#             quiz = get_object_or_404(Quiz, id=quiz_id)
#             bookform.instance.quiz = quiz
#             book = bookform.save()
#             for form in formset:
#                 # so that `book` instance can be attached.
#                 author = form.save(commit=False)
#                 author.question = book
#                 author.save()
#             messages.success(request, f'Your question has been created successfully !')
#             return redirect('update-quiz', quiz_id)
#     return render(request, template_name, {'bookform': bookform, 'formset': formset, 'quiz_id': quiz_id})
#

def delete_quiz(request, question_id):
    quiz = get_object_or_404(Quiz, id=question_id)
    quiz.delete()
    messages.ERROR(request, f'Your quiz has been deleted successfully !')


def take_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    student = request.user.profile

    if student.quiztaker_set.filter(quiz=quiz).exists():
        messages.warning(request, f'You have already taken this quiz successfully !')
        return redirect('course-detail', quiz.course.Enroll_key)

    total_questions = quiz.question_set.count()
    unanswered_questions = quiz.question_set.all()
    paginator = Paginator(unanswered_questions, 1)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    for un_question in page_obj:
        question = un_question

    if request.method == 'POST':
        form = TakeQuizForm(question=question, data=request.POST)
        if UsersAnswer.objects.filter(student=student, question=question).exists():
            messages.warning(request, f'you have already answered this question, you can change your ans on review')
        else:
            if form.is_valid():
                with transaction.atomic():
                    users_answer = form.save(commit=False)
                    users_answer.student = student
                    users_answer.question=question
                    users_answer.save()
                    messages.success(request, f'Your answer has been submitted successfully !')
                    return redirect('attempt-quiz', pk)

    else:
        form = TakeQuizForm(question=question)

    return render(request, 'quiz/take_quiz_form.html', {
        'quiz': quiz,
        'question': question,
        'form': form,
        'page_obj': page_obj,
    })


def review_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    student = request.user.profile
    questions = quiz.question_set.all()
    answer = UsersAnswer.objects.filter(student=student, question__in=questions)
    answered_question_id = UsersAnswer.objects.filter(student=student, question__in=questions).values_list('question_id',flat=True)
    question = quiz.question_set.exclude(id__in=answered_question_id)

    return render(request, 'quiz/review_quiz.html', {
        'quiz': quiz,
        'question': question,
        'answers': answer,
    })


def edit_ans(request, pk):
    question = get_object_or_404(Question, pk=pk)
    quiz = question.quiz
    student = request.user.profile
    answer = UsersAnswer.objects.filter(student=student, question=question).first()
    if student.quiztaker_set.filter(quiz=quiz).exists():
        messages.warning(request, f'You have already taken this quiz successfully !')
        return redirect('course-detail', quiz.course.Enroll_key)

    if request.method == 'POST':
        form = TakeQuizForm(question=question, data=request.POST, instance=answer)

        if form.is_valid():
            with transaction.atomic():
                users_answer = form.save(commit=False)
                users_answer.student = student
                users_answer.question = question
                users_answer.save()
                messages.success(request, f'Your answer has been submitted successfully !')
                return redirect('review-quiz', quiz.pk)

    else:
        form = TakeQuizForm(question=question, instance=answer)

    return render(request, 'quiz/edit_ans_form.html', {
        'quiz': quiz,
        'question': question,
        'form': form,
    })


def finis_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    student = request.user.profile
    questions = quiz.question_set.all()
    total_questions = questions.count()

    correct_answers = student.usersanswer_set.filter(answer__question__quiz=quiz, answer__is_correct=True).count()
    score = round((correct_answers / total_questions) * 100.0, 2)
    QuizTaker.objects.create(user=student, quiz=quiz, score=score)
    if score < 50.0:
        messages.warning(request, 'Better luck next time! Your score for the quiz %s was %s.' % (quiz.name, score))
    else:
        messages.success(request, 'Congratulations! You completed the quiz %s with success! You scored %s points.' % (quiz.name, score))
    return redirect('dashboard-home')


def quiz_result(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    result = quiz.quiztaker_set.all()
    return render(request, 'quiz/quiz_result.html', {
        'quiz': quiz,
        'result': result
    })