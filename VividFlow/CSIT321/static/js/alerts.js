
var alert_info_timeout = null;
var alert_error_timeout = null;

function display_error_alert(message="", timeout=5) {
    $("#alert-danger-content").text(message);
    $(".alert-danger").show('slow');

    clearTimeout(alert_error_timeout);
    alert_error_timeout = setTimeout(function() {
        $(".alert-danger").hide('slow');
    }, 5000);
}

function dismiss_error_alert() {
    clearTimeout(alert_error_timeout);
    $(".alert-danger").hide('fast');
}

function display_info_alert(message="", timeout=5) {
    $("#alert-info-content").text(message);
    $(".alert-info").show('slow');

    clearTimeout(alert_info_timeout);
    alert_info_timeout = setTimeout(function() {
        $(".alert-info").hide('slow');
    }, 5000);
}

function dismiss_info_alert() {
    clearTimeout(alert_info_timeout);
    $(".alert-info").hide('fast');
}
