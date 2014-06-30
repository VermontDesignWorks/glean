$(document).ready(function(){ 

infos = {
    "directions": "These directions will appear on the glean page any time you coordinate a glean at this farm. Directions could be brief to compliment the glean page map or could be detailed, i.e. from the north, south, etc. or from major towns near the farm.",
    "instructions": "These instructions appear on the glean page every time you coordinate a glean at this farm. For example, parking instructions.",
    "vt_counties_single": "If volunteers signed up to learn about events in this county, they’ll get any announcements sent out about gleans at this farm.",
    "description": "These are internal notes regarding farm relations, preferred service, etc.",
    "ny_counties_single": "If volunteers signed up to learn about events in this county, they’ll get any announcements sent out about gleans at this farm."
}

    for (var i=0; i<Object.keys(infos).length; i++) {
       var key = Object.keys(infos)[i];
        var value = infos[key];
        var pop_name = key + "_popover";
        $("label[for='id_" + key +"']").append(
           "<div style='float: right;'><a id='" + pop_name + "'><i class='icon-info-sign farm-form-icons'></i></a></div>"
        );
        $("#" + pop_name).tooltip({
           "title": value,
           "trigger": "hover",
        });
    }



});