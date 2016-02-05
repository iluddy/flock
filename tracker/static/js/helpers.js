
function elapsed_time(milliseconds) {
    // TIP: to find current time in milliseconds, use:
    // var  current_time_milliseconds = new Date().getTime();

    milliseconds = new Date().getTime() - milliseconds;

    function numberEnding (number) {
        return (number > 1) ? 's' : '';
    }

    var temp = Math.floor(milliseconds / 1000);
    var years = Math.floor(temp / 31536000);
    if (years) {
        return years + ' year' + numberEnding(years);
    }
    //TODO: Months! Maybe weeks?
    var days = Math.floor((temp %= 31536000) / 86400);
    if (days) {
        return days + ' day' + numberEnding(days);
    }
    var hours = Math.floor((temp %= 86400) / 3600);
    if (hours) {
        return hours + ' hr' + numberEnding(hours);
    }
    var minutes = Math.floor((temp %= 3600) / 60);
    if (minutes) {
        return minutes + ' min' + numberEnding(minutes);
    }
//    var seconds = temp % 60;
//    if (seconds) {
//        return seconds + ' s' + numberEnding(seconds);
//    }
    return 'just now'; //'just now' //or other string you like;
}

function ajax_load(func, args, callback, timeout){
    return $.ajax({
        url: func,
        data: args,
        timeout: timeout == undefined ? 10000 : timeout
    }).done(function(input){
        console.log(input);
        if (callback)
            callback(input);
    }).error(function(request, error){
        console.log(error);
    });
}