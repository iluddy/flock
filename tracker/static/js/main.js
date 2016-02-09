//var people_tmpl;

$(document).ready(function () {
    page_main = $("#main");
    loader = $("#loader");
    $.when(
        ajax_load('/role_types', {}, cache_role_types),
        ajax_load('/templates', {}, add_templates)
    ).done(templates_loaded);
});

function add_templates(input){
    $("#tmpl_holder").html(input);
}

function cache_role_types(input){
    role_types = {};
    for( var index in input){
        role_types[input[index]._id] = input[index];
    }
}


function compile_templates(){
    people_tmpl = Handlebars.compile($("#people_tmpl").html());
    dashboard_tmpl = Handlebars.compile($("#dashboard_tmpl").html());
    calendar_tmpl = Handlebars.compile($("#calendar_tmpl").html());
    events_tmpl = Handlebars.compile($("#events_tmpl").html());
    things_tmpl = Handlebars.compile($("#things_tmpl").html());
    places_tmpl = Handlebars.compile($("#places_tmpl").html());
    settings_tmpl = Handlebars.compile($("#settings_tmpl").html());
    notifications_tmpl = Handlebars.compile($("#notifications_tmpl").html());
    people_type_table_tmpl = Handlebars.compile($("#people_type_table_tmpl").html());
}

function add_handlers(){
    $('.tab').click(tab_handler);
}

function tab_handler(){
    clear();
    window['load_' + $(this).attr('target').toString()]();
    $(this).addClass('active').siblings('.tab').removeClass('active');
    load_components();
}

function load_components(){
    $('.i-checks').iCheck({
        checkboxClass: 'icheckbox_square-green',
        radioClass: 'iradio_square-green',
    });
    $('.color-choice').on('click', function(){
        $(this).addClass('selected').siblings().removeClass('selected');
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

function load_dashboard(){
    $(page_main).html(dashboard_tmpl());
}

function load_calendar(){
    $(page_main).html(calendar_tmpl());
}

function load_people(){
    $(page_main).html(people_tmpl());
}

function load_things(){
    $(page_main).html(things_tmpl());
}

function load_places(){
    $(page_main).html(places_tmpl());
}

function load_settings(){
    $(page_main).html(settings_tmpl());
    load_people_type_table();
}

function load_people_type_table(){
    function load_people_types(input){
        $('#people_type_table_holder').html(people_type_table_tmpl({'types': input}));
    }
    ajax_call({
        'url': 'roles',
        'notify': false,
        'success': load_people_types
    });
}

function load_notifications(){
    $(page_main).html(notifications_tmpl());
}

function load_events(){
    $(page_main).html(events_tmpl());
}

function add_update_people_type(){
    data = {
        'theme': $('#people_type_colour .color-choice.selected').attr('value'),
        'type': $('#people_type_type_check').find('input:checked').attr('value'),
        'name': $('#people_type_name').val(),
        'id': $('#people_type_id').val(),
    }
    ajax_call({
        'url': 'roles/update',
        'data': data,
        'type': 'post',
        'success': load_people_type_table
    });
}