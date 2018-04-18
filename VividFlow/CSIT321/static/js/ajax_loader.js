
var ajax_loader_stylesheet_added = false;
var ajax_loader_div_added = false;

function add_ajax_loader_css(filename) {
   var link = '<link rel="stylesheet" type="text/css" href="' + filename + '">'
   $('head').append(link)
}

function add_ajax_loader_stylesheet() {
    if(ajax_loader_stylesheet_added == true) {
        return;
    }
    ajax_loader_stylesheet_added = true;
    add_ajax_loader_css("/static/css/ajax_loader.css");
}

function add_ajax_loader_div() {
    if(ajax_loader_div_added == true) {
        return;
    }
    ajax_loader_div_added = true;
    let html = '<div id="loading-modal" class="modalbackground">';
    html += '<img src="/static/images/ajax-loader.gif" id="loading-indicator" />';
    html += '</div>';

    $( "body" ).append( html );
}

function setup_ajax_loader() {
    add_ajax_loader_stylesheet();
    add_ajax_loader_div();
    hide_ajax_loader();
}

function show_ajax_loader() {
    //steal focus
    setup_ajax_loader();
    $("#loading-modal").show();
    //steal focus again
}

function hide_ajax_loader() {
    $("#loading-modal").hide();
}
