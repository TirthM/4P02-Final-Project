userMsgStyleStart = "<div class='user-bubble round'> ";
botMsgStyleStart = "<div class='bot-bubble border round'>";
msgEnd = "</div>";
var msgLock = false;
function printResponse() {
	
	var messageBody = document.querySelector('.message_holder');
	var imsg = $('#msg').val();
	document.getElementById('msg').value = ''

	if (imsg && msgLock == false) {
		msgLock = true
		var user = userMsgStyleStart + imsg + msgEnd;
		$('div.message_holder').append("<div class='userTextTitle'><b>You</b></div>");
		$('div.message_holder').append(user);

		
		$('div.message_holder').append("<div class='chatbotTextTitle'><b>Chatbot</b></div>");
		$('div.message_holder').append(botMsgStyleStart + "Hold on Im thinking..." + msgEnd);

		messageBody.scrollTop = messageBody.scrollHeight - messageBody.clientHeight;
		$.ajax({
			url: "/join",
			type: "POST",
			data: { msg: imsg }
		}).done(function (response) {

			message = response.result;

			$('div.message_holder').children().last().remove();
			$('div.message_holder').children().last().remove();

			if (message.inputType == "question") {

				respText = urlify(message.response);

				var bot = botMsgStyleStart + respText + msgEnd;
				$('div.message_holder').append("<div class='chatbotTextTitle'><b>Chatbot</b></div>");
				$('div.message_holder').append(bot);

				messageBody.scrollTop = messageBody.scrollHeight - messageBody.clientHeight;
				msgLock = false
			}
			else if (message.inputType == "command") {
				
				var bot = botMsgStyleStart;
				
				switch (message.response) {
					case "chatlogs":
						userLogs = message.userschatLogs
						responseLogs = message.responseschatLogs						
						for (var i = 0; i < userLogs.length; i++) {
							respText = urlify(responseLogs[i]);
							u = userMsgStyleStart + userLogs[i] + msgEnd;
							b = botMsgStyleStart + respText + msgEnd;
							$('div.message_holder').append("<div class='userTextTitle'><b>You</b></div>");
							$('div.message_holder').append(u);
							$('div.message_holder').append("<div class='chatbotTextTitle'><b>Chatbot</b></div>");
							$('div.message_holder').append(b);

						}
						msgLock = false
						break;
					case "clearlogs":
						$("div.message_holder *").remove();
						$('div.message_holder').append("<div class='userTextTitle'><b>You</b></div>");
						$('div.message_holder').append(user);
						msgLock = false
						break;
					case "Invalid Command":
						bot += message.response + msgEnd;
						$('div.message_holder').append("<div class='chatbotTextTitle'><b>Chatbot</b></div>");
						$('div.message_holder').append(bot);
						msgLock = false
						break;
					case "endsession":
						bot += "The Session has ended. Thanks I enjoyed talking with you. <button onclick='returnToMenu()'>Restart</button>" + msgEnd;
						$('div.message_holder').append("<div class='chatbotTextTitle'><b>Chatbot</b></div>");
						$('div.message_holder').append(bot);
						break;
					case "insert":
						bot += "Successfully added question to the database" + msgEnd;
						$('div.message_holder').append("<div class='chatbotTextTitle'><b>Chatbot</b></div>");
						$('div.message_holder').append(bot);
						msgLock = false
						break;
					case "rating":
						bot += "Thanks for your rating, the average rating for me is " + message.rating + msgEnd;
						$('div.message_holder').append("<div class='chatbotTextTitle'><b>Chatbot</b></div>");
						$('div.message_holder').append(bot);
						msgLock = false
						break;
					case "helpPrompt":
						bot += "<b>Commands</b><br><b>!end</b>, ends the chat session and returns to menu.<br><b>!logs</b>, brings up any message questions onto the chat window from previously in the session.<br>" +
							"<b>!clear</b>, clears the screen of all chat bubbles.<br><b>!help</b>, brings you to here! <br><b>!insert</b>, inserts a question to a database that can be assess to implement into a response. ex '!insert is this how I use the insert command?'<br>" +
							"<b>!rate</b>, rate me on how well you think I am from 1-5 ex '!rate 5'"+
							"<br><b>How to use</b><br>Enter messages below and I will respond the best I can to answer questions you may have about Brock University. " +
							+ msgEnd;
						$('div.message_holder').append("<div class='chatbotTextTitle'><b>Chatbot</b></div>");
						$('div.message_holder').append(bot);
						msgLock = false
						break;
				}
				messageBody.scrollTop = messageBody.scrollHeight - messageBody.clientHeight;
				
			}
			else if (message.inputType == "TIMEOUT") {
				var bot = botMsgStyleStart;
				bot += "Sorry but the session has timed out click this button to return. <button onclick='returnToMenu()'>Restart</button>" + msgEnd;
				$('div.message_holder').append("<div class='chatbotTextTitle'><b>Chatbot</b></div>");
				$('div.message_holder').append(bot);
				messageBody.scrollTop = messageBody.scrollHeight - messageBody.clientHeight;
            }
		});
	}
};
function urlify(text) {
	var urlRegex = /(https?:\/\/[^\s]+)/g;
	return text.replace(urlRegex, function (url) {
		return '<a href="' + url + '">' + url + '</a>';
	})
};