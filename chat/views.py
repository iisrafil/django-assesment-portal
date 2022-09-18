from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import ChatGrant

from dashboard.models import Courses
from .models import Room

fake = Faker()


@login_required
def all_rooms(request):
    if request.user.profile.is_student:
        courses = request.user.profile.courseenrolled_set.all()

        rooms = Room.objects.filter(slug__in=courses.values_list('Course', flat=True))
    else:
        courses = request.user.profile.teacher.courses_set.all()
        rooms = Room.objects.filter(slug__in=courses.values_list('Enroll_key', flat=True))

    return render(request, 'chat/index.html', {'rooms': rooms})

@login_required
def room_detail(request, slug):
    room = Room.objects.get(slug=slug)
    return render(request, 'chat/room_detail.html', {'room': room})


def token(request):
    #identity = request.GET.get('identity', fake.user_name())
    identity = request.user.username
    device_id = request.GET.get('device', 'default')  # unique device ID

    account_sid = settings.TWILIO_ACCOUNT_SID
    api_key = settings.TWILIO_API_KEY
    api_secret = settings.TWILIO_API_SECRET
    chat_service_sid = settings.TWILIO_CHAT_SERVICE_SID

    token = AccessToken(account_sid, api_key, api_secret, identity=identity)

    # Create a unique endpoint ID for the device
    endpoint = "MiniSlackChat:{0}:{1}".format(identity, device_id)

    if chat_service_sid:
        chat_grant = ChatGrant(endpoint_id=endpoint,
                               service_sid=chat_service_sid)
        token.add_grant(chat_grant)

    response = {
        'identity': identity,
        'token': token.to_jwt().decode('utf-8')
    }

    return JsonResponse(response)