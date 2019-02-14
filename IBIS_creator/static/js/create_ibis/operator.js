/* start edit theme */
function show_edit_theme() {
    document.getElementById("edit-theme-name").value = theme_obj["name"];
    document.getElementById("edit-theme-description").value = theme_obj["description"];

    $('#edit-theme').modal();
}

function edit_theme() {

    if(!document.getElementById("edit-theme-name").value.trim() || !document.getElementById("edit-theme-description").value.trim()){
        alert("入力に不備があります");
        return;
    }

    let old_theme_obj = Object.assign({}, theme_obj);
    theme_obj["name"] = document.getElementById("edit-theme-name").value;
    theme_obj["description"] = document.getElementById("edit-theme-description").value;

    sendMessage("theme", "edit", theme_obj);

    document.getElementById("navvar").firstElementChild.innerText = theme_obj["name"];
    document.title = theme_obj["name"];


    $.ajax({
        type: 'POST',
        url: base_url + "/api/theme/" + theme_id + "/theme/edit/",
        data:
            {
                'name' : theme_obj["name"],
                'description' : theme_obj["description"]
            }
    }).done(function(){
        // if data sending is successful
        document.getElementById("navvar").firstElementChild.innerText = theme_obj["name"];
        document.title = theme_obj["name"];
    }).fail(function(){
        // if data sending is failed
        theme_obj = old_theme_obj;
        alert("テーマ編集エラー\nリロードしてください");
    });

    $('#edit-theme').modal('hide');
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

function add_node(d) {

    if(!document.getElementById("add-node-name").value.trim() || document.getElementById("add-node-type").value === "unselected"){
        alert("入力に不備があります");
        return;
    }

    let node_name = document.getElementById("add-node-name").value;
    let node_type = document.getElementById("add-node-type").value;
    let node_description = document.getElementById("add-node-description").value;

    $.ajax({
        type: 'POST',
        url: base_url + "/api/theme/" + theme_id + "/node/add/",
        data:
            {
                'node_name' : node_name,
                'node_type' : node_type,
                "node_description": node_description,
                'parent_id' : d.data.id
            }
    }).done(function(node_id){
        // if data sending is successful

        let node =
            d3.hierarchy(
                {
                    'id' : node_id,
                    'name' : node_name,
                    'type' : node_type,
                    "description": node_description,
                    'relevant' : {},
                    'children' : []
                }
            );

        node.parent = d;
        node.children = undefined;
        node.depth = d.depth + 1;

        if(d.children !== undefined || d._children !== undefined){
            //if d already has child node
            if(d._children !== undefined){
                d.children = d._children;
                d._children = undefined;
            }
        }else {
            //if d still hasn't child node
            d.children= [];
        }
        d.children.push(node);
        d.data.children.push(node.data);
        update(d, true);

    }).fail(function(){
        // if data sending is failed
        alert("追加エラー\nリロードしてください");
    });

    $('#add-node').modal('hide');
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

function delete_node(d) {

    if(d.parent !== null)
    {
        $.ajax({
            type: 'POST',
            url: base_url + "/api/theme/" + theme_id + "/node/delete/",
            data:
                {
                    'node_id' : d.data.id
                }
        }).done(function(){
            // if data sending is successful
            let parent = d.parent;
            let array_num = d.parent.children.indexOf(d);
            parent.children.splice(array_num,1);
            parent.data.children.splice(array_num,1);
            if(parent.children.length === 0){
                parent.children = undefined;
                parent._children  = undefined;
            }
            update(d,true);
        }).fail(function(){
            // if data sending is failed
            alert("削除エラー\nリロードしてください");
        });
    }
    modal_obj = undefined;
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

function edit_node(d) {
    if(!document.getElementById("edit-node-name").value.trim()){
        alert("入力に不備があります");
        return;
    }

    let node_name = document.getElementById("edit-node-name").value;
    let node_type = document.getElementById("edit-node-type").value;
    let node_description = document.getElementById("edit-node-description").value;

    $.ajax({
        type: 'POST',
        url: base_url + "/api/theme/" + theme_id + "/node/edit/",
        data:
            {
                'node_id' : d.data.id,
                'node_name' : node_name,
                'node_type' : node_type,
                "node_description": node_description
            }
    }).done(function(){
        // if data sending is successful
        d.data.name = node_name;
        d.data.type =node_type;
        d.data.description = node_description;
        update(d, true);
    }).fail(function(){
        // if data sending is failed
        alert("編集エラー\nリロードしてください");
    });

    $('#edit-node').modal('hide');
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

function add_relevant_info(d) {

    if(!document.getElementById("add-relevant-info-title").value.trim() || !document.getElementById("add-relevant-info-url").value.trim()){
        alert("入力に不備があります");
        return;
    }

    let relevant_url = document.getElementById("add-relevant-info-url").value;
    let relevant_title = document.getElementById("add-relevant-info-title").value;

    $.ajax({
        type: 'POST',
        url: base_url + "/api/theme/" + theme_id + "/relevant/add/",
        data:
            {
                'node_id' : d.data.id,
                'relevant_url' : relevant_url,
                "relevant_title": relevant_title,
            }
    }).done(function(relevant_info_id){
        // if data sending is successful

        let relevant_obj = {
            "id": relevant_info_id,
            "url": relevant_url,
            "title": relevant_title
        };

        d.data.relevant.push(relevant_obj);

    }).fail(function(){
        // if data sending is failed
        alert("関連情報追加エラー\nリロードしてください");
    });

    $('#add-relevant-info').modal('hide');
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

function delete_relevant_info(index, d) {
    /*
    let relevantData = d.data.relevant;
    relevantData.splice(index, 1);
    */
    let relevantData = d.data.relevant;

    $.ajax({
        type: 'POST',
        url: base_url + "/api/theme/" + theme_id + "/relevant/delete/",
        data:
            {
                'relevant_id' : relevantData[index].id
            }
    }).done(function(){
        // if data sending is successful
        relevantData.splice(index, 1);
    }).fail(function(){
        // if data sending is failed
        alert("関連情報削除エラー\nリロードしてください");
    });
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

function edit_relevant_info(index, d) {
    let relevant = d.data.relevant[index];
    let relevant_url = document.getElementById("edit-relevant-info-url").value;
    let relevant_title = document.getElementById("edit-relevant-info-title").value;

    if(!relevant_title.trim() || !relevant_url.trim()){
        alert("入力に不備があります");
        return;
    }
    $.ajax({
        type: 'POST',
        url: base_url + "/api/theme/" + theme_id + "/relevant/edit/",
        data:
            {
                'relevant_id' : relevant.id,
                'relevant_url' : relevant_url,
                'relevant_title': relevant_title
            }
    }).done(function(){
        // if data sending is successful
        relevant.url　= relevant_url;
        relevant.title =relevant_title;
    }).fail(function(){
        // if data sending is failed
        alert("関連情報編集エラー\nリロードしてください");
    });

    $('#edit-relevant-info').modal('hide');
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