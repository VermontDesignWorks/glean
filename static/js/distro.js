$(document).ready(function(){ 
    warnMessage = null;
    $(window).bind("beforeunload", function(){
    	if (warnMessage != null) return warnMessage;
    });
    $('input').change(function(){
    	console.log("Change made")
		warnMessage = "You may have unsaved changes.  You should save before leaving!!";
    });
    $('select').change(function(){
    	console.log("Change made")
		warnMessage = "You may have unsaved changes.  You should save before leaving!!";
    });
    $('input[type="submit"]').click(function(){
        warnMessage = null;
    });
	$('.control-group .checkbox').each(function(){
	    htmlString = $(this).html();
	    htmlString = htmlString.replace('Delete', '');
	    $(this).html(htmlString);
	});
	form_delete = false;
	$('.control-group').each(function(){
	  if ($(this).attr('id').substring($(this).attr('id').length - 6) == 'DELETE')
	  {
	    form_delete = true;
	    $(this).addClass('delete-format');
	  }
	});
	$('.control-group').each(function(){
	    if ($(this).attr('id').substring(0,12) == 'div_id_form-')
	    {
	      $(this).addClass('formset-row');
	      if (!form_delete)
	      {
	        if ($(this).attr('id').substring($(this).attr('id').length - 10) == 'containers')
	        {
	          $(this).after('</br>');
	        }
	      } else {
	        if ($(this).attr('id').substring($(this).attr('id').length - 6)=='DELETE')
	        {
	          $(this).after('</br>');
	        }
		  }
		}
	});
    if ($("select[id='id_form-0-member_organization']").get(0))
    {
    	$(".formset-label").prepend("<div>Member Organization</div>");
    }

});