from django.shortcuts import render
from django.http import JsonResponse
from.models import ChatContent, ChatTopic
from aistudybuddy.aihelpers import buddybot


def index(request):
  return render(request, "index.html")


def chatbuddy(request):
  if request.user.is_authenticated:

    user = request.user
    titleHistory = ChatTopic.objects.filter(user=request.user).order_by("created_at").reverse()
    topic = None
    Allmessages = []

    idTopic = request.GET.get("topic")
    if idTopic:
      topic = ChatTopic.objects.get(id=idTopic, user=user)
      Allmessages = ChatContent.objects.filter(topic=topic)

    if request.method == "POST":
      userMessage = request.POST.get("message")
      idTopic = request.POST.get("idTopic")
      if not userMessage:
        return render(request, "Chat/chatbuddy.html", {
          "chatHistory": Allmessages,
          "titleHistory": titleHistory,
          "currenttopic": topic,
          "error": "Please enter a message."
        })

      # Find or create new topic
      if idTopic:
        topic = ChatTopic.objects.get(id=idTopic, user=user)
      else:
        # Auto generate new topic
        newtitle = userMessage[:68]
        topic = ChatTopic.objects.create(user=user, name=newtitle)

      #Save messages
      chat = ChatContent.objects.create(
        user = user,
        topic = topic,
        message = userMessage,
        response = ""
      )

      # AI buddybot reply
      system_prompt = "Buddybot, you are my best AI assistant."
      aiResponse = buddybot(system_prompt,userMessage)

      chat.response = aiResponse
      chat.save()

      Allmessages = ChatContent.objects.filter(topic=topic)
    return render(request, "Chat/chatbuddy.html", {
      "chatHistory": Allmessages,
      "titleHistory": titleHistory,
      "currenttopic": topic,
    })
  else: 
    return render(request,"Chat/chatbuddy.html")
