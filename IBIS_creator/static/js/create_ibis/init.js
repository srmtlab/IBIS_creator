/*
refer to d3-hierarchy document from https://github.com/d3/d3-hierarchy if you want to know d3-hierarchy
below code is made by using
https://wizardace.com/d3-collapsible-tree/
https://bl.ocks.org/adamfeuer/042bfa0dde0059e2b288
https://stackoverflow.com/questions/32327489/error-invalid-value-for-g-attribute-transform-translateundefined-undefined
as a reference
*/

let g, root, modal_obj, theme_obj = null, relevant_info_obj;
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
        let receive_data = JSON.parse(e.data);
        let status = receive_data["status"];

        if(init_flag && status === "init"){
            theme_obj = receive_data["theme"];


            let ibisData = receive_data['node'];

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

            let type = receive_data["type"];
            let operation = receive_data["operation"];
            let data = receive_data["data"];

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

window.addEventListener("resize", resize_ibis);

window.onload = function () {
    resize_ibis();

    let websocket_url = "ws://" + location.host + "/ws/theme/" + theme_id + "/";

    init_data(websocket_url);

    $("#edit-theme").on('hidden.bs.modal', function () {
        document.editTheme.classList.remove("was-validated");
    });

    $("#add-node").on('hidden.bs.modal', function () {
        document.getElementById("add-node-name").value = "";
        document.getElementById("add-node-type").value = "";
        document.getElementById("add-node-description").value = "";
        document.addNode.classList.remove("was-validated");
    });

    $("#edit-node").on('hidden.bs.modal', function () {
        document.editNode.classList.remove("was-validated");
    });

    $("#delete-relevant-info").on('hidden.bs.modal', function () {
        show_relevant_info(modal_obj);
    });

    $("#add-relevant-info").on('hidden.bs.modal', function () {
        document.getElementById("add-relevant-info-url").value = "";
        document.getElementById("add-relevant-info-title").value = "";
        document.addRelevantInfo.classList.remove("was-validated");
        show_relevant_info(modal_obj);
    });

    $("#edit-relevant-info").on('hidden.bs.modal', function () {
        document.editRelevantInfo.classList.remove("was-validated");
        show_relevant_info(modal_obj);
    });
};