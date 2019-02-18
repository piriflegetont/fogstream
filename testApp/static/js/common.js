function getCookie(name) {
    if (typeof document.cookie === 'undefined' || document.cookie.length === 0) {
        return null;
    }
    let cookies = document.cookie.split(';');
    cookies = cookies.filter(cookie => ~cookie !== name);
    cookies = cookies.map((item) => {
        let cookie = jQuery.trim(item);
        cookie = cookie.split('=');
        return {name: cookie[0], value: decodeURIComponent(cookie[1])}
    })
    if (cookies.length === 1 && cookies[0].name === name)
        return cookies[0].value
    return null;
}
function csrfSafeMethod (method) {return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);}

function sendError($label, message) {
    $label.addClass('error');
    $label.removeClass('success');
    $label.text(message);
    if(!$label.is(':visible'))
        $label.slideToggle("slow");
}

function sendSuccess($label, message) {
    $label.removeClass('error');
    $label.addClass('success');
    $label.text(message);
    if(!$label.is(':visible'))
        $label.slideToggle("slow");
}