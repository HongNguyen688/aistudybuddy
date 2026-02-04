document.addEventListener("DOMContentLoaded", () => {
  //convert all flashcards into an array
  let cardElements = document.querySelectorAll(".js_flashcard");
  let cards = Array.from(cardElements);

  let currentCard = 0;
  let isFrontcard = true;

  //Store each card's question and answer
  cards.forEach(card => {
    const question = card.querySelector(".js_front").textContent.trim();
    const answer = card.querySelector(".js_back").textContent.trim();
    card.dataset.question = question;
    card.dataset.answer = answer;
  });

  function displayCard(indexCard) {
    cards.forEach((card, i) => {
      if (i === indexCard) {
        card.style.display = "block";
        card.textContent = cards[i].dataset.question;
      } else {
        card.style.display = "none";
      }
    });

    //Update number of card
    const recentCard = document.getElementById("js_currentCard");
    if (recentCard) { 
      recentCard.textContent = indexCard + 1;
    }
    isFrontcard = true;
  }

  function updateControlButton() {
    if (currentCard === 0) {
      prevBtn.style.display = 'none';
    } else {
      prevBtn.style.display = 'inline-block';
    }

    if (currentCard === cards.length - 1) {
      nextBtn.textContent = 'Finish';
    } else {
      nextBtn.textContent = 'Next';
    }

    cards.forEach((card, i) => {
      if (i === currentCard) {
        card.style.display = 'block';
        if (isFrontcard) {
          card.textContent = card.dataset.question;
        } else {
          card.textContent = card.dataset.answer;
        }  
      } else {
        card.style.display = 'none';
      }
      const recentCard = document.getElementById("js_currentCard");
      if (recentCard) { 
        recentCard.textContent = currentCard + 1;
      }
    });

  }

  //Flip card
  const flipbtn = document.getElementById("js_flipbtn");
  if (flipbtn) {
    flipbtn.addEventListener("click", () => {
      const card = cards[currentCard];
      if(isFrontcard) {
        card.textContent = card.dataset.answer;
      }
      else {
        card.textContent = card.dataset.question;
      }
      isFrontcard = !isFrontcard;
    });
  }

  //Previous card
  const prevBtn = document.getElementById("js_prevbtn");
  if (prevBtn) {
    prevBtn.addEventListener("click", () => {
      if (currentCard > 0) {
        currentCard --;
        //displayCard(currentCard);
        updateControlButton();
      }
    });
  }

  //Next card
  const nextBtn = document.getElementById("js_nextbtn");
  if (nextBtn) {
    nextBtn.addEventListener("click", () => {
      if (currentCard < cards.length - 1) {
        currentCard ++;
        //displayCard(currentCard);
        updateControlButton();
      } else {
        document.getElementById('js_message').textContent = 'Great Job! You are done to learn flash card'
        document.getElementById('js_doneButtons').style.display = 'block';
      }
    });
  }

  displayCard(currentCard);
  updateControlButton();
});