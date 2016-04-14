var user_id, page_main, loader, permissions;

$(document).ready(function () {
    page_main = $("#main");
    loader = $("#loader");
    user_id = parseInt($(".account_info .fa").attr("user_id"));
    permissions = $(".account_info .fa").attr("permissions");
    $.when(
        ajax_load('/templates', {}, add_templates)
    ).done(templates_loaded);
});

$( document ).ajaxError(function( event, jqxhr ) {
    // Logout if session expires
    if( jqxhr.status == 403 )
        $(location).attr('href', 'logout');
});

function add_templates(input){
    $("#tmpl_holder").html(input);
}

function compile_templates(){
    // Templates
    people_tmpl = Handlebars.compile($("#people_tmpl").html());
    dashboard_tmpl = Handlebars.compile($("#dashboard_tmpl").html());
    planner_tmpl = Handlebars.compile($("#planner_tmpl").html());
    events_tmpl = Handlebars.compile($("#events_tmpl").html());
    things_tmpl = Handlebars.compile($("#things_tmpl").html());
    places_tmpl = Handlebars.compile($("#places_tmpl").html());
    settings_tmpl = Handlebars.compile($("#settings_tmpl").html());
    notifications_tmpl = Handlebars.compile($("#notifications_tmpl").html());
    no_data_tmpl = Handlebars.compile($("#no_data_tmpl").html());
    no_data_table_tmpl = Handlebars.compile($("#no_data_table_tmpl").html());
    places_table_body_tmpl = Handlebars.compile($("#places_table_body_tmpl").html());
    people_type_table_tmpl = Handlebars.compile($("#people_type_table_tmpl").html());
    people_table_body_tmpl = Handlebars.compile($("#people_table_body_tmpl").html());
    event_tmpl = Handlebars.compile($("#event_tmpl").html());
    event_tip_tmpl = Handlebars.compile($("#event_tip_tmpl").html());
    notifications_tmpl = Handlebars.compile($("#notifications_tmpl").html());
    upcoming_events_tmpl = Handlebars.compile($("#upcoming_events_tmpl").html());

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

function sort_toggle(dom){
    $(dom).parent().siblings().children('.table-sorter').removeClass('fa-sort-up').removeClass('fa-sort-down').addClass('fa-sort');
    $(dom).removeClass('fa-sort');
    if( $(dom).hasClass('fa-sort-down') ){
        $(dom).removeClass('fa-sort-down').addClass('fa-sort-up');
    }else if( $(dom).hasClass('fa-sort-up') ){
        $(dom).removeClass('fa-sort-up').addClass('fa-sort-down');
    }else{
        $(dom).addClass('fa-sort-down');
    }
}

function load_components(){
    $('.i-checks').iCheck({
        checkboxClass: 'icheckbox_square-green',
        radioClass: 'iradio_square-green',
    });
    $('.color-choice').on('click', radio_toggle);
    $('.color-choice').first().click();
    $('.label-color-choice').on('click', radio_toggle);
    $('.label-color-choice').first().click();
    $('.btn-choice .btn').on('click', function(){
        $(this).siblings().removeClass('btn-primary').addClass('btn-white').removeClass('selected');
        if( $(this).hasClass('selected') ){
            $(this).removeClass('btn-primary').addClass('btn-white').removeClass('selected');
        }else{
            $(this).addClass('btn-primary').removeClass('btn-white').addClass('selected');
        }
    });
}

function reset_components(){
    $('.btn-choice .btn').off('click').removeClass('btn-primary').addClass('btn-white').removeClass('selected');
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
    ajax_call({
        'url': '/events',
        'data': {
            'limit': 10,
            'sort_by': 'start',
            'show_expired': false,
            'user_id': user_id
        },
        'notify': false,
        'success': function(input){
            $('#upcoming-timeline-wrapper').append(upcoming_events_tmpl({'events': input}));
        }
    });
    ajax_call({
        'url': '/notifications',
        'type': 'post',
        'data': {
            'limit': 20,
            'offset': 0,
            'sort_by': 'stamp',
            'sort_dir': 'asc'
        },
        'notify': false,
        'success': function(input){
            $('#notifications-wrapper').append(notifications_tmpl({'notifications': input}));
        }
    });
}

function load_planner(){
    $(page_main).html(planner_tmpl());

    $('#calendar_holder').fullCalendar({
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'agendaDay,agendaWeek,month',
        },
        defaultView: "agendaDay",
        minTime: "06:00:00",
        maxTime: "23:00:00",
        height: $('#page-wrapper').height(),
        selectable: true,
        events: '/events',
        eventRender: function(event, element) {
            event.start_string = date_string(event.start);
            event.end_string = date_string(event.end);
            $(event_tmpl({'people': event.people})).insertAfter($(element).find('.fc-content'));
            $(element).qtip({
                content:{
                  text: event_tip_tmpl(event)
                },
                style: {
                    classes: 'qtip-bootstrap'
                },
                hide: {
                    delay: 200,
                    fixed: true
                },
                position: {
                    my: 'bottom middle',  // Position my top left...
                    at: 'top middle', // at the bottom right of...
                }
            });
        },
        eventMouseover: function(event, element){
            $(element.currentTarget).addClass('active');
        },
        eventMouseout: function(event, element){
            $(element.currentTarget).removeClass('active');
        },
    });
}

