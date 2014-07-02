$(document).ready(function(){
	$("#id_username").tooltip({
		placement: "top",
		trigger: "focus",
		title: "Please use only letters, numbers, and no spaces. Usernames are case sensitive!",
	});	
	$("#id_password1").tooltip({
		placement: "top",
		trigger: "focus",
		title: "Please use something long! All characters are allowed, case sensitive!"
	});
	
	var infos = {
      "vt_counties": "Selecting a county is necessary to recieve email notifications " +
      	"about gleans! "
    };
})
