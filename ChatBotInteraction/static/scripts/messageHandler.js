function printResponse() {
  var imsg = $('#msg').val();
  $.ajax({
	  url: "/join",
	  type: "POST",
	  data: { msg: imsg }
  }).done(function (response) {

	  message = response.result;

	  if (message.inputType == "question") {
		  var user = "<div><b style='color: #000'>You</b>   ";
		  var bot = "<div><b style='color: #000'>ChatBot</b>  ";
		  user += message.message + '</div>';
		  bot += message.response + '</div>';
		  $('h3').remove()
		  $('div.message_holder').append(user);
		  $('div.message_holder').append(bot);
	  }
	  else if (message.inputType == "command") {
		  var user = "<div><b style='color: #000'>You</b>   ";
		  var bot = "<div><b style='color: #000'>ChatBot</b>  ";
		  user += message.message + '</div>';
		  $('h3').remove()
		  switch (message.response) {
			  case "chatlogs":
				  userLogs = message.userschatLogs
				  responseLogs = message.responseschatLogs
				  
				  $('div.message_holder').append(user);
				  for (var i = 0; i < userLogs.length; i++){                            
					  u = "<div><b style='color: #000'>You</b>   " + userLogs[i] + "</div>"
					  b = "<div><b style='color: #000'>ChatBot</b>   " + responseLogs[i] + "</div>"
					  $('div.message_holder').append(u);
					  $('div.message_holder').append(b);
					  
				  }
				  break;
			  case "clearlogs":
				  $("div.message_holder *").remove();
				  $('div.message_holder').append(user);
				  break;
			  case "Invalid Command":
				  bot += message.response + '</div>';
				  $('div.message_holder').append(user);
				  $('div.message_holder').append(bot);
				  
				  break;
		  }
	  }
	
	  
  });
};