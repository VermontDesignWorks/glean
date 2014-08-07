$(document).ready(function(){ 

infos = {
    "description": "This is internal information useful in determining how best to serve this site; i.e. deliveries must be received at rear door, open 3rd Saturday of the Month, prepared meal site for children under 6, etc.",
}

    for (var i=0; i<Object.keys(infos).length; i++) {
       var key = Object.keys(infos)[i];
        var value = infos[key];
        var pop_name = key + "_popover";
        $("label[for='id_" + key +"']").append(
           "<div style='float: right;'><a class='farm-form-icons' id='" + pop_name + "'><i class='icon-info-sign'></i></a></div>"
        );
        $("#" + pop_name).tooltip({
           "title": value,
           "trigger": "hover",
        });
    }



});