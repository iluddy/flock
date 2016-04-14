
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
    var url = options.url;
    var data = options.data;
    if( (options.type == 'get' || options.type == undefined) && options.data != undefined){
        url = url + '?' + $.param(options.data);
        data = '';
    }
    $.ajax({
        url: url,
        type: options.type || "get",
        datatype: "json",
        data: data,
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
            console.log(data);
            if (options.error != undefined)
                options.error(data);
            if (options.notify != false)
                 // TODO - this better
                 toastr.error(strip_response_msg(data.responseText), 'Oh No!', {'timeOut':3000, 'progressBar':true});
        }
    });
}

function anim(dom, type){
    $(dom).addClass('animated ' + type);
    setTimeout(function(){$(dom).removeClass('animated ' + type);}, 800);
}

function strip_response_msg(msg){
    return msg.replace('</p>', '').split('<p>').slice(-1)[0];
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

function date_string(unix_timestamp){
    // Create a new JavaScript Date object based on the timestamp
    // multiplied by 1000 so that the argument is in milliseconds, not seconds.
    var date = new Date(unix_timestamp);
    // Hours part from the timestamp
    var hours = date.getHours();
    // Minutes part from the timestamp
    var minutes = "0" + date.getMinutes();
    // Seconds part from the timestamp
    var seconds = "0" + date.getSeconds();

    // Will display time in 10:30:23 format
    var formattedTime = hours + ':' + minutes.substr(-2);
    return formattedTime;
}

function add_file_uploader(target, api_call, callback) {
    $(target).html($("#upload_file").tmpl({"api_call": api_call}));
    $('#fileuploader').fileupload({
        dataType: 'json',
        autoUpload: false,
        multipart: true,
        dropZone: $('#file_dropzone'),
        progressall: function (e, data) {
            var progress = parseInt(data.loaded / data.total * 100, 10);
            $(".upload_progress .progress-bar").css("width", progress.toString()+"%");
            $(".upload_progress .progress-bar").attr("aria-valuenow", progress.toString());
        },
        stop: function (e, data) {
            setTimeout(function(){$(".upload_progress").fadeOut(500);}, 1000);
            info_msg("Saved");
            callback();
        },
        start: function (e, data) {
            $('#file_dropzone').removeClass('accept');
            $("#file_upload_progress").css("width","0%");
            $(".upload_progress .progress-bar").attr("aria-valuenow", "0");
            $(".upload_progress .progress-bar").css("width","0%");
            $(".upload_progress").fadeIn(100);
        },
        dragover : function(e){
            $('#file_dropzone').addClass('accept');
        },
    }).on('dragleave', function(){$('#file_dropzone').removeClass('accept');})
}