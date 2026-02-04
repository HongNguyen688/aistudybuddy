from django.shortcuts import render, redirect
from aistudybuddy.aihelpers import buddybot, extractfilePDF
from .models import CardTopic, FlashCard


# Create your views here.
def index(request):
  return render(request, "index.html")

def flashcards(request):
  if request.user.is_authenticated:

    flashcards = []
    error = ""
    username = request.user
    topics = CardTopic.objects.filter(user=username).order_by("created_at").reverse()

    idTopic = request.GET.get("topic")

    if idTopic:
      topic = CardTopic.objects.get(id=idTopic, user=username)
      flashcards = FlashCard.objects.filter(topic=topic)

    if request.method == "POST":
      uploadedFile = request.FILES.get("fileupload")
      numberCards = request.POST.get("numbercards")
      numberCards = int(numberCards)
      if numberCards < 1 or numberCards > 50:
        error = "Number of quizzes must between 1 and 50."
        numberCards = None

      #  Extract text and AI generate flash cards depend on numberCards
      if uploadedFile and uploadedFile.name.endswith(".pdf"):
        pdfText = extractfilePDF(uploadedFile)
        
        if pdfText:
          estismateTokens = len(pdfText) / 4
          maxTokens = 16000

          if estismateTokens > maxTokens:
           return render(request, "Flashcards/flashcards.html", {
            "cardtopics": topics,
            "flashcards": flashcards,
            "error": "Your PDF is too long. Please upload a shorter PDF with fewer than ~64,000 characters."
           })
          system_prompt = (
            f" Generate {numberCards} flashcards based on the uploaded pdf document, where {numberCards} is chosen by the user(must be between 1 and 50). For each flashcard must: be short and easy to understand, follow this format: key phrase | definition. Ensure none of the key phrases or definitions contain the '|' symbol. Prioritize full coverage of the input while keeping flashcards concise and focused."
          )

          aiResponse = buddybot(system_prompt, pdfText)

          allLines = aiResponse.splitlines()

          #Create a new card topic automatically
          firstline = None
          for line in allLines:
            if "|" in line:
              firstline = line
              break

          if firstline:
            title = firstline.split("|", 1)[0].strip()
            if title.lower().startswith("key phrase:"):
              newTitle = title[len("key phrase:"):].strip()
            else:
              newTitle = title.strip()
          else:
            newTitle = "None Topic"

          topic = CardTopic.objects.create(
              user=username, 
              name=newTitle
            )
          request.session["idCardtopic"] = topic.id

          #split the AI output into separate lines and save Flashcards
          flashcardLines = []
          for line in allLines:
            # The "|" symbol separates the flashcard Q & A
            if "|" in line: 
              parts = line.split("|", 1) #split into two parts at the first "|"
              question=parts[0].strip()
              answer=parts[1].strip()

              if question.lower().startswith("key phrase:"):
                question = question[len("key phrase:"):].strip()
              
              flashcardLines.append({
                "question": question,
                "answer": answer
              })

              FlashCard.objects.create(
                topic = topic,
                question=question,
                answer=answer
              )

          request.session["waitingCards"] = flashcardLines
          flashcards = flashcardLines
          topics = CardTopic.objects.filter(user=username).order_by("created_at").reverse()

        else:
          error = "Can not extract text from the PDF file."
      else:
        error = " The upload file must be a valid PDF."

      return render(request, "Flashcards/flashcards.html", {
        "cardtopics": topics,
        "flashcards": flashcards,
        "error": error 
        })
    else:
      return render(request, "Flashcards/flashcards.html", {
        "cardtopics": topics,
        "flashcards": flashcards
      })
  else:
    return render(request, "Flashcards/flashcards.html", {
      "error":"You must be logged in to generate flashcards. If you do not have an account, feel free to register.",
      "cardtopics": topics
    })


def learncards(request):
  if request.user.is_authenticated: 
    learnflashcards = []
    topic = None
    username = request.user
    idTopic = request.GET.get("topic")
    if idTopic:
      topic = CardTopic.objects.get(id=idTopic, user=username)
      learnflashcards = FlashCard.objects.filter(topic=topic)
    else: 
      learnflashcards = request.session.get("waitingCards", [])
  return render(request, "Flashcards/learncards.html",{
    "topic": topic,
    "flashcards": learnflashcards
  })