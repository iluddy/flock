var people_tmpl;

$(document).ready(function () {
    page_main = $("#main");
    loader = $("#loader");
    $.when(
        ajax_load('/templates', {}, add_templates)
    ).done(templates_loaded);
});

function add_templates(input){
    $("#tmpl_holder").html(input);
}

function compile_templates(){
    people_tmpl = Handlebars.compile($("#people_tmpl").html());
}

function add_handlers(){
    $('.tab').click(tab_handler);
}

function tab_handler(){
    clear();
    var target = $(this).attr('target').toString() + '_tmpl';
    $(page_main).html(people_tmpl());
    $(this).addClass('active').siblings('.tab').removeClass('active');
    load_components();
}

function load_components(){
    $('.i-checks').iCheck({
        checkboxClass: 'icheckbox_square-green',
        radioClass: 'iradio_square-green',
    });
}

function templates_loaded(){
    compile_templates();
    add_handlers();
    $('.tab').first().click();
}

function clear(){
    page_main.empty();
}

function loadr(show){
    $(loader).toggle(show);
}
