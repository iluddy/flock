/* Constants */
var FADE = 500;
var TASK_DELAY = 800;

/* Globals */
var fetch_function = null;
var sort_by = "score";
var product_total;
var sort_dir = -1;
var page = 0;
var tasks = {};
var stats = {};
var page_title, page_main;
var pizza_info = {};
var side_info = {};
var vendor_info = ["Dominos Pizza", "Four Star Pizza", "Papa Johns", "Pizza Hut"];
var title_tmpl, filter_group_tmpl, table_page_tmpl, spinner_tmpl, no_result_tmpl, side_grid_tmpl, pizza_grid_tmpl;
var count_tmpl, range_filter_group_tmpl, about_tmpl;
var ajax_loading = false;

$(document).ready(function () {
    ajax_load("vendors", {}, function(input){vendor_info = input;}, 5000);
    ajax_load("stats", {}, update_counts);
    page_main = $("#page_main");
    page_title = $("#page_title");
    setInterval(run_tasks, TASK_DELAY);
    toaster("Hello!", "Use the filters to compare Pizzas from around the country :)");
    $.when(
        ajax_load('templates.html', {}, attach_templates)
    ).done(templates_loaded);
});

/* About */

function load_about_page(){
    $(page_main).append(about_tmpl());
}

/* Sides */

function load_sides_page(){
    ajax_loading = true;
    show_loader($("body"), function(){
        $.when(
            ajax_load("sides/types", {}, function(input){side_info["types"] = input;}),
            ajax_load("sides/prices", {}, function(input){side_info["prices"] = input;})
        ).done(function(){
            draw_product_page(add_side_filters, fetch_sides, false);
            product_total = stats["sides"]; // Total count for current selection
        });
    });
}

function add_side_filters(){
    add_filter("vendors", vendor_info, "active");
    add_filter("types", side_info["types"]);
    add_range_filter("price", side_info["prices"].min, side_info["prices"].max, 1,  "&#8364; ");
}

function fetch_sides(){
    fetch("sides", fetch_sides_parameters, side_grid_tmpl);
}

function fetch_sides_parameters(){
    return {
        "vendor": JSON.stringify(get_filter("vendors")),
        "type": JSON.stringify(get_filter("types")),
        "price": JSON.stringify(get_range_filter("price")),
        "page": page,
        "sort_by": "price", // Only sortable on price for the moment
        "sort_dir": sort_dir,
    };
}

/* Pizza */

function load_pizza_page(){
    ajax_loading = true;
    show_loader($("body"), function(){
        $.when(
            ajax_load("pizza/bases", {}, function(input){pizza_info["bases"] = input;}),
            ajax_load("pizza/toppings", {}, function(input){pizza_info["toppings"] = input;}),
            ajax_load("pizza/styles", {}, function(input){pizza_info["styles"] = input;}),
            ajax_load("pizza/sizes", {}, function(input){pizza_info["sizes"] = input;}),
            ajax_load("pizza/prices", {}, function(input){pizza_info["prices"] = input;}),
            ajax_load("pizza/scores", {}, function(input){pizza_info["scores"] = input;}),
            ajax_load("pizza/diameters", {}, function(input){pizza_info["diameters"] = input;}),
            ajax_load("pizza/slices", {}, function(input){pizza_info["slices"] = input;})
        ).done(function(){
            draw_product_page(add_pizza_filters, fetch_pizza, true);
            product_total = stats["pizza"]; // Total count for current selection
        });
    });
}

function add_pizza_filters(){
    add_filter("vendors", vendor_info, "active");
    add_filter("crusts", pizza_info["bases"], "active");
    add_filter("toppings", pizza_info["toppings"], "");
    add_range_filter("score", pizza_info["scores"].min, pizza_info["scores"].max, 1, "", "", "Score = Area * Toppings / Price");
    add_range_filter("price", pizza_info["prices"].min, pizza_info["prices"].max, 1,  "&#8364; ");
    add_range_filter("size", pizza_info["diameters"].min, pizza_info["diameters"].max, 0.5, "", '"');
    add_range_filter("slices", pizza_info["slices"].min, pizza_info["slices"].max, 2);
}

function fetch_pizza(){
    fetch("pizza", fetch_pizza_parameters, pizza_grid_tmpl, true);
}

function fetch_pizza_parameters(){
    return {
        "vendor": JSON.stringify(get_filter("vendors")),
        "base_style": JSON.stringify(get_filter("crusts")),
        "toppings": JSON.stringify(get_filter("toppings")),
        "diameter": JSON.stringify(get_range_filter("size")),
        "slices": JSON.stringify(get_range_filter("slices")),
        "price": JSON.stringify(get_range_filter("price")),
        "score": JSON.stringify(get_range_filter("score")),
        "page": page,
        "sort_by": sort_by,
        "sort_dir": sort_dir,
    };
}

/* Templates */

function templates_loaded(){
    attach_templates();
    compile_templates();
    add_tab_handlers();
}

function compile_templates(){
    title_tmpl = Handlebars.compile($("#title_tmpl").html());
    filter_group_tmpl = Handlebars.compile($("#filter_group_tmpl").html());
    range_filter_group_tmpl = Handlebars.compile($("#range_filter_group_tmpl").html());
    table_page_tmpl = Handlebars.compile($("#table_page_tmpl").html());
    about_tmpl = Handlebars.compile($("#about_tmpl").html());
    spinner_tmpl = Handlebars.compile($("#spinner_tmpl").html());
    no_result_tmpl = Handlebars.compile($("#no_result_tmpl").html());
    pizza_grid_tmpl = Handlebars.compile($("#pizza_grid_tmpl").html());
    side_grid_tmpl = Handlebars.compile($("#side_grid_tmpl").html());
    count_tmpl = Handlebars.compile($("#count_tmpl").html());
}

