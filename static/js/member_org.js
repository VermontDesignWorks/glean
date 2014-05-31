$(document).ready(function(){   
   var $datefield = $("#id_date");
   var infos = {
      "description": "Information entered here can include" +
      " any of the following: your organization/program(s)" +
      " mission, goals and objectives, your history," +
      " populations served, etc."
   };
   for (var i=0; i<Object.keys(infos).length; i++) {
      (function(i){
         var key = Object.keys(infos)[i];
         var value = infos[key];
         var pop_name = key + "_popover";
         $("label[for='id_" + key +"']").append(
            "<div class='pull-right'><a id='" + pop_name + "'><i class='icon-info-sign'></i></a></div>"
         );
         $("#" + pop_name).tooltip({
            "title": value,
            "trigger": "hover",
         })
      })(i)
   }
})