function load_people(){
    var sort_by, sort_dir, search, roles, people, count;
    var page = 0;
    var limit = 15;

    function draw_people(data){
        if( data.data.length == 0){
            $('#people_table_body').html(no_data_table_tmpl({
                'caption': 'No People to display. Broaden your search or add some People!', 'span': '6'
            }));
        }else{
            $('#people_table_body').html(people_table_body_tmpl({'people': data.data}));
            $('#people_table_body .delete-btn').on('click', delete_person);
            $('#people_table_body .edit-btn').on('click', edit_person);
            $('#people_table_body .invite-btn').on('click', invite_person);
        }
        count = data.count;
        $('#person_count').text(data.count);
        update_pagination();
    }

    function update_pagination(){
        var start = (limit * page) + 1;
        start = start < count ? start : count;
        $('#person_start').text(start);
        var end = (limit * page) + limit;
        end = end > count ? count : end;
        $('#person_end').text(end);
    }

    function next_page(){
        if( (page + 1) * limit <= count ){
            page = page + 1;
            reload_people();
        }
    }

    function last_page(){
        if( page > 0){
            page = page - 1;
            reload_people();
        }
    }

    function reset_people_form(){
        $("#add_person_form").attr("person_id", "");
        $("#add_person_invite_box").show();
        $('#add_person_email').removeAttr('disabled');
        $('#add_person_name').val('');
        $('#add_person_email').val('');
        $('#add_person_phone').val('');
        $("#modal_add_person").text('Add');
        $("#add_people_modal .modal-title").text("Add a Person");
    }

    function reload_people(){
        $('#add_person_error').hide();
        var filter = {
            'search': search.val(),
            'sort_by': sort_by,
            'sort_dir': sort_dir,
            'offset': page,
            'limit': limit
        }
        ajax_call({
            'url': '/people',
            'type': 'get',
            'notify': false,
            'data': filter,
            'success': draw_people
        });
        $('#add_people_modal').modal('hide');
    }

    function edit_person(){
        reset_people_form();
        $("#add_person_invite_box").hide();
        var person_id = $(this).attr("person_id");
        var person_dom = $(this).parent().parent();
        $("#modal_add_person").text('Update');
        $("#add_people_modal .modal-title").text("Update a Person");
        $("#add_person_form").attr("person_id", person_id);
        $('#add_person_name').val($.trim($(person_dom).find('.person_name').text()));
        $('#add_person_email').val($.trim($(person_dom).find('.person_email').text()));
        $('#add_person_email').attr('disabled','');
        var person_phone = $(person_dom).find('.person_phone').text();
        if( person_phone.indexOf('Unknown') == -1 )
            $('#add_person_phone').val($.trim(person_phone));
    }

    function add_person(e){
        e.preventDefault();
        var person = {
            'id': $('#add_person_form').attr('person_id'),
            'type': $('#role_dropdown_value').attr('role_id'),
            'name': $('#add_person_name').val(),
            'mail': $('#add_person_email').val()
        };

        var phone = $('#add_person_phone').val();
        var invite = $('#add_person_invite').is(":checked");

        if( invite == true )
            person['invite'] = true;

        if( phone.length > 0)
            person['phone'] = phone;

        if ( person['name'].length > 0 && person['mail'].length > 0 )

            if( person['id'].length > 0 ){
                ajax_call({
                    'url': '/people',
                    'type': 'put',
                    'data': person,
                    'success': reload_people
                });
            }else{
                ajax_call({
                    'url': '/people',
                    'type': 'post',
                    'data': person,
                    'success': reload_people
                });
            }

    }

    function delete_person(){
        var to_remove = {'id': parseInt($(this).attr("person_id")), 'name': $(this).attr('name')};
        ajax_call({
            'url': '/people',
            'type': 'delete',
            'data': to_remove,
            'success': reload_people
        });
    }

    function invite_person(){
        var to_invite = {'mail': $(this).attr("mail")};
        ajax_call({'url': '/people/invite', 'type': 'post', 'data': to_invite, 'success': reload_people});
    }
    
    function choose_role(){
        $("#role_dropdown_value").removeClass().addClass("themed themed-" + $(this).attr("role_theme"));
        $("#role_dropdown_value").attr("role_id", $(this).attr("role_id"));
        $("#role_dropdown_value").text($(this).attr("role_name"));
    }
    
    function add_handlers(){
        $('#modal_add_person').on('click', add_person);
        $('#add_person_btn').on('click', reset_people_form);
        $('#role_dropdown_choice li > a').on('click', choose_role);
        $('#role_dropdown_choice li > a:first').click();
        $('#people_table_search').on('keyup', function(){
            delay(function(){
                page = 0;
                reload_people();
            }, 800 );
        });
        $('.table-sorter').on('click', function(){
            sort_toggle($(this));
            sort_by = $(this).attr('sorter');
            sort_dir = $(this).hasClass('fa-sort-down') == true ? 'desc' : 'asc';
            reload_people();
        });
        $('#person_next').on('click', next_page);
        $('#person_prev').on('click', last_page);
        search = $('#people_table_search');
    }
    $.when(
        ajax_load('/roles', {}, function(data){roles=data}),
        ajax_load('/people', {}, function(data){people=data})
    ).done(function(){
        $(page_main).html(people_tmpl({"roles": roles}));
        draw_people(people);
        add_handlers();
        load_components();
    });
}

