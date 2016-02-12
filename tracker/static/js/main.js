var roles;

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
    // Templates
    people_tmpl = Handlebars.compile($("#people_tmpl").html());
    dashboard_tmpl = Handlebars.compile($("#dashboard_tmpl").html());
    calendar_tmpl = Handlebars.compile($("#calendar_tmpl").html());
    events_tmpl = Handlebars.compile($("#events_tmpl").html());
    things_tmpl = Handlebars.compile($("#things_tmpl").html());
    places_tmpl = Handlebars.compile($("#places_tmpl").html());
    settings_tmpl = Handlebars.compile($("#settings_tmpl").html());
    notifications_tmpl = Handlebars.compile($("#notifications_tmpl").html());
    people_type_table_tmpl = Handlebars.compile($("#people_type_table_tmpl").html());
    no_data_tmpl = Handlebars.compile($("#no_data_tmpl").html());
    people_table_body_tmpl = Handlebars.compile($("#people_table_body_tmpl").html());

    // Partial Templates
    Handlebars.registerPartial("person_type_part", $("#people_type_table_row_tmpl").html());
    Handlebars.registerPartial("checkbox_part", $("#checkbox_tmpl").html());
    Handlebars.registerPartial("radio_part", $("#radio_button_tmpl").html());
}

function add_handlers(){
    $('.tab').click(tab_handler);
}

function tab_handler(){
    clear();
    var target = $(this).attr('target').toString();
    window['load_' + target]();
    $(this).addClass('active').siblings('.tab').removeClass('active');
}

function radio_toggle(){
    $(this).addClass('selected').siblings().removeClass('selected');
}

function toggle(){
    $(this).toggleClass('selected');
}

function load_components(){
    $('.i-checks').iCheck({
        checkboxClass: 'icheckbox_square-green',
        radioClass: 'iradio_square-green',
    });
    $('.color-choice').on('click', radio_toggle);
}

function templates_loaded(){
    compile_templates();
    add_handlers();
    if ( window.location.hash != '' ){
        var target = $('.tab[target=' + window.location.hash.replace('#', '') + ']');
        if( $(target).length > 0 ){
            $(target).click();
        }else{
            $('.tab').first().click();
        }
    }else{
        $('.tab').first().click();
    }
    $(document).ajaxStart(function() { Pace.restart(); });
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
    $('#calendar_wrap').fullCalendar({
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay'
        },
    })

}

function load_people(){
    var roles, people;
    var sort_by, sort_dir, role_filter;

    function draw_people(data){
        $('#people_table_body').html(people_table_body_tmpl({'people': data}));
    }

    function reload_people(){
        var filter = {
            'roles': JSON.stringify(role_filter)
        }
        ajax_call({'url': '/people', 'type': 'post', 'notify': false, 'data': filter, 'success': draw_people});
    }

    function apply_filter(){
        $(this).toggleClass('selected');
        get_filters();
        reload_people();
    }

    function get_filters(){
        sort_by = 'type';
        sort_dir = 'asc';
        role_filter =  $(".filter-label.selected").map(function(){return parseInt($(this).attr("role_id"));}).get();
    }

    $.when(
        ajax_load('/roles', {}, function(data){roles=data}),
        ajax_load('/people', {}, function(data){people=data})
    ).done(function(){
        $(page_main).html(people_tmpl({"roles": roles}));
        draw_people(people);
        $('#people_table_control .filter-label').on('click', apply_filter);
    });
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
    load_components();
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
        'id': $('#add_people_type_form').attr('people_type_id')
    }
    ajax_call({
        'url': 'roles/update',
        'data': data,
        'type': 'post',
        'success': load_people_type_table
    });
}

function load_people_type_table(){

    function reset_form(){
        $("#add_people_type_btn").text("Add");
        $("#people_type_name").val("");
        $("#people_type_type_check .iradio_square-green").first().click();
        $("#people_type_colour span").first().click();
        $("#add_people_type_form").attr('people_type_id', '');
    }

    function delete_people_type(){
        ajax_call({
            'url': 'roles/delete',
            'type': 'post',
            'data': {
                'id': $(this).attr('type_id')
             },
            'success': load_people_type_table
        });
    }

    function edit_people_type(){
        $("#add_people_type_btn").text("Update");
        $('#add_people_type_form').attr('people_type_id', $(this).attr('type_id'));
        $("#people_type_name").val($(this).attr('name'));
        $("#people_type_colour span").first().click();
        $("#people_type_type_check .iradio_square-green input[value=" + $(this).attr('role_type')  + "]").click();
        $('#people_type_colour span.label-' + $(this).attr('theme')).click();
        scrll('#main', 200);
        anim('#add_people_type_form', 'pulse');
    }

    reset_form();
    ajax_call({
        'url': 'roles',
        'notify': false,
        'success': function(input){
            roles = input;
            if( input.length > 0){
                $('#people_type_table_holder').html(people_type_table_tmpl({'types': input}));
                $('#people_type_table_body i.delete').on('click', delete_people_type);
                $('#people_type_table_body i.edit').on('click', edit_people_type);
            }else{
                $('#people_type_table_holder').html(no_data_tmpl({
                    'caption': 'There are no People-Types configured. Add some now!'
                }));
            }
        }
    });
}