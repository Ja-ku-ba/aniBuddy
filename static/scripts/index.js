// set chat view at the bottom
var messageBody = document.getElementById('chat');
messageBody.scrollTop = messageBody.scrollHeight - messageBody.clientHeight;

// when enter is preesed in chat textare, send message
var chatTextarea = document.getElementById('id_message')
chatTextarea.addEventListener("keypress",function(e){
  if(e.keyCode == 13){
  document.getElementById("js-chat-textarea-button").click();
  }
});
