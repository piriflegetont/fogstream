$(function () {
    $('#logout').on('click', () => {
        let $result = $('#result');
        $.ajax({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            },
            url: '/logout',
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            type: 'post',
            success: function(data) {
                window.location.href = data.url;
            },
            failure: function(data) {
            }
        });
    })
    $('#send').on('click', () => {
        let $email = $('#email');
        let $text = $('#text');
        let $result = $('#result');
        if($result.is(':visible'))
            $result.toggle();
        $('#result').ajaxError(function(e) {
            sendError($(this), JSON.stringify(e.type));
        });
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
                if (typeof data === 'object' && Boolean(data.error)) {
                    sendError($result, `Ошибка при отправке письма ${data.error}`);
                } else {
                    sendSuccess($result, "Письмо успешно отправлено");
                }
            },
            failure: function(data) {
                sendError($result, `Ошибка при отправке письма ${data.error}`);
            }
        });
    })
});