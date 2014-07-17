$(document).ready(function(){
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
	        if ($(this).attr('id').substring($(this).attr('id').length - 5) == 'notes')
	        {
	          $(this).after('</br>');
	        }
	      } else {
	        if ($(this).attr('id').substring($(this).attr('id').length - 6)=='DELETE')
	        {
	          width = $('.label-row').width() + 100;
	          $(".label-row").css("width", width);
	          $("#form-id-0").css("width", width);
	          $(this).after('</br>');

	        }
		  }
		}
	});
    if (form_delete) {
    	$(".label-row").append("<div>Delete</div>");
    }
	if ($("select[id='id_form-0-member_organization']").get(0))
    {
    	$(".label-row").prepend("<div>Member Organization</div>");
    	width = $('.label-row').width() + 100;
	    $(".label-row").css("width", width);
	    $("#form-id-0").css("width", width);
    }
});