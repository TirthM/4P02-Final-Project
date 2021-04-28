// JavaScript source code
function startSession() {
    var name = $('#username').val();
    var userEmail = $('#email').val();
    var chatDes = $('#chatname').val();
    console.log(name + " <-");
    if (name  && userEmail  && chatDes ) {
        $.ajax({
            url: "/startchat",
            type: "POST",
            data: {
                username: name,
                email: userEmail,
                seshName: chatDes
            }
        }).done(function (response) {
            startdata = response.startPackage
            $('div.message_holder').append("<div class='chatbotTextTitle'><b>Chatbot</b></div>");
            var botMsg = "<div class='bot-bubble border round'>Welcome ";
            botMsg += startdata.username + " to the Brock University Chatbot! I'm here to talk about " + startdata.chatTitle +
                " with you. Enter a question below about Brock University and I will answer it for you. Use !help to see the list of commands on how to use me. </div>";
            $('div.message_holder').append(botMsg);
        });
    }

}