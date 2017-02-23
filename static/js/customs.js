$("#event_start_date").datepicker({
  dateFormat: 'yy-mm-dd',
  changeMonth: true,
  numberOfMonths: 1,
  onClose: function(selectedDate) {

    /*var day1 = $("#booking-from").datepicker('getDate').getDate() + 1;
    var month1 = $("#booking-from").datepicker('getDate').getMonth();
    var year1 = $("#booking-from").datepicker('getDate').getFullYear();
    year1 = year1.toString().substr(2,2);
    var fullDate = day1 + "-" + month1 + "-" + year1;*/
    var minDate = $(this).datepicker('getDate');
    var newMin = new Date(minDate.setDate(minDate.getDate() + 1));
    $("#event_end_date").datepicker("option", "minDate", newMin);
  }
});
$("#event_end_date").datepicker({
  changeMonth: true,
  dateFormat: 'yy-mm-dd',
  numberOfMonths: 1,

});
$("#event_start_date").datepicker('setDate', '+0');
$("#event_end_date").datepicker('setDate', '+0');
$(".datepicker").datepicker({
  dateFormat: 'yy-mm-dd'
});




var remoteDataConfig = {
      containerCss : {"display":"block"},
        ajax: {
            url: "/calendar/json/project/",
            dataType: 'json',
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
            cache: true
        },
        minimumInputLength: 1

}
$(document).ready(function() {
  $("#select2").select2({
    remoteDataConfig
  });


$("#project-select").select2(remoteDataConfig);


});

// List of days not filled in time scheet view


$(document).ready(function() {
    $('#datatable').DataTable( {
        "ajax": "/json/daysnotfilled/",
        "sAjaxDataProp" : "",
        "columns": [
            { "data": "start_date" },
            { "data": "total_hours" }
        ]
    } );
} );
