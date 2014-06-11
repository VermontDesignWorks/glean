
/* ==========================================================================
                                  -----Forms-----
   ========================================================================== */
$('#div_id_vt_counties_single :checkbox').each(function(){
  $(this).click(function(){
    box=$(this).attr('id');
    if ($(this).prop('checked'))
    {
      $('#div_id_vt_counties_single :checkbox').each(function(){
          if ($(this).attr('id') != box)
          {
            $(this).attr('checked',false);
          }
      });
      $('#div_id_ny_counties_single :checkbox').each(function(){
          $(this).attr('checked',false);
      });
    }
  });
});
$('#div_id_ny_counties_single :checkbox').each(function(){
  $(this).click(function(){
    box=$(this).attr('id');
    if ($(this).prop('checked'))
    {
      $('#div_id_ny_counties_single :checkbox').each(function(){
          if ($(this).attr('id') != box)
          {
            $(this).attr('checked',false);
          }
      });
      $('#div_id_vt_counties_single :checkbox').each(function(){
          $(this).attr('checked',false);
      });
    }
  });
});
$('#title-button').popover({
 'title':"Title",
 'trigger':"hover",
 'content':"This is the name of your glean. It is how you will identify this glean from others on this day or week, and it also will also be the default Title to any Announcement Emails that are sent."
});

$('#description-button').popover({
         'title':"Description of the Glean",
         'trigger':"hover",
         'content':"This field will be visible on the Glean Page, and tells Volunteers what to expect. It is copied automatically into any Announcements made for this glean."
});

$('#farm-button').popover({
               'title':"Farm and Farm Location",
               'trigger':"hover",
               'content':"By Choosing a farm (and optionally a Farm Location) the remainder of the form auto-populates with Farm-specific Data."
            });

$('#counties-button').popover({
            'title':"Counties",
            'trigger':"hover",
            'content':"Volunteers are notified of gleans based on which counties they're interested in gleaning in. To select more than one county, use Ctrl (or option) and click on the additional counties you'd like to select"
         });

$('#farm-directions-button').popover({
   'title':"Farm Directions",
   'trigger':"hover",
   'content':"The Directions listed here, like all information in this grey box, will automatically be used whenever a Glean is at this farm. The Glean will also include a map, so only a couple of sentences are necessary."
});

$('#farm-instructions-button').popover({
   'title':"Farm Instructions",
   'trigger':"hover",
   'content':"These instructions will also be used when whenever a Glean is at this farm. This is a good place to put a couple general reminders about this farm, again only a couple of sentences are necessary."
});

$('#farm-counties-button').popover({
   'title':"Counties",
   'trigger':"hover",
   'content':"This determines what volunteers will be notified when a glean is taking place at this farm. Highlight the county to select it, if you need to select more than one you can click it while holding the Control key (Option key for mac)"
});

$('#location-name-button').popover({
       'title':"Location Name",
       'trigger':"hover",
       'content':"This is how you will identify this field or location from others. It is best to keep this simple but descriptive, like 'Back Field' or 'Wolcott Entrance'. This will help voluteers go to the right place, as the glean page will already reflect which farm this field is a subset of."
    });

$('#location-directions-button').popover({
   'title':"Farm Directions",
   'trigger':"hover",
   'content':"The Directions listed here, like all information in this grey box, will automatically be used whenever a Glean is at this farm. The Glean will also include a map, so only a couple of sentences are necessary."
});

$('#location-instructions-button').popover({
   'title':"Farm Instructions",
   'trigger':"hover",
   'content':"These instructions will also be used when whenever a Glean is at this farm location. This is a good place to put a couple general reminders about this farm, again only a couple of sentences are necessary."
});

$('#location-counties-button').popover({
   'title':"Counties",
   'trigger':"hover",
   'content':"This determines what volunteers will be notified when a glean is taking place at this farm location. Highlight the county to select it, if you need to select more than one you can click it while holding the Control key (Option key for mac)"
});

$('#physical_is_mailing-button').popover({
   'title':"Mailing Information",
   'trigger':"hover",
   'content':"This information is optional and for reference use only."
});

$(".datepicker").datepicker();

/* fix for bottom */
$(document).ready(function(){

});