# AISTUDYBUDDY - My CS50W Final Project

**Welcome to AISTUDYBUDDY**

## Demo Video

[Here is my AISTUDYBUDDY video demo](https://youtu.be/I4vvnLFQfN0)



## What is AISTUDYBUDDY?

AISTUDYBUDDY is a web application I created for my CS50W final project. It helps students study better using AI. The app is built with Django (a Python tool) for the backend and JavaScript for the frontend. It uses OpenAI’s API to create study tools from PDF files uploaded by users. AISTUDYBUDDY does: **Chat Buddy**: Talk to Buddybot like a friend who helps you study. **Flashcards**: Upload a PDF, and the app makes 1 - 50 flashcards to study with. **Quizzes**: Upload a PDF, get a quiz with multiple-choice questions, and see your score. **Study History**: The app remembers your chats, flashcards, and quizzes base on their titles, then you can come back and learn anytime. The app is also **Mobile-Friendly**: It looks good and works well on your phone. Users must create an account to use all the features.



## Distinctiveness and Complexity

AISTUDYBUDDY is distinct from the other CS50W projects in both purpose and technical implementation. Unlike Project 1 (Wiki) a static wiki, AISTUDYBUDDY generates study materials using AI from PDFs. Project2 (E-commerce) focuses on transactions, AISTUDYBUDDY is educational, creating personalized study tools. Project 3 (Email) is an email system, AISTUDYBUDDY processes files to generate content like flashcards and quizzes. While Project 4 (Social Network) is a social media site, AISTUDYBUDDY centered around personalized AI-powered studying, not involving social interactions.

Most CS50w projects are about creating, reading, updating, and deleting user content like posts, emails, or orders. But my AISTUDYBUDDY is different. **AI integration** interacts with OpenAI's API to generate learning tools based on each PDF's content. **PDF data extraction** extracting and cleaning data from various PDF formats was challenging due to inconsistent formatting and structure. **Prompt Engineering** Custom prompts were carefully designed and tested to generate accurate, helpful topic title and content. **No Javascript Libraries** All (flashcard flipping, quiz scoring, chat scrolling) was built using plain JavaScript. No course project covered file parsing, prompt engineering, or OpenAI API integration. That makes this project unique and original.

What makes AISTUDYBUDDY complex is its integration of real-world AI capabilities with dynamic user inputs. The app allows users to upload a PDF and uses OpenAI's API to generate flashcards and quizzes —it must be clear and relevant to the PDF’s content. This required me to design and test complex prompt engineering strategies to ensure meaningful, accurate AI output.

Working with PDFs was another major technical challenge. I used PyMuPDF to extract and clean text from uploaded files. Since PDFs vary in structure and formatting, I had to write code that parsed them consistently and cleaned up unexpected issues like page breaks, headers, and non-text elements.

On the frontend, I chose not to use Bootstrap or any JavaScript libraries like jQuery. Instead, I built all interactivity, such as the flashcard flip functionality and automatic quiz scoring. This added complexity because I had to manage the DOM and event listeners directly without helper tools.

The application is also organized into three separate Django apps: chat, flashcards, and quizzes. Each app includes its own models, views, and templates. Managing this modular architecture, handling user authentication, saving user data, and maintaining consistent design across apps required careful planning and coordination.

And advanced frontend interactivity and hamburger menu without using any external frontend frameworks like Bootstrap.

Here’s why it was hard to build:
- **AI Stuff**: I used OpenAI’s API to make the chat, flashcards, and quizzes. I had to figure out how to write instructions (prompts) for the AI to give good answers.
- **PDF Uploads**: Users can upload PDFs, and I used a tool called PyMuPDF to read them. PDFs are tricky because they’re all different, so I had to clean up the text.
- **Lots of Features**: The app has three tools (chat, flashcards, quizzes) that work together, which was a lot to build.
- **No JavaScript Libraries**: I wrote all the interactive parts (like flipping flashcards) with plain JavaScript, not using tools like jQuery.
- **Django Models**: I made three Django apps and used models to save user data, like flashcards  and  quiz content.

This project used everything I learned in CS50W—HTML/CSS, Django, JavaScript, APIs, models, forms, and front-end logic — and added new stuff like AI and PDF handling, making it bigger than other projects.



## File Structure and Explanation

### accounts/
- **urls.py**: Routes URLs like `/login/` and `/register/` to the appropriate views.
- **views.py**: Contains views for user login and registration using Django forms.

### chat/
- **models.py**: Defines `ChatTopic` and `ChatContent` models for storing AI conversations per user.
- **urls.py**: Connects routes like `/chatbuddy/` to the chat interface.
- **views.py**: Handles user input, sends messages to the OpenAI API, and returns chat responses and saves chats based on it title.

### flashcards/
- **models.py**: Defines `CardTopic` and `Flashcard` models for storing sets of flashcards.
- **urls.py**: Routes related to flashcard generation and learning.
- **views.py**: Processes PDF uploads, sends the extracted text to OpenAI, and saves flashcards based on it title.

### quizzes/
- **models.py**: Defines `QuizTopic` and `QuizContent` models for storing quizzes and answers.
- **urls.py**: Routes for quiz generation and taking quizzes.
- **views.py**: Handles PDF uploads, generates quiz questions via OpenAI and saves quizzes based on it title.

### aistudybuddy/
- **aihelpers.py**: Contains utility functions `extractfilePDF()` for extracting text from PDFs using PyMuPDF and `buddybot()` interacting with the OpenAI API to generate flashcards and quizzes.
- **settings.py**: Django settings including OpenAI API configuration and app registration.

### templates/
- `layout.html`: Shared layout template used across all apps with responsive nav bar and footer.
- `index.html`: Home page for the platform with links to all features.
- `Accounts/login.html`: login form pages with form validation and error display.
- `Accounts/register.html`: registration form pages with form validation and error display.
- `Chat/chatbuddy.html`: Chat interface between user and Buddybot and Layout for showing chat history.
- `Flashcards/flashcards.html`: Upload PDF file and review flashcards generation interface and list title history.
- `Flashcards/learncards.html`: Flip-style study interface using Javascript and CSS.
- `Quizzes/quiz.html`: For Upload PDF file, creating and reviewing quizzes and list title history.
- `Quizzes/takequiz.html`: For taking quizzes with real-time Javascript logic. Quiz interface with answer selection and scoring.

### static/
- **CSS Files**: Includes `styles.css`,`account.css`,`chatbuddy.css`,`flashcard.css`, etc. that define the layout and mobile responsiveness of each section of the app.
- **chat.js**: Updates chats without refreshing and auto-scroll.
- **flashcard.js**: Flip animation for flashcards and navigation logic.
- **quiz.js**: Shows quiz questions with multiple choice answers and displays your score at the end.

### requirements.txt
- Lists all Python packages used: Django, openai, python-dotenv, PyMuPDF, etc.



## How to Run It

- Download my code and go to the project folder.
- Set up a virtual environment:
    *python3 -m venv venv*
    *source venv/bin/activate*
- Install the tools:
    *pip3 install -r requirements.txt*
- Add your OpenAI API key in a .env file:
    *OPENAI_API_KEY=your-openai-api-key-here*
- Start the app:
    *python3 manage.py migrate*
    *python3 manage.py runserver*
- Open http://127.0.0.1:8000/ in your browser.



## Features

- **Chat Buddy**: Talk to Buddybot and save your chats.
- **Flashcards**: Upload a PDF, get 1-50 flashcards, and flip them to study.
- **Quizzes**: Make a quiz from a PDF, answer questions, and see your score.
- **Study History**: The app saves your study stuff.
- **Mobile-Friendly**: Works on iPhones and Android phones.



## What Was Hard

- **AI Was Tricky**: I had to try lots of ways to ask OpenAI for good flashcards and quiz questions.
- **PDFs Were Messy**: Some PDFs had weird formatting, so I had to clean them up.
- **JavaScript Was Tough**: Making flashcards flip and quizzes score without libraries was hard but cool.
- **Big Project**: Organizing three apps and six models took a lot of planning.

I learned how to build a real app and use AI, PDF data extraction, pure Javascript, modular design which was new for me.



## Future Ideas

- Track quiz scores over time with a chart.
- Let users upload Word documents, not just PDFs.
- Add a tool to summarize content, highlight key sentences and bullet-point takeaways,export notes as PDFs into study notes.



## Additional Notes

- This project was built independently by me as part of the CS50W Capstone.
- I chose not to use external libraries like Bootstrap or jQuery to demonstrate full control over frontend interactivity.
- All AI functionality was handled through OpenAI's GPT-4 API using carefully designed prompt templates.
- Responsive design was done manually using CSS media queries.



## About Me

**Hong Nguyen** 
CS50’s Web Programming with Python and JavaScript – 2025
