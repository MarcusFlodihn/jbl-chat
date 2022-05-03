import json

from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


from . import models


@require_http_methods(["GET"])
def users(request):
    all_users = models.User.objects.all()
    return JsonResponse({"users": [user.to_json() for user in all_users]})


@require_http_methods(["GET"])
def conversation(request, user_id: int):
    receiver_id = request.GET.get("receiver_id")
    if not receiver_id:
        return HttpResponseBadRequest(content="missing query parameter 'recipient_id'")
    get_object_or_404(models.User, pk=receiver_id)
    get_object_or_404(models.User, pk=user_id)
    messages = models.Message.objects.filter(sender_id=user_id, receiver_id=receiver_id).order_by('created_at')
    return JsonResponse({"messages": [m.to_json() for m in messages]})


@csrf_exempt
@require_http_methods(["POST"])
def message(request, user_id: int):
    sender = get_object_or_404(models.User, pk=user_id)
    receiver_id = request.GET.get("receiver_id")
    if not receiver_id:
        return HttpResponseBadRequest(content="missing query parameter 'recipient_id'")
    receiver = get_object_or_404(models.User, pk=receiver_id)
    payload = json.loads(request.body)
    content = payload.get("content")
    if not content or len(content) > 255:
        return HttpResponseBadRequest(content="Content of message was missing or greater than 255 characters!")
    m = models.Message(content=content, receiver=receiver, sender=sender)
    m.save()
    return JsonResponse({"message": f"Successfully sent '{m.content}' to '{receiver.username}'"})
