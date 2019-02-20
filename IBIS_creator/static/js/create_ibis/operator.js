function data_formatting(status, type, operation, data) {
    return {
        "status" : status,
        "type" : type,
        "operation" : operation,
        "data" : data
    }
}

/* start edit theme */
function show_edit_theme() {
    document.getElementById("edit-theme-name").value = theme_obj["name"];
    document.getElementById("edit-theme-description").value = theme_obj["description"];

    $('#edit-theme').modal();
}

function send_edit_theme() {

    if(!document.getElementById("edit-theme-name").value.trim() || !document.getElementById("edit-theme-description").value.trim()){
        alert("入力に不備があります");
        return;
    }

    // let old_theme_obj = Object.assign({}, theme_obj);
    theme_obj["name"] = document.getElementById("edit-theme-name").value;
    theme_obj["description"] = document.getElementById("edit-theme-description").value;

    document.getElementById("navvar").firstElementChild.innerText = theme_obj["name"];
    document.title = theme_obj["name"];

    let json_data = {
        'name' : theme_obj["name"],
        'description' : theme_obj["description"]
    };
    let edit_data = data_formatting("work","theme","edit",json_data);
    connection.send(JSON.stringify(edit_data));

    $('#edit-theme').modal('hide');
}

function edit_theme(data) {
    theme_obj["name"] = data["name"];
    theme_obj["description"] = data["description"];

    document.getElementById("navvar").firstElementChild.innerText = theme_obj["name"];
    document.title = theme_obj["name"];
}
/* end edit theme */

/* start add node */
function show_add_node(d) {
    modal_obj = d;
    $('#add-node').modal();

    $(".modal-backdrop")
        .css({
            top: navvar_height + "px",
            left: 5 + "px", // 5px is #ibis side's margin
            right: 5 + "px",
            bottom: 5 + "px"
        });

    $(".modal")
        .css({
            top: navvar_height + "px",
            left: 5 + "px", // 5px is #ibis side's margin
            right: 5 + "px",
            bottom: 5 + "px"
        });
}

function send_add_node(d) {

    if(!document.getElementById("add-node-name").value.trim() || document.getElementById("add-node-type").value === "unselected"){
        alert("入力に不備があります");
        return;
    }

    let node_name = document.getElementById("add-node-name").value;
    let node_type = document.getElementById("add-node-type").value;
    let node_description = document.getElementById("add-node-description").value;

    let json_data = {
        'node_name' : node_name,
        'node_type' : node_type,
        "node_description": node_description,
        'parent_id' : d.data.id
    };
    let add_data = data_formatting("work","node","add",json_data);
    connection.send(JSON.stringify(add_data));

    $('#add-node').modal('hide');
    modal_obj = undefined;
}

function add_node(data) {

    let parent_node = null;
    let node_list = root.descendants();

    for(let i in node_list){
        if(node_list.hasOwnProperty(i)){
            if(node_list[i].id === data["parent_id"]){
                parent_node = node_list[i];
                break;
            }
        }
    }

    let node =
        d3.hierarchy(
            {
                'id' : data["node_id"],
                'name' : data["node_name"],
                'type' : data["node_type"],
                "description": data["node_description"],
                'relevant' : {},
                'children' : []
            }
        );

    node.parent = parent_node;
    node.children = undefined;
    node.depth = parent_node.depth + 1;

    if(parent_node.children !== undefined || parent_node._children !== undefined)
    {
        //if parent_node already has child node

        if(parent_node.children !== undefined)
        {
            parent_node.children.push(node);
            parent_node._children = undefined;
        }
        else if(parent_node._children !== undefined)
        {
            parent_node._children.push(node);
            parent_node.children = undefined;
        }

    }
    else
    {
        //if parent_node still hasn't child node
        parent_node.children= [];
        parent_node.children.push(node);
    }

    parent_node.data.children.push(node.data);
    update(parent_node, true);
}
/* end add node */

/* start delete node */
function show_delete_node(d) {
    modal_obj = d;
    $("#delete-modal-body").html("ノード : <span style=\"color:red\">" + d.data.name + "</span>&nbspを削除しますか？");
    $('#delete-node').modal();

    $(".modal-backdrop")
        .css({
            top: navvar_height + "px",
            left: 5 + "px", // 5px is #ibis side's margin
            right: 5 + "px",
            bottom: 5 + "px"
        });

    $(".modal")
        .css({
            top: navvar_height + "px",
            left: 5 + "px", // 5px is #ibis side's margin
            right: 5 + "px",
            bottom: 5 + "px"
        });
}

