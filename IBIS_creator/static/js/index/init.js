function show_create_theme_modal() {
    $("#create_theme_modal").modal();
}

function create_theme() {
    let theme_form = document.createTheme;

    if(theme_form.checkValidity() === false){
        theme_form.classList.add("was-validated");
        return;
    }
    document.createTheme.submit();

    $('#create_theme_modal').modal('hide');
}

window.onload = function () {
    $("#create_theme_modal").on('hidden.bs.modal', function (e) {
        document.getElementById("create-theme-name").value = "";
        document.getElementById("create-theme-description").value = "";
        document.createTheme.classList.remove("was-validated");
    });
};