$(document).ready(function(){ 

	$('.control-group .checkbox').each(function(){
	    htmlString = $(this).html();
	    htmlString = htmlString.replace('Delete', '');
	    $(this).html(htmlString);
	});
	form_delete = false
	$('.control-group').each(function(){
	  if ($(this).attr('id').substring(14,21) == 'DELETE')
	  {
	    form_delete = true
	  }
	});
	$('.control-group').each(function(){
	    if ($(this).attr('id').substring(0,12) == 'div_id_form-')
	    {
	      $(this).addClass('formset-row');
	      if (!form_delete)
	      {
	      }
	    }
	});
    if ($("select[id='id_form-0-member_organization']").get(0))
    {
    	$(".formset-label").prepend("<div>Member Organization</div>");
    }

});