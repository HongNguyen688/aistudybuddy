//Wait for the page to load
document.addEventListener("DOMContentLoaded", function () {
  const chatForm = document.getElementById("js_chatform");
  const inputMessage = document.getElementById("js_message");
  const chatBox = document.getElementById("js_chatmessages");

  if (chatForm && inputMessage) {
    chatForm.addEventListener("submit", function (event) {
      const messageValue = inputMessage.value.trim();
      if (!messageValue) {
        alert("Please type a message");
        event.preventDefault(); //stop the form from submitting
        return;
      }
    });
  }
  //scrolls to the latest message
  if (chatBox) {
    setTimeout(() => {
      chatBox.scrollTop = chatBox.scrollHeight;
    }, 50);
  }
});
