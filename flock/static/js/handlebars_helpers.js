Handlebars.registerHelper('decimal', function(value) {
    return new Handlebars.SafeString(value.toFixed(2));
});

Handlebars.registerHelper('tip', function(position, tip) {
    return new Handlebars.SafeString(
        '<span class="sl-hint hint--' + position + ' hint--bounce" data-hint="' + tip + '">' +
        '<i class="fa fa-question-circle"></i></span>'
    );
});

Handlebars.registerHelper('elapsed', function(stamp) {
    return new Handlebars.SafeString(
        elapsed_time(stamp * 1000)
    );
});

Handlebars.registerHelper('in_array', function(elem, list, options) {
    if(list.indexOf(elem) > -1) {
        return options.fn(this);
    }
    return options.inverse(this);
});

Handlebars.registerHelper('any_in_array', function(elems, list, options) {
    for( var i in elems ){
        if(list.indexOf(elems[i]) > -1) {
            return options.fn(this);
        }
    }
    return options.inverse(this);
});