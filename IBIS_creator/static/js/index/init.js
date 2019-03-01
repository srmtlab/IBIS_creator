// start Cross Site Request Forgery protection (https://docs.djangoproject.com/en/1.7/ref/contrib/csrf/)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
let csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
// end Cross Site Request Forgery protection

function show_create_theme_modal() {
    $("#create_theme_modal").modal();
}

function create_theme() {

    if(!document.getElementById("create-theme-name").value.trim() || !document.getElementById("create-theme-description").value.trim()){
        alert("入力に不備があります");
        return;
    }

    document.createTheme.action = base_url + "/api/make_theme/";
    document.createTheme.submit();
    $.ajax({
        type: 'POST',
        url: base_url + "/api/make_theme/",
        data:
            {
                'name' : document.getElementById("create-theme-name").value,
                'description' : document.getElementById("create-theme-description").value
            },
    }).fail(function(data){
        // if data sending is failed
        alert("テーマの作成に失敗しました");
    });

    $('#create_theme_modal').modal('hide');
}

window.onload = function () {
    $("#create_theme_modal").on('hidden.bs.modal', function (e) {
        document.getElementById("create-theme-name").value = "";
        document.getElementById("create-theme-description").value = "";
    });
};