$(document).ready(function(){ 
	position = $("#wrapper").offset();
	top = position.top
	bottom = position.top + $("#wrapper").height()
	bottom = bottom - 100
    $("#footer-overall").css({"top": bottom });
});