function load_things(){
    $(page_main).html(things_tmpl());
}

function load_places(){
    var sort_by, sort_dir, search, places, count;
    var page = 0;
    var limit = 10;

    function draw_places(data){
        if( data.data.length == 0){
            $('#places_table_body').html(no_data_table_tmpl({
                'caption': 'No Places to display. Broaden your search or add some Places!', 'span': '5'
            }));
        }else{
            $('#places_table_body').html(places_table_body_tmpl({'places': data.data}));
            $('#places_table_body .delete-btn').on('click', delete_place);
            $('#places_table_body .edit-btn').on('click', edit_place);
        }
        count = data.count;
        $('#places_count').text(data.count);
        update_pagination();
    }

    function update_pagination(){
        var start = (limit * page) + 1;
        start = start < count ? start : count;
        $('#places_start').text(start);
        var end = (limit * page) + limit;
        end = end > count ? count : end;
        $('#places_end').text(end);
    }

    function next_page(){
        if( (page + 1) * limit <= count ){
            page = page + 1;
            reload_places();
        }
    }

    function last_page(){
        if( page > 0){
            page = page - 1;
            reload_places();
        }
    }

    function reset_places_form(){
        $("#add_place_form").attr("place_id", "");
        $('#add_place_name').val('');
        $('#add_place_email').val('');
        $('#add_place_phone').val('');
        $('#add_place_address').val('');
        $("#modal_add_place").text('Add');
        $("#add_places_modal .modal-title").text("Add a Place");
    }

    function reload_places(){
        $('#add_place_error').hide();
        var filter = {
            'search': search.val(),
            'sort_by': sort_by,
            'sort_dir': sort_dir,
            'offset': page,
            'limit': limit
        }
        ajax_call({
            'url': '/places',
            'type': 'get',
            'notify': false,
            'data': filter,
            'success': draw_places
        });
        $('#add_places_modal').modal('hide');
    }

    function add_place(e){
        e.preventDefault();
        var place = {
            'name': $('#add_place_name').val(),
            'email': $('#add_place_email').val(),
            'phone': $('#add_place_phone').val(),
            'address': $('#add_place_address').val(),
        };
        // TODO - validate form
        if ( place['name'].length > 0 && place['address'].length > 0 ) {
            var place_id = $("#add_place_form").attr("place_id").toString();
            if( place_id.length > 0){
                place['id'] = place_id;
                ajax_call({
                    'url': '/places',
                    'type': 'put',
                    'data': place,
                    'success': reload_places
                });
            }else{
                ajax_call({
                    'url': '/places',
                    'type': 'post',
                    'data': place,
                    'success': reload_places
                });
            }
        }
    }

    function delete_place(){
        var to_remove = {'id': parseInt($(this).attr("place_id")), 'name': $(this).attr('name')};
        ajax_call({
            'url': '/places',
            'type': 'delete',
            'data': to_remove,
            'success': function(){
                reload_places();
            }
        });
    }

    function edit_place(){
        reset_places_form();
        var place_id = $(this).attr("place_id");
        var place_dom = $(this).parent().parent();
        $("#modal_add_place").text('Update');
        $("#add_places_modal .modal-title").text("Update a Place");
        $("#add_place_form").attr("place_id", place_id);

        $('#add_place_name').val($.trim($(place_dom).find('.place_name').text()));
        $('#add_place_address').val($.trim($(place_dom).find('.place_address').text()));

        var place_email = $(place_dom).find('.place_mail').text();
        if( place_email.indexOf('Unknown') == -1 )
            $('#add_place_email').val($.trim(place_email));

        var place_phone = $(place_dom).find('.place_phone').text();
        if( place_phone.indexOf('Unknown') == -1 )
            $('#add_place_phone').val($.trim(place_phone));
    }

    function add_handlers(){
        $('#modal_add_place').on('click', add_place);
        $('#add_places_btn').on('click', reset_places_form);
        $('#places_table_search').on('keyup', function(){
            delay(function(){
                page = 0;
                reload_places();
            }, 800 );
        });
        $('.table-sorter').on('click', function(){
            sort_toggle($(this));
            sort_by = $(this).attr('sorter');
            sort_dir = $(this).hasClass('fa-sort-down') == true ? 'desc' : 'asc';
            reload_places();
        });
        $('#place_next').on('click', next_page);
        $('#place_prev').on('click', last_page);
        search = $('#places_table_search');
    }
    $.when(
        ajax_load('/places', {}, function(data){places=data})
    ).done(function(){
        $(page_main).html(places_tmpl());
        draw_places(places);
        add_handlers();
        load_components();
    });
}