function send_delete_node(d) {

    if(d.parent !== null)
    {

        let json_data = {
            'node_id' : d.data.id
        };
        let delete_data = data_formatting("work","node","delete",json_data);
        connection.send(JSON.stringify(delete_data))
    }
    modal_obj = undefined;
}
function delete_node(data) {

    let delete_node = null;
    let node_list = root.descendants();

    for(let i in node_list){
        if(node_list.hasOwnProperty(i)){
            if(node_list[i].id === data["node_id"]){
                delete_node = node_list[i];
                break;
            }
        }
    }

    let parent = delete_node.parent;
    let array_num = delete_node.parent.children.indexOf(delete_node);
    parent.children.splice(array_num,1);
    parent.data.children.splice(array_num,1);
    if(parent.children.length === 0){
        parent.children = undefined;
        parent._children  = undefined;
    }
    update(delete_node,true);
}
/* end delete node */

/* start edit node */
function show_edit_node(d) {
    modal_obj = d;

    document.getElementById("edit-node-name").value = d.data.name;
    document.getElementById("edit-node-type").value = d.data.type;
    document.getElementById("edit-node-description").value = d.data.description;

    $('#edit-node').modal();

    $(".modal-backdrop")
        .css({
            top: navvar_height + "px",
            left: 5 + "px", // 5px is #ibis side's margin
            right: 5 + "px",
            bottom: 5 + "px"
        });

    $(".modal")
        .css({
            top: navvar_height + "px",
            left: 5 + "px", // 5px is #ibis side's margin
            right: 5 + "px",
            bottom: 5 + "px"
        });

}

function send_edit_node(d) {
    if(!document.getElementById("edit-node-name").value.trim()){
        alert("入力に不備があります");
        return;
    }

    let node_name = document.getElementById("edit-node-name").value;
    let node_type = document.getElementById("edit-node-type").value;
    let node_description = document.getElementById("edit-node-description").value;

    let json_data = {
        'node_id' : d.data.id,
        'node_name' : node_name,
        'node_type' : node_type,
        'node_description' : node_description
    };
    let edit_data = data_formatting('work','node','edit',json_data);
    connection.send(JSON.stringify(edit_data));

    $('#edit-node').modal('hide');
    modal_obj = undefined;
}
function edit_node(data) {
    let edit_node = null;
    let node_list = root.descendants();

    for(let i in node_list){
        if(node_list.hasOwnProperty(i)){
            if(node_list[i].id === data["node_id"]){
                edit_node = node_list[i];
                break;
            }
        }
    }

    edit_node.data.name = data["node_name"];
    edit_node.data.type = data["node_type"];
    edit_node.data.description = data["node_description"];
    update(edit_node, true);
}
/* end edit node */

