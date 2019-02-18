$(function () {
    $('#do_login').on('click', () => {
        let $login = $('#login');
        let $password = $('#password');
        let $result = $('#result');
        if($result.is(':visible'))
            $result.toggle();
        $('#result').ajaxError(function(e) {
            sendError($(this), e.type);
        });
        $.ajax({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            },
            url: '/login',
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            type: 'post',
            data: JSON.stringify({
                login: $login.val(),
                password: $password.val(),
            }),
            success: function(data) {
                if (typeof data === 'object' && Boolean(data.error)) {
                    sendError($result, data.error);
                } else {
                    window.location.href = data.url;
                }
            },
            failure: function(data) {
                sendError($result, data.error);
            }
        });
    })
    $('#do_register').on('click', () => {
        let $login = $('#reg_login');
        let $password = $('#reg_password');
        let $passwordRepeat = $('#reg_repeat');
        let $result = $('#result');
        if($result.is(':visible'))
            $result.toggle();
        $('#result').ajaxError(function(e) {
            sendError($(this), e.type);
        });
        $.ajax({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            },
            url: '/register',
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            type: 'post',
            data: JSON.stringify({
                login: $login.val(),
                password: $password.val(),
                repeat_password: $passwordRepeat.val()
            }),
            success: function(data) {
                if (typeof data === 'object' && Boolean(data.error)) {
                    sendError($result, data.error);
                } else {
                    let $authBtn = document.querySelector('div.tabs > a:nth-child(2)');
                    $authBtn.click();
                    sendSuccess($result, `Пользователь ${$login.val()} успешно зарегестрирован`);
                }
            },
            failure: function(data) {
                sendError($result, data.error);
            }
        });
    })
});