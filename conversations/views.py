from time import sleep
from django.http import Http404
from django.shortcuts import redirect, reverse, render
from users import models as user_models
from django.views.generic import View
from . import models


# Create your views here.
def redirect_conversation(conversation):
    return redirect(reverse("conversations:detail", kwargs={"pk": conversation.pk}))


def go_conversation(request, a_pk, b_pk):
    try:
        user_one = user_models.User.objects.get(pk=a_pk)
    except user_models.User.DoesNotExist:
        user_one = None
    try:
        user_two = user_models.User.objects.get(pk=b_pk)
    except user_models.User.DoesNotExist:
        user_two = None
    if user_one is not None and user_two is not None:
        conversation = models.Conversation.objects.filter(participants=user_one).filter(
            participants=user_two
        )
        if conversation.count() == 0:
            conversation = models.Conversation.objects.create()
            conversation.participants.add(user_one, user_two)
            conversation = models.Conversation.objects.filter(
                participants=user_one
            ).filter(participants=user_two)
    return redirect(reverse("conversations:detail", kwargs={"pk": conversation[0].pk}))


class ConversationDetailView(View):
    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        conversation = models.Conversation.objects.get_or_none(pk=pk)
        if not conversation:
            raise Http404()
        return render(
            self.request,
            "conversations/conversation_detail.html",
            {"conversation": conversation},
        )

    def post(self, *args, **kwargs):
        message = self.request.POST.get("message", None)
        pk = kwargs.get("pk")
        conversation = models.Conversation.objects.get_or_none(pk=pk)
        if not conversation:
            raise Http404()
        if message is not None:
            models.Message.objects.create(
                message=message, user=self.request.user, conversation=conversation,
            )
        return redirect(reverse("conversations:detail", kwargs={"pk": pk}))