/* start relevant_info */
function show_relevant_info(d) {
    modal_obj = d;

    let relevantData = d.data.relevant;
    if(relevantData.length !== 0) {
        // if relevantData is not empty
        let table_relevant_info_details = document.createElement('table');
        table_relevant_info_details.setAttribute('id','relevant-info-details');
        table_relevant_info_details.setAttribute('class','table table-sm table-hover table-responsive');


        for(let i in relevantData) {
            if(relevantData.hasOwnProperty(i)){
                let relevantData_url = relevantData[i].url;
                let relevantData_title = relevantData[i].title;

                let tr = document.createElement('tr');
                let td = document.createElement('td');
                td.setAttribute("data-relevant_info_index", i);
                let url_pattern = new RegExp('^https?:\\/\\/[^\\n]+$/i');
                if(url_pattern.test(relevantData_url)){
                    td.setAttribute("ondblclick","window.open().location.href='"+ relevantData_url + "'");
                }
                td.innerText = relevantData_title;
                tr.append(td);
                table_relevant_info_details.append(tr);
            }
        }

        let div_relevant_info_buttons = document.getElementById("relevant-info-details-buttons");
        div_relevant_info_buttons.parentNode.insertBefore(table_relevant_info_details, div_relevant_info_buttons);
        $("#relevant-info-details tr").click(function(){
            tr_default("#relevant-info-details");
            tr_click($(this));
        });
    }else {
        // if relevantData is empty
        let p_relevant_info_details = document.createElement('p');
        p_relevant_info_details.setAttribute('id','relevant-info-details');
        p_relevant_info_details.setAttribute('class','text-justify');
        p_relevant_info_details.innerText = "登録されている関連情報はありません";

        let div_relevant_info_buttons = document.getElementById("relevant-info-details-buttons");
        div_relevant_info_buttons.parentNode.insertBefore(p_relevant_info_details, div_relevant_info_buttons);
    }


    let query = d.data.name;
    let temp = d;
    while (true){
        if(!d.parent){
            break;
        }
        d = d.parent;
        query = query + ' ' + d.data.name;
    }
    d = temp;

    $.ajax({
        type: 'GET',
        dataType: 'json',
        url: base_url + "/api/relevant/search/?q=" + query
    }).done(function(d){
        // if data sending is successful
        if(d.query.length !== 0){
            let table_relevant_info_searches = document.createElement('table');
            table_relevant_info_searches.setAttribute('id','relevant-info-searches');
            table_relevant_info_searches.setAttribute('class','table table-sm table-responsive');
            let query_list = d.query;

            for(let i in query_list) {
                if(query_list.hasOwnProperty(i)){
                    let tr = document.createElement('tr');

                    let td_input = document.createElement('td');
                    let queryCheckbox = document.createElement('input');
                    queryCheckbox.setAttribute("name", "searchQuery");
                    queryCheckbox.setAttribute("type", "checkbox");
                    queryCheckbox.setAttribute("value", query_list[i]);
                    td_input.append(queryCheckbox);

                    let td_text = document.createElement('td');
                    td_text.innerText = query_list[i];

                    tr.append(td_input);
                    tr.append(td_text);

                    table_relevant_info_searches.append(tr);
                }
            }

            document.getElementById("relevant-info-searches-form")
                .insertBefore(table_relevant_info_searches,
                    document.getElementById("relevant-info-searches-buttons"));

            document.getElementById("relevant-info-searches-button").setAttribute('data-theme-id', theme_id);
            document.getElementById("relevant-info-searches-button").setAttribute('data-theme-name', theme_obj["name"]);
            document.getElementById("relevant-info-searches-button").setAttribute('data-node-name', modal_obj.data.name);
            document.getElementById("relevant-info-searches-button").setAttribute('data-node-id', modal_obj.data.id);

        }else{
            let p_relevant_info_searches = document.createElement('p');
            p_relevant_info_searches.setAttribute('id','relevant-info-searches');
            p_relevant_info_searches.setAttribute('class','text-justify');
            p_relevant_info_searches.innerText = "推薦される検索キーワードはありません";
            document.getElementById("relevant-info-searches-form").appendChild(p_relevant_info_searches);

            document.getElementById("relevant-info-searches-buttons").style.display="none";
        }
    }).fail(function(){
        // if data sending is failed
        alert("推薦キーワードを取得することができませんでした");
    });

    $('#relevant-info').modal();

    $(".modal-backdrop")
        .css({
            top: navvar_height + "px",
            left: 5 + "px", // 5px is #ibis side's margin
            right: 5 + "px",
            bottom: 5 + "px"
        });

    $(".modal")
        .css({
            top: navvar_height + "px",
            left: 5 + "px", // 5px is #ibis side's margin
            right: 5 + "px",
            bottom: 5 + "px"
        });
}

function show_add_relevant_info(d) {
    $('#relevant-info').modal('hide');
    $('#add-relevant-info').modal();
    $(".modal-backdrop")
        .css({
            top: navvar_height + "px",
            left: 5 + "px", // 5px is #ibis side's margin
            right: 5 + "px",
            bottom: 5 + "px"
        });

    $(".modal")
        .css({
            top: navvar_height + "px",
            left: 5 + "px", // 5px is #ibis side's margin
            right: 5 + "px",
            bottom: 5 + "px"
        });
}

function send_add_relevant_info(d) {

    if(!document.getElementById("add-relevant-info-title").value.trim() || !document.getElementById("add-relevant-info-url").value.trim()){
        alert("入力に不備があります");
        return;
    }

    let relevant_url = document.getElementById("add-relevant-info-url").value;
    let relevant_title = document.getElementById("add-relevant-info-title").value;

    let json_data = {
        'node_id' : d.data.id,
        'relevant_url' : relevant_url,
        "relevant_title": relevant_title
    };
    let add_data = data_formatting("work","relevant_info","add",json_data);
    connection.send(JSON.stringify(add_data));

    $('#add-relevant-info').modal('hide');
}

function add_relevant_info(data){

    let target_node = null;
    let node_list = root.descendants();

    for(let i in node_list){
        if(node_list.hasOwnProperty(i)){
            if(node_list[i].id === data["node_id"]){
                target_node = node_list[i];
                break;
            }
        }
    }
    let relevant_obj = {
        "id": data["relevant_id"],
        "url": data["relevant_url"],
        "title": data["relevant_title"]
    };

    target_node.data.relevant.push(relevant_obj);
}

