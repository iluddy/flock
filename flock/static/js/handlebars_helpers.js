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

Handlebars.registerHelper('array_empty', function(list, options) {
    if(list.length == 0) {
        return options.fn(this);
    }
    return options.inverse(this);
});

Handlebars.registerHelper('perm', function(elem, options) {
    if (permissions.indexOf(elem) > -1) {
        return options.fn(this);
    }
    return options.inverse(this);
});

Handlebars.registerHelper('array_not_empty', function(list, options) {
    if(list.length > 0) {
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

Handlebars.registerHelper('dateFormat', function(context, block) {
    if (window.moment) {
        var f = block.hash.format || "MMM DD, YYYY hh:mm:ss A";
        return moment(context).format(f); //had to remove Date(context)
    }else{
        return context;   //  moment plugin not available. return data as is.
    };
});

Handlebars.registerHelper('isToday', function(context, block) {
  if (window.moment) {
    if (moment(context).format('DD/MM/YYYY') == moment(new Date()).format('DD/MM/YYYY')){
        return 'Today';
    }else{
        return moment(context).format('DD MMM'); //had to remove Date(context)
    }
  }else{
    return context;   //  moment plugin not available. return data as is.
  };
});

Handlebars.registerHelper('relativeTime', function(context, block) {
  if (window.moment) {
    // var f = block.hash.format || "MMM DD, YYYY hh:mm:ss A";
    return moment(context).fromNow();
  }else{
    return context;   //  moment plugin not available. return data as is.
  };
});

Handlebars.registerHelper('equal', function(lvalue, rvalue, options) {
    if (arguments.length < 3)
        throw new Error("Handlebars Helper equal needs 2 parameters");
    if( lvalue!=rvalue ) {
        return options.inverse(this);
    } else {
        return options.fn(this);
    }
});