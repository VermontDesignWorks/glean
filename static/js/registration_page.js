$(document).ready(function(){
	$("#id_username").tooltip({
		placement: "top",
		trigger: "focus",
		title: "Please use only letters, numbers, and no spaces.",
	});	
	$("#id_password1").tooltip({
		placement: "top",
		trigger: "focus",
		title: "Please use something long! All characters are allowed"
	});
	console.log("working");
})