function show_delete_relevant_info(index,d){
    let relevantData = d.data.relevant;

    $("#delete-relevant-info-body").html("関連情報 : <span style=\"color:red\">" + relevantData[index].title + "</span>&nbspを削除しますか？");

    $('#relevant-info').modal('hide');
    $('#delete-relevant-info').modal();
    $(".modal-backdrop")
        .css({
            top: navvar_height + "px",
            left: 5 + "px", // 5px is #ibis side's margin
            right: 5 + "px",
            bottom: 5 + "px"
        });

    $(".modal")
        .css({
            top: navvar_height + "px",
            left: 5 + "px", // 5px is #ibis side's margin
            right: 5 + "px",
            bottom: 5 + "px"
        });
}

function send_delete_relevant_info(index, d) {
    let relevantData = d.data.relevant;

    let json_data = {
        'relevant_id' : relevantData[index].id
    };
    let delete_data = data_formatting("work","relevant_info","delete",json_data);
    connection.send(JSON.stringify(delete_data));
}

function delete_relevant_info(data) {
    let target_node = null;
    let delete_index = null;
    let node_list = root.descendants();

    for(let i in node_list){
        if(node_list.hasOwnProperty(i)){
            if(node_list[i].id === data["node_id"]){
                target_node = node_list[i];
                break;
            }
        }
    }
    let relevantData_list = target_node.data.relevant;

    for(let i in relevantData_list){
        if(relevantData_list.hasOwnProperty(i)){
            if(relevantData_list[i].id === data["relevant_id"]){
                delete_index = i;
                break;
            }
        }
    }

    relevantData_list.splice(delete_index, 1);
}
function show_edit_relevant_info(index, d) {
    let relevantData = d.data.relevant;

    document.getElementById("edit-relevant-info-title").value = relevantData[index].title;
    document.getElementById("edit-relevant-info-url").value = relevantData[index].url;

    $('#relevant-info').modal('hide');
    $('#edit-relevant-info').modal();
    $(".modal-backdrop")
        .css({
            top: navvar_height + "px",
            left: 5 + "px", // 5px is #ibis side's margin
            right: 5 + "px",
            bottom: 5 + "px"
        });

    $(".modal")
        .css({
            top: navvar_height + "px",
            left: 5 + "px", // 5px is #ibis side's margin
            right: 5 + "px",
            bottom: 5 + "px"
        });
}

function send_edit_relevant_info(index, d) {
    let relevant = d.data.relevant[index];
    let relevant_url = document.getElementById("edit-relevant-info-url").value;
    let relevant_title = document.getElementById("edit-relevant-info-title").value;

    if(!relevant_title.trim() || !relevant_url.trim()){
        alert("入力に不備があります");
        return;
    }

    let json_data = {
        'node_id' : d.id,
        'relevant_id' : relevant.id,
        'relevant_url' : relevant_url,
        'relevant_title': relevant_title
    };
    let delete_data = data_formatting("work","relevant_info","edit",json_data);
    connection.send(JSON.stringify(delete_data));

    $('#edit-relevant-info').modal('hide');
}

function edit_relevant_info(data) {
    let target_node = null;
    let node_list = root.descendants();

    for(let i in node_list){
        if(node_list.hasOwnProperty(i)){
            if(node_list[i].id === data["node_id"]){
                target_node = node_list[i];
                break;
            }
        }
    }
    let relevantData_list = target_node.data.relevant;

    for(let i in relevantData_list){
        if(relevantData_list.hasOwnProperty(i)){
            if(relevantData_list[i].id === data["relevant_id"]){
                relevantData_list[i].url = data["relevant_url"];
                relevantData_list[i].title = data["relevant_title"];
                break;
            }
        }
    }
}

function search_info() {
    let flag = false;

    let searchQuery = "";
    for(let query of document.getElementsByName("searchQuery")) {
        if(query.checked){
            flag = true;
            searchQuery = searchQuery + "+" + query.value;
        }
    }

    if (!flag) {
        // 何も選択されていない場合の処理
        alert("項目が選択されていません。");
    }else{
        window.open(
            "https://www.google.co.jp/search?q=" + searchQuery,
            '_blank',
            'menubar=no,toolbar=yes,resizable=yes,width=700,height=500,top=100,left=100'
        );
    }
}
/* end relevant_info */