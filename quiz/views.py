from django.shortcuts import render, redirect
from aistudybuddy.aihelpers import buddybot, extractfilePDF
from .models import QuizTopic, QuizContent

# Create your views here.
def index(request):
  return render(request, 'index.html')

def quizzes(request):

  if request.user.is_authenticated:
    username = request.user
    allquizzes = []
    error = ""
    alltopics = QuizTopic.objects.filter(user=username).order_by("created_at").reverse()

    topic = None
    idTopic =  request.GET.get("topic")
    if idTopic:
      topic = QuizTopic.objects.get(id=idTopic, user=username) 
      allquizzes = QuizContent.objects.filter(topic=topic).order_by('order')

    if request.method == 'POST':
      uploadedFile = request.FILES.get("fileupload")
      numberQuizzes = request.POST.get("numberquizzes")
      numberQuizzes = int(numberQuizzes)
      if numberQuizzes < 1 or numberQuizzes > 50:
        error = "Number of quizzes must between 1 and 50."
        numberQuizzes = None

      if uploadedFile and uploadedFile.name.endswith(".pdf"):
        pdfText = extractfilePDF(uploadedFile)

        if pdfText:
          estismateTokens = len(pdfText) / 4
          maxTokens = 16000

          if estismateTokens > maxTokens:
           return render(request, 'Quiz/quiz.html', {
            "topics": alltopics,
            "allquizzes": allquizzes,
            "error": "Your PDF is too long. Please upload a shorter PDF with fewer than ~64,000 characters."
           })
        
          system_prompt = (
            f" Generate {numberQuizzes} multiple choice quiz questions based on the content of the uploaded PDF file. The number of quizzes {numberQuizzes} is provided by the user(between 1 and 50). Each quiz must be clear and relevant to the PDF's content, test the user's understanding. Format quiz output exactly like this: \nQ: [Question text]\n1) [Choice 1] \n2) [Choice 2] \n3) [Choice 3] \n4) [Choice 4] \nAnswer: [number]. Make sure each question must have exactly 4 answer choices and mark the correct answer clearly example 'Answer:'[1]. Don't repeat any questions or answers. Important, ensure quizzes are informative and base strictly on the document."
          )

          aiRespone = buddybot(system_prompt, pdfText)
          #print("AI Response:\n", aiRespone)
          alllines = aiRespone.splitlines()

          #Empty list to store all(question, answerChoices, correctAnswer)
          question_answers =[]
          question = None
          answerChoices = []
          correctAnswer = None
    
          for line in alllines:
            if line.startswith(('Question:', 'Q:')):
              # Save the previous question
              if question:
                question_answers.append((question, answerChoices, correctAnswer))
                answerChoices = [] #Reset choices for the new question

              #Remove 'question:' and save the question text
              if line.startswith("Question:"):
                prefixLen = len("Question:")
                questionText = line[prefixLen:]
                question = questionText.strip()
              elif line.startswith("Q:"):
                question = line[2:].strip()
              correctAnswer = None

            elif line.startswith(('1)','2)','3)','4)')):
              position = line.index(')')
              afterbracket = line[position + 1:]
              answertext = afterbracket.strip()
              answerChoices.append(answertext)

            elif line.startswith('Answer:'):
              parts = line.split(':', 1)
              correctAnswer = int(parts[1].strip())
    

          #Save the last question because after for loop no new 'Question:' arrives  
          if question:
            question_answers.append((question, answerChoices, correctAnswer))

          #Create a new quiz topic automatically
          if question_answers and question_answers[0][0]:
            newTitle = question_answers[0][0][:100]
          else:
            newTitle = "None Topic"

          topic = QuizTopic.objects.create(
            user = username,
            name=newTitle
          )
          request.session["idQuiztopic"] = topic.id

          #print("All Question Answers ", question_answers)
          questionNumber = 1
          for question in question_answers:
            questiontext = question[0]
            answerchoices = question[1]
            correctanswer = question[2]

            print(f"Saving question in Database {questionNumber}. {questiontext}")
            if len(answerchoices) != 4 or not correctanswer:
             # print(f"Skip question: {questiontext}")
             # print(f"Answer choice: {answerchoices}, Correct answer: {correctanswer} ")
              continue
              
            
            QuizContent.objects.create(
              question=questiontext,
              answer1=answerchoices[0],
              answer2=answerchoices[1],
              answer3=answerchoices[2],
              answer4=answerchoices[3],
              correct_answer=correctanswer,
              order=questionNumber,
              topic=topic
            )
            questionNumber += 1
          allquizzes = QuizContent.objects.filter(topic=topic).order_by("order")

          request.session["waitingQuizzes"] = question_answers
          alltopics = QuizTopic.objects.filter(user=username).order_by("created_at").reverse()
          
        else:
          error = "Can not extract text from the PDF file."
      else:
        error = " The upload file must be a valid PDF."
    
    return render(request, 'Quiz/quiz.html', {
        "topics": alltopics,
        "allquizzes": allquizzes,
        "error": error
      })
  else:
    return render(request, 'Quiz/quiz.html', {
      "error":"You must be logged in to generate Quiz. If you do not have an account, feel free to register.",
      "topics": [],
      "allquizzes":[]
    })

def takequizzes(request):
  if request.user.is_authenticated:
    topic = None
    allquizzes = []
    username = request.user
    idTopic = request.GET.get("topic")
    if idTopic:
      topic = QuizTopic.objects.get(id=idTopic, user=username)
      allquizzes = QuizContent.objects.filter(topic=topic).order_by("order")
    else: 
      allquizzes = request.session.get("waitingQuizzes", [])
    return render(request, "Quiz/takequiz.html", {
      "topic": topic,
      "allquizzes": allquizzes
    })
  else:
    return render(request, 'Quiz/quiz.html', {
      "error":"You must be logged in to generate Quiz. If you do not have an account, feel free to register.",
    })