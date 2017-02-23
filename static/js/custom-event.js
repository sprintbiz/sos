(function() {
  $('#calendar').fullCalendar({
    editable: true,
    height: 300,
    header: {
      left: 'title',
      center: '',
      right: 'today prev,next'
    },
    eventSources: [
        {
            url: '/calendar/json/event/' // url to get events
        }
        // any other sources...
    ],
    eventClick: function(calEvent, jsEvent, view) {
      //var start = $.fullCalendar.moment(calEvent.start).format('YYYY-MM-DD');
      //var end = $.fullCalendar.moment(calEvent.end).format('YYYY-MM-DD');

      var $select = $('#modal-select');

      $select.select2({
        containerCss : {"display":"block"},
        dropdownParent: $("#myModal"),
        ajax: {
          url: "/calendar/json/project/",
          delay: 250,
          data: function(params) {
              return {
                  q: params.term // search term
              };
          },
          processResults: function(data, params) {
              // parse the results into the format expected by Select2
              // since we are using custom formatting functions we do not need to
              // alter the remote JSON data, except to indicate that infinite
              // scrolling can be used
              var resData = [];
              data.forEach(function(value) {
                  if (value.text.indexOf(params.term) != -1)
                      resData.push(value)
              })
              return {
                  results: $.map(resData, function(item) {
                      return {
                          text: item.text,
                          id: item.id
                      }
                  })
              };
          },
        }
      }); // initialize Select2 and any events

      var $option = $('<option selected>Loading...</option>').val("0");

      $select.append($option).trigger('change'); // append the option and update Select2

      $.ajax({ // make the request for the selected data object
        type: 'GET',
        url: '/calendar/json/project/?id=' + calEvent.project,
        dataType: 'json'
      }).then(function (data) {
        // Here we should have the data object
        console.log(data);
        $option.text(data.text).val(data.id); // update the text that is displayed (and maybe even the value)
        $option.removeData(); // remove any caching data that might be associated
        $select.trigger('change'); // notify JavaScript components of possible changes
      });

      $("#dialog").dialog({
        autoOpen: false,
      });
      document.getElementsByName('modal-event-id')[0].value = calEvent.id;
      //$("#id").val(calEvent.id);
      document.getElementsByName('modal-event-name')[0].value = calEvent.title;
      //$("#title").val(calEvent.title);
      document.getElementsByName('modal-event-start_date')[0].value = $.fullCalendar.moment(calEvent.start).format('YYYY-MM-DD');
      //$('#start').val(start);
      document.getElementsByName('modal-event-end_date')[0].value = $.fullCalendar.moment(calEvent.end).format('YYYY-MM-DD');
      //$('#end').val(end);
      document.getElementsByName('modal-event-hour')[0].value = calEvent.hour;
      //$('#hour').val(calEvent.hour);
      document.getElementsByName('modal-event-project')[0].value = calEvent.project;
      //$('#project').val(calEvent.project);
      $('#myModal').modal();
    },
    viewRender: function(view, element) {
      $.each($(".fc-day-top"), function(key, val) {
        var dateYMD = $(this).attr("data-date");
        $(this).append("<div class='fc-dailytotal' id='dailytotal-"+dateYMD+"'></div>");
      });
    },

    eventRender: function(event, element, view) {
    // lets test if the event has a property called holiday.
    // If so and it matches '1', change the background of the correct day
    $(".fc-dailytotal").text(0); //Clear total sum
      if (event.id >= 1) {
          var dateString = event.start.format("YYYY-MM-DD");

          $(view.el[0]).find('.fc-day[data-date=' + dateString + ']').css('background-color', '#29c75f' );
          element.find('.fc-day-numer').css('color', '#f5f5f5');
          element.find(".fc-title").append(' ' + event.hour + 'h'); // Add hour to displayed event
      }

    },
    eventAfterRender: function(event, element, view) {
        var currentday = moment(event.start).format("YYYY-MM-DD");

        if (event.hour > 0) {
          var prev = $("#dailytotal-"+currentday).text() || 0;
          $("#dailytotal-"+currentday).text(+prev + +event.hour);
        }
    }

  });
}());