function load_settings(){
    $(page_main).html(settings_tmpl());
    load_settings_people();
    load_components();
}

function load_notifications(){
    $(page_main).html(notifications_tmpl());
}

function load_events(){
    $(page_main).html(events_tmpl());
}

function load_settings_people(){

    function reset_form(){
        reset_components();
        $("#modal_add_role_btn").text("Add");
        $("#add_role_name").val("");
        $('#role_colour span').first().click();
        $("#add_role_form").attr('role_id', '');
        $('#modal_add_role_btn').off('click');
        $('#add_role_modal').modal('hide');
    }

    function edit_role(){
        reset_form();
        add_handlers();
        $('#add_role_modal').modal('show');
        $("#modal_add_role_btn").text("Update");
        $("#add_role_form").attr('role_id', $(this).attr('role_id'));
        $("#add_role_name").val($(this).attr('name'));
        $('#role_colour span.label-' + $(this).attr('theme')).click();
        var permissions = $(this).attr('permissions').split(',');
        for( var i in permissions ){
            $('#add_role_form .btn[value="' + permissions[i] + '"]').click();
        }
    }

    function save_role(e){
        e.preventDefault();

        var role_id = $('#add_role_form').attr('role_id');

        var data = {
            'theme': $('#role_colour .color-choice.selected').attr('value'),
            'name': $('#add_role_name').val(),
            'permissions': []
        };

        if( data.name.length > 0 ) {

            $('#add_role_form .btn-choice .btn.selected').each(function () {
                var dom_permissions = $(this).attr('value');
                if (dom_permissions != undefined) {
                    var split_permissions = dom_permissions.split(' ');
                    for (var i in split_permissions) {
                        data.permissions.push(split_permissions[i]);
                    }
                }
            });

            data.permissions = JSON.stringify(data.permissions);

            if ( role_id.length > 0 ){
                data.id = role_id;
                ajax_call({
                    'url': 'roles',
                    'data': data,
                    'type': 'PUT',
                    'success': load_roles
                });
            }else{
                ajax_call({
                    'url': 'roles',
                    'data': data,
                    'type': 'POST',
                    'success': load_roles
                });
            }

        }
    }

    function delete_role(){
        ajax_call({
            'url': 'roles',
            'type': 'delete',
            'data': {
                'id': $(this).attr('role_id')
             },
            'success': load_roles
        });
    }

    function draw_roles(input){
        if( input.length > 0 ){
            $('#role_table_holder').html(people_type_table_tmpl({'types': input}));
        }else{
            $('#role_table_holder').html(no_data_tmpl({
                'caption': 'There are no People-Types configured. Add some now!'
            }));
        }
        $('#role_table_body i.delete-btn').on('click', delete_role);
        $('#role_table_body i.edit-btn').on('click', edit_role);
        $('#add_role_btn').on('click', open_modal);
    }

    function open_modal(){
        reset_form();
        add_handlers();
    }

    function add_handlers(){
        load_components();
        $('#modal_add_role_btn').on('click', save_role);
    }

    function load_roles(){
        reset_form();
        ajax_call({
            'url': 'roles',
            'notify': false,
            'success': draw_roles
        });
    }

    load_roles();
}