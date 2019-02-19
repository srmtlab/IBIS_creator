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


/*
refer to d3-hierarchy document from https://github.com/d3/d3-hierarchy if you want to know d3-hierarchy
below code is made by using
https://wizardace.com/d3-collapsible-tree/
https://bl.ocks.org/adamfeuer/042bfa0dde0059e2b288
https://stackoverflow.com/questions/32327489/error-invalid-value-for-g-attribute-transform-translateundefined-undefined
as a reference
*/

let g, root, modal_obj, theme_obj, relevant_info_index;
let ibis_width, ibis_height, navvar_height;
let scale = 1, current_gx, current_gy, translate_x = 0, translate_y = 0;
let init_flag = true;
let connection = null;

function resize_ibis() {
    navvar_height = document.getElementById("navvar").offsetHeight + 10;
    let window_height = window.innerHeight;

    let ibis =　document.getElementById("ibis");
    ibis.style.height = ( window_height - navvar_height - 5 ) + "px";

    ibis_width = ibis.clientWidth;
    ibis_height = ibis.clientHeight;
}

let zoom = function() {
    translate_x = d3.event.transform.x;
    translate_y = d3.event.transform.y;
    scale = d3.event.transform.k;

    g.attr("transform", "translate(" + (current_gx*scale + translate_x) + "," + (current_gy*scale + translate_y)
        + ") scale(" + scale + ")");
};

function init_data(websocket_url) {
    // this function gets conversation data from server
    let ibis = $("#ibis");
    ibis_width = ibis.width();
    ibis_height = ibis.height();
    navvar_height = $("#navvar").outerHeight(true);

    connection = new WebSocket(websocket_url);

    connection.onopen = function(e) {
        connection.send(JSON.stringify({
            'status': 'init'
        }));
    };

    connection.onmessage =function (e) {
        let data = JSON.parse(e.data);
        let status = data["status"];
        if(init_flag && status === "init"){
            theme_obj = data["theme"];

            let ibisData = data['node'];

            //Constructs a root node from the hierarchical data "ibisData"
            root = d3.hierarchy(ibisData);

            g = d3.select("#ibis").append("g");

            d3.select("#ibis")
                .call(
                    d3.zoom()
                        .scaleExtent([1 / 8, 12])
                        .on("zoom", zoom)
                )
                .on("dblclick.zoom", null);

            update(root);
        }else if (status === "work"){
            let type = data["type"];
            let operation = data["operation"];
            let data = data["data"];

            if(type === "theme")
            {
                if(operation === "edit")
                {
                    edit_theme(data);
                }
            }
            else if(type === "node")
            {
                if(operation === "add")
                {
                    add_node(data);
                }
                else if(operation === "delete")
                {
                    delete_node(data)
                }
                else if(operation === "edit")
                {
                    edit_node(data)
                }
            }
            else if(type === "relevant_info")
            {
                if(operation === "add")
                {
                    add_relevant_info(data)
                }
                else if(operation === "delete")
                {
                    delete_relevant_info(data)
                }
                else if(operation === "edit")
                {
                    edit_relevant_info(data)
                }
            }
        }
    };

    connection.onerror = function(error) {
        console.log(error);
    };

}

function tr_default(tblID){
    let vTR = tblID + " tr";
    $(vTR).css("background-color","#ffffff");
}

function tr_click(trID){
    trID.css("background-color","#bce2e8");
    $("#relevant-info-details-buttons button").prop("disabled", false);
    relevant_info_index = Number(trID.children('td').attr('data-relevant_info_index'));
}

window.addEventListener("resize", resize_ibis);

window.onload = function () {
    resize_ibis();

    //let theme_url = base_url + "/api/theme/" + theme_id + "/";
    //let node_url = base_url + "/api/theme/" + theme_id + "/node/";
    let websocket_url = "ws://" + location.host + base_url + "/ws/theme/" + theme_id + "/";

    init_data(websocket_url);


    $("#add-node").on('hidden.bs.modal', function () {
        document.getElementById("add-node-name").value = "";
        document.getElementById("add-node-type").value = "unselected";
        document.getElementById("add-node-description").value = "";
    });

    $("#relevant-info").on('hidden.bs.modal', function () {
        let relevant_info_details = document.getElementById("relevant-info-details");
        let relevant_info_searches = document.getElementById("relevant-info-searches");

        relevant_info_details.parentNode.removeChild(relevant_info_details);
        relevant_info_searches.parentNode.removeChild(relevant_info_searches);

        document.getElementById("relevant-info-searches-buttons").style.display="block";
        $("#relevant-info-details-buttons > .btn-danger").prop("disabled", true);
        $("#relevant-info-details-buttons > .btn-success").prop("disabled", true);
    });

    $("#delete-relevant-info").on('hidden.bs.modal', function () {
        show_relevant_info(modal_obj);
    });

    $("#add-relevant-info").on('hidden.bs.modal', function () {
        document.getElementById("add-relevant-info-url").value = "";
        document.getElementById("add-relevant-info-title").value = "";
        show_relevant_info(modal_obj);
    });

    $("#edit-relevant-info").on('hidden.bs.modal', function () {
        show_relevant_info(modal_obj);
    });
};