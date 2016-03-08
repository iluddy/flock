
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
        type: 'get',
        timeout: timeout == undefined ? 10000 : timeout
    }).done(function(input){
        if (callback)
            callback(input);
    }).error(function(request, error){
        console.log(error);
    });
}

function ajax_call(options){
    $.ajax({
        url: options.url,
        type: options.type || "get",
        datatype: "json",
        data: options.data,
        complete: function(data) {
            if (options.complete != undefined)
                options.complete(data);
        },
        success: function(data) {
            if (options.success != undefined)
                options.success(data);
            if (options.notify != false)
                toastr.success(data, 'Success!', {'timeOut':2000, 'progressBar':true});
        },
        error: function(data) {
            if (options.error != undefined)
                options.error(data);
            if (options.notify != false)
                // TODO - this better
                var error_msg = data.responseText.replace('</p>', '').split('<p>').slice(-1)[0];
                toastr.error(error_msg, 'Oh No!', {'timeOut':3000, 'progressBar':true});
        }
    });
}

function anim(dom, type){
    $(dom).addClass('animated ' + type);
    setTimeout(function(){$(dom).removeClass('animated ' + type);}, 800);
}

function scrll(dom, delay){
    $('html, body').animate({
        scrollTop: $(dom).offset().top
    }, delay);
}

function confirmation(){
    swal({
        title: "Are you sure?",
        text: "You will not be able to recover this imaginary file!",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "Yes, delete it!",
        closeOnConfirm: false
    }, function () {
        swal("Deleted!", "Your imaginary file has been deleted.", "success");
    });
}

var delay = (function(){
    var timer = 0;
    return function(callback, ms){
        clearTimeout (timer);
        timer = setTimeout(callback, ms);
    };
})();