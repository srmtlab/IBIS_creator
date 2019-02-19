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