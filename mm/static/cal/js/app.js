$(document).ready(function() {
    $('#calendar').fullCalendar({
    })
});

function loadEvents(p1, p2) {
    var val = $("input[type='checkbox']").val();
    $.ajax({
        url: "http://localhost:8000/schedule/api/occurrences?calendar_slug="+val+"&start=2017-12-31&end=2018-02-11"
    })
    .done(function( data ) {
        $('#calendar').fullCalendar('addEventSource', data);
    });
}