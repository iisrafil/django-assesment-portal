from django.contrib import messages
from django.shortcuts import render, redirect

from announcement.forms import AnnouncementForm
from announcement.models import Announcement


def announcements(request):
    content = Announcement.objects.all().order_by('-id')

    context = {
        'contents': content,
    }
    return render(request, 'announcement/announcement.html', context)


def view(request, pk):
    content = Announcement.objects.get(pk=pk)

    context = {
        'content': content,
    }
    return render(request, 'announcement/view.html', context)


def createAnnouncement(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            messages.success(request, f'Your announcement has been created successfully !')
            return redirect("announcements")
    else:
        form = AnnouncementForm()

    context = {
        'form': form,
    }
    return render(request, 'announcement/forms.html', context)
