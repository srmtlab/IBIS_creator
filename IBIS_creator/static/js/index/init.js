function show_create_theme_modal() {
    $("#create_theme_modal").modal();
}

function create_theme() {

    if(!document.getElementById("create-theme-name").value.trim() || !document.getElementById("create-theme-description").value.trim()){
        alert("入力に不備があります");
        return;
    }

    document.createTheme.submit();

    $('#create_theme_modal').modal('hide');
}

window.onload = function () {
    $("#create_theme_modal").on('hidden.bs.modal', function (e) {
        document.getElementById("create-theme-name").value = "";
        document.getElementById("create-theme-description").value = "";
    });
};