function attach_templates(input){
    $("#tmpl_holder").html(input);
}

/* Filters */

function add_filter(id, items, active){
    $(get_filter_wrapper()).append(filter_group_tmpl({
        "id": id,
        "title": id.toUpperCase(),
        "items": items,
        "active": active
    }));
}

function add_range_filter(id, min, max, step, prefix, postfix, help){
    $(get_filter_wrapper()).append(range_filter_group_tmpl({
        "id": id,
        "title": id.toUpperCase(),
        "help": help
    }));
    $("#" + id + "_range").ionRangeSlider({
        min: min,
        max: max,
        type: 'double',
        step: step,
        prefix: prefix,
        postfix: postfix,
        maxPostfix: "",
        prettify: true,
        hasGrid: true,
        onFinish: function(){queue_task(fetch_function)}
    });
}

function create_filters() {
    $(".sl-btn").on("click", function () {
        $(this).toggleClass("sl-btn-active")
    });
}

function add_filter_handler(){
    $(get_filter_wrapper()).on("click.filter", ".sl-btn", function(){queue_task(fetch_function)});
}

function remove_filter_handler(){
    $(get_filter_wrapper()).off("click.filter", ".sl-btn");
}

function get_filter(id){
    var filtered = [];
    $("#" + id + " .sl-btn-active").each(function(){filtered.push($(this).attr("filter_id"))});
    if (filtered.length > 0)
        return filtered;
    return undefined;
}

function get_range_filter(id){
    var range = $("#" + id + "_range").attr("value").split(";");
    return [parseFloat(range[0]), parseFloat(range[1])];
}

/* Page */

function add_tab_handlers(){
    $("#tabs > h3").on("click", function(){
        if( !$(this).hasClass("active") && !ajax_loading){
            $(this).addClass("active").siblings("h3").removeClass("active");
            clear();
            window[$(this).attr("target")]();
        }
    });
    $("#tabs > h3").first().click();
}

function update_counts(input){
    stats = input;
}

function draw_product_page(add_filters, fetcher, show_score_sorter){
    fetch_function = fetcher;
    $(page_main).append(table_page_tmpl({"show_score_sorter": show_score_sorter}));
    sort_dir = -1;
    remove_filter_handler();
    add_filters();
    add_filter_handler();
    create_filters();
    add_sort_handlers();
    fetcher();
    $(document).ajaxStart(function() { Pace.restart(); });
}

function no_result(){
    get_table_wrapper().empty().append(no_result_tmpl());
    hide_count();
}

function clear(){
    $(page_title).empty();
    $(page_main).empty();
}

function get_table_wrapper(){
    return $("#sl-table-wrapper");
}

function get_filter_wrapper(){
    return $("#sl-filter-wrapper");
}

function update_count(count, total){
    $("#sl-table-count").html(count_tmpl({
        "visible": $(".sl-grid-product").length,
        "count": count,
        "total": total,
        "filtered": count != total
    }));
}

function hide_count(){
    $("#sl-table-count").empty();
}

/* Sorting */

function add_sort_handlers(){
    $("#sl-sort-desc").on("click", sort_dir_handler);
    $("#sl-sort-asc").on("click", sort_dir_handler);
    $("#sl-sort-by li a").on("click", sort_by_handler);
}

function sort_by_handler(){
    var sort_value = $(this).text();
    sort_by = sort_value.toLowerCase();
    $("#sl-sorted-by-label").text(sort_value);
    refresh_data();
}

function sort_dir_handler(){
    $(this).addClass("btn-primary").removeClass("btn-white");
    $(this).siblings().addClass("btn-white").removeClass("btn-primary");
    sort_dir = $(this).attr("sort_dir");
    refresh_data();
}

/* Loading */

function fetch(endpoint, param_func, template, show_score_option){
    haze_load(get_table_wrapper(), function(){
        ajax_load(endpoint, param_func(), function(input){
            if( input.data.length > 0 ){
                get_table_wrapper().empty();
                get_table_wrapper().prepend(
                    template({
                        "items": input["data"],
                        "count": input["count"],
                        "score_sort": show_score_option
                    })
                );
                update_count(input["count"], product_total);
            }else{
                no_result();
            }
            hide_haze(get_table_wrapper());
            hide_loader($("body"));
            ajax_loading = false;
        })
    });
}

function refresh_data(){
    fetch_function(0);
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

function show_loader(dom, func){
    $("#spinner").remove();
    $(dom).append($(spinner_tmpl()).fadeIn(FADE));
    setTimeout(func, FADE);
}

function haze_load(dom, func){
    $(dom).animate({"opacity": 0.4}, FADE);
    setTimeout(func, FADE);
}

function hide_loader(){
    setTimeout(function(){
        $("#spinner").fadeOut(FADE, function(){$(this).remove()});
    });
}

function hide_haze(dom){
    setTimeout(function(){
        $(dom).animate({"opacity": 1}, FADE);
    });
}

/* Notifications */

function toaster(title, message){
    setTimeout(function() {
        toastr.options = {
            closeButton: true,
            progressBar: true,
            showMethod: 'slideDown',
            timeOut: 4000
        };
        toastr.info(message, title);
    }, 1300);
}

/* Task Manager */

function run_tasks(){
    for( var func_id in tasks ){
        var task = tasks[func_id];
        if( task["stamp"] != undefined && task["stamp"] < Date.now() ){
            task["stamp"] = undefined;
            async(task["func"]);
        }
    }
}

function queue_task(func){
    tasks[func.name] = {
        "stamp": Date.now() + TASK_DELAY,
        "func": func
    }
}

function async(func){
    setTimeout(func, 0);
}

