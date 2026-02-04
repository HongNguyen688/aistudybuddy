document.addEventListener("DOMContentLoaded", () => {
  const currentquiz = document.getElementById("js_currentquiz");
  const userscore = document.getElementById("js_score");
  const quizzes = document.querySelectorAll(".js_quizzes");
  const total = quizzes.length;

  let recentquiz = 0;
  let score = 0;

  //show only current quiz and hide all others quizzes
  function displayQuiz(indexQuiz) {
    for (let j = 0; j < quizzes.length; j++) {
      let quiz = quizzes[j];
      if(j === indexQuiz) {
        quiz.style.display = "block";
      } else {
        quiz.style.display = "none";
      }
    }
    if(currentquiz) {
      currentquiz.innerText = indexQuiz + 1;
    }

    if ( recentquiz === 0) {
      previousBtn.style.display = 'none';
    } else {
      previousBtn.style.display = 'inline-block';
    }
  }
  
  //Select answer
  for (let j = 0; j < quizzes.length; j++) {
    let quiz = quizzes[j];

    let answerBtns = quiz.querySelectorAll(".js_answer button");
    for (let k = 0; k < answerBtns.length; k++) {
      let button = answerBtns[k];
      button.addEventListener("click", function() {
        let answered = quiz.classList.contains("answered");
        if (answered)
          return;
        quiz.classList.add("answered");

        for (let l = 0; l < answerBtns.length; l++) {
          answerBtns[l].classList.remove("selected");
        }
        button.classList.add("selected");
      

        const isCorrect = button.dataset.correct === "true";

        if (isCorrect) {
          button.innerHTML = "&#9989; " + button.innerText;
          button.classList.add("correct");
          score++;
          userscore.innerText = `Your score: ${score}`;
        } else {
          button.innerHTML = "&#10060; " + button.innerText;
          button.classList.add("incorrect");

          answerBtns.forEach(btn => {
            if (btn.dataset.correct === "true"){
              btn.innerHTML = "&#9989; " + btn.innerText;
              btn.classList.add("correct");
            }
          });
        }
    });
    }
  }

  function updateBtncontrol() {
    //Hide previous button
    if ( recentquiz === 0) {
      previousBtn.style.display = 'none';
    } else {
      previousBtn.style.display = 'inline-block';
    }

    if (recentquiz === total - 1) {
      nextBtn.textContent = 'Finish';
    } else {
      nextBtn.textContent = 'Next';
    }

    quizzes.forEach((quiz, i) => {
      if ( i === recentquiz) {
        quiz.style.display = 'block';
      } else {
        quiz.style.display = 'none';
      }
      currentquiz.innerText = recentquiz + 1;
    });
  }

  //Previous quiz
  const previousBtn = document.getElementById("js_previous");
  if (previousBtn) {
    previousBtn.addEventListener("click", () => {
      if (recentquiz > 0) {
        recentquiz --;
       // displayQuiz(recentquiz);
       updateBtncontrol();
      }
    });
  }

  //Next quiz
  const nextBtn = document.getElementById("js_next");
  if (nextBtn) {
    nextBtn.addEventListener("click", () => {
      if (recentquiz < total - 1) {
        recentquiz ++;
        updateBtncontrol();
      } else {
        document.getElementById('js_scoreMsg').textContent = `You are done. Your score is ${score} out of ${total}`;
        document.getElementById('js_doneBtns').style.display = 'block';
      }
    });
  }

  displayQuiz(recentquiz);
  updateBtncontrol();
})