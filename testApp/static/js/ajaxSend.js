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

$(function () {
    let $btn = $('#send');
    $btn.on('click', () => {
        let $email = $('#email');
        let $text = $('#text');
        $.ajax({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            },
            url: '/send',
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            type: 'post',
            data: JSON.stringify({
                email: $email.val(),
                text: $text.val(),
            }),
            success: function(data) {
                console.log('success', data);
            },
            failure: function(data) {
                console.log('failure', data);
            }
        });
    })

});