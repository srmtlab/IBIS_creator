function wrap(text, move_flag) {
    text.each(function (d) {
        if(move_flag){
            d.data.words = [];
            let text = d3.select(this),
                word_width = 200,
                word,
                words = text.text().split('').reverse(),
                line = [],
                lineHeight = 1.2, // ems
                x = text.attr("x"),
                dy = text.attr("dy"),
                tspan = text.text(null)
                    .append("tspan")
                    .attr("x", x)
                    .attr("dy", dy);
            while (word = words.pop()) {
                line.push(word);
                tspan.text(line.join(""));
                if (tspan.node().getComputedTextLength() > word_width) {
                    line.pop();
                    tspan.text(line.join(""));
                    d.data.words.push(line.join(""));
                    line = [word];
                    tspan = text.append("tspan")
                        .attr("x", x)
                        .attr("dy", lineHeight + "em")
                        .text(word);
                    if(d.data.words.length === 2){
                        tspan.remove();
                        break;
                    }
                }
            }
            if(d.data.words.length < 2){
                d.data.words.push(line.join(""));
            }
        }else {
            let text = d3.select(this),
                word,
                words = d.data.words.concat().reverse(),
                line = [],
                lineHeight = 1.2, // ems
                x = text.attr("x"),
                dy = text.attr("dy"),
                tspan = text.text(null)
                    .append("tspan")
                    .attr("x", x)
                    .attr("dy", dy)
                    .text(words.pop());
            while (word = words.pop()) {
                tspan = text.append("tspan")
                    .attr("x", x)
                    .attr("dy", lineHeight + "em")
                    .text(word);
            }
        }
    });
}

function update(source, move_flag = false) {
    let circle_range = 60;
    let duration = 500;

    let levelWidth = [1];
    let childCount = function(level, n) {
        if (n.children && n.children.length > 0) {
            if (levelWidth.length <= level + 1) levelWidth.push(0);

            levelWidth[level + 1] += n.children.length;
            n.children.forEach(function(d) {
                childCount(level + 1, d);
            });
        }
    };
    childCount(0, root);
    let newHeight = d3.max(levelWidth) * 230;
    let tree = d3.tree().size([newHeight, ibis_width]);

    tree(root);

    // assign the y-coordinate on each node
    root.each(
        function(d) {
            d.y = d.depth * 320;
        }
    );

    // below code regarding to each node
    // declare .node and decide the array of root's descendant node, using d.id as key
    let node = g.selectAll('.node')
        .data(root.descendants(),
            function(d) {
                return d.id || (d.id = d.data.id);
            }
        );

    // enter the root node data
    let nodeEnter = node
        .enter()
        .append("g")
        .attr("class", "node")
        .attr("transform", function (d) {
            if (init_flag) {
                return "translate(" + source.y + "," + source.x + ")";
            } else {
                return "translate(" + source.y0 + "," + source.x0 + ")";
            }
        });


    nodeEnter.append("image")
        .attr("class","node_img")
        .attr("x", -(circle_range - 4) / 2)
        .attr("y", -(circle_range - 4) / 2)
        .attr("width", circle_range - 4)
        .attr("height", circle_range - 4)
        .on("click", function (d) {
            toggle(d);
            update(d);
        })
        .on("mouseenter", function(d) {
            let parent=this.parentNode;
            $(parent.getElementsByClassName("operator")).fadeIn("fast");
        })
        .on("mouseleave", function(d) {
            let current_hover=jQuery(":hover").slice(-1)[0];
            if(!$(current_hover).is('.operator')){
                let parent=this.parentNode;
                $(parent.getElementsByClassName("operator")).fadeOut("fast");
            }
        });

    nodeEnter.append("text")
        .attr("x","0")
        .attr("dy", "55")
        .attr("font-size", "120%")
        .attr("font-weight", "bold")
        .attr("text-anchor", "middle")
        .style("fill-opacity", 1e-6);


    nodeEnter.append("image")
        .attr("class","delete_img operator")
        .attr("style","display:none")
        .attr("x", (circle_range/3 - 4) / 5)
        .attr("y", -(circle_range/3 - 4) / 2)
        .attr("width", circle_range/3 - 4)
        .attr("height", circle_range/3 - 4)
        .on("click", function (d) {
            if(d.parent !== null) {
                show_delete_node(d);
            }
        })
        .on("mouseleave", function(d) {
            let current_hover=jQuery(":hover").slice(-1)[0];
            if(!$(current_hover).is('.node_img')) {
                let parent = this.parentNode;
                $(parent.getElementsByClassName("operator")).fadeOut("fast");
            }
        });

    nodeEnter.append("image")
        .attr("class","add_img operator")
        .attr("style","display:none")
        .attr("x", (circle_range/3 - 4) / 5)
        .attr("y", (circle_range/3 - 4) / 4)
        .attr("width", circle_range/3 - 4)
        .attr("height", circle_range/3 - 4)
        .on("click", function (d) {
            show_add_node(d);
        })
        .on("mouseleave", function(d) {
            let current_hover=jQuery(":hover").slice(-1)[0];
            if(!$(current_hover).is('.node_img')) {
                let parent = this.parentNode;
                $(parent.getElementsByClassName("operator")).fadeOut("fast");
            }
        });


    nodeEnter.append("image")
        .attr("class","edit_img operator")
        .attr("style","display:none")
        .attr("x", - (circle_range/3 - 4) / 2)
        .attr("y", (circle_range/3 - 4) / 4)
        .attr("width", circle_range/3 - 4)
        .attr("height", circle_range/3 - 4)
        .on("click", function (d) {
            show_edit_node(d);
        })
        .on("mouseleave", function(d) {
            let current_hover=jQuery(":hover").slice(-1)[0];
            if(!$(current_hover).is('.node_img')) {
                let parent = this.parentNode;
                $(parent.getElementsByClassName("operator")).fadeOut("fast");
            }
        });

    nodeEnter.append("image")
        .attr("class","relevant_info_img operator")
        .attr("style","display:none")
        .attr("x", -(circle_range/3 - 4) / 2)
        .attr("y", -(circle_range/3 - 4) / 2)
        .attr("width", circle_range/3 - 4)
        .attr("height", circle_range/3 - 4)
        .on("click", function (d) {
            show_relevant_info(d)
        })
        .on("mouseleave", function(d) {
            let current_hover=jQuery(":hover").slice(-1)[0];
            if(!$(current_hover).is('.node_img')) {
                let parent = this.parentNode;
                $(parent.getElementsByClassName("operator")).fadeOut("fast");
            }
        });

    let nodeUpdate = nodeEnter.merge(node);

    nodeUpdate.transition()
        .duration(duration)
        .attr("transform", function (d) {
            return "translate(" + d.y + "," + d.x + ")";
        });

    nodeUpdate.select(".node_img")
        .attr("xlink:href",
            function (d) {
                let type = d.data.type;
                if(type === "Issue"){
                    return static_url + "img/create_ibis/operator/issue.png";
                }else if(type === "Idea"){
                    return static_url + "img/create_ibis/operator/idea.png";
                }else if(type === "Merit"){
                    return static_url + "img/create_ibis/operator/merit.png";
                }else if (type === "Demerit"){
                    return static_url + "img/create_ibis/operator/demerit.png";
                }else if (type === "Example"){
                    return static_url + "img/create_ibis/operator/example.png";
                }else if (type === "Reason"){
                    return static_url + "img/create_ibis/operator/reason.png";
                }else if (type === "Opinion"){
                    return static_url + "img/create_ibis/operator/opinion.png";
                }
            }
        )
        .attr("x", - (circle_range / 2))
        .attr("y", - (circle_range / 2))
        .attr("width", circle_range)
        .attr("height", circle_range);


    nodeUpdate.select("text")
        .text(function (d) {
            return d.data.name;
        })
        .call(wrap, init_flag||move_flag)
        .style("fill-opacity", 1);

    nodeUpdate.select(".delete_img")
        .attr("xlink:href",
            function (d) {
                if(d.parent !== null){
                    return  static_url + "img/create_ibis/operator/delete.png";
                }
            }
        )
        .attr("x", circle_range/5)
        .attr("y", - (circle_range/2))
        .attr("width", circle_range/3)
        .attr("height", circle_range/3);

    nodeUpdate.select(".add_img")
        .attr("xlink:href",
            function (d) {
                return static_url + "img/create_ibis/operator/add.png";
            }
        )
        .attr("x", circle_range/5)
        .attr("y",  circle_range/4)
        .attr("width", circle_range/3)
        .attr("height", circle_range/3);

    nodeUpdate.select(".edit_img")
        .attr("xlink:href",
            function (d) {
                return static_url + "img/create_ibis/operator/edit.png";
            }
        )
        .attr("x", -(circle_range/2))
        .attr("y", circle_range/4)
        .attr("width", circle_range/3)
        .attr("height", circle_range/3);

    nodeUpdate.select(".relevant_info_img")
        .attr("xlink:href",
            function (d) {
                return static_url + "img/create_ibis/operator/relevant_info.png";
            }
        )
        .attr("x", -(circle_range/2))
        .attr("y", -(circle_range/2))
        .attr("width", circle_range/3)
        .attr("height", circle_range/3);

    let nodeExit;

    if (move_flag) {
        nodeExit = node
            .exit()
            .transition()
            .duration(duration)
            .attr("transform", function (d) {
                return "translate(" + d.y + "," + d.x + ")";
            })
            .remove();

    } else {
        nodeExit = node
            .exit()
            .transition()
            .duration(duration)
            .attr("transform", function (d) {
                return "translate(" + source.y + "," + source.x + ")";
            })
            .remove();
    }

    nodeExit.select(".node_img")
        .attr("x", -2)
        .attr("y", -2)
        .attr("width", 4)
        .attr("height", 4);

    nodeExit.select("text")
        .style("fill-opacity", 1e-6);

    // below code regarding to each link
    let link = g.selectAll(".link")
        .data(root.links(), function(d) { return d.target.id; });

    let linkEnter = link.enter()
        .insert('line', "g")
        .attr("class", "link")
        .attr("x1", function(d) {
            if(init_flag){
                return source.y;
            }else {
                return source.y0;
            }
        })
        .attr("y1", function(d) {
            if(init_flag){
                return source.x;

            }else {
                return source.x0;
            }
        })
        .attr("x2", function(d) {
            if(init_flag){
                return source.y;

            }else {
                return source.y0;
            }
        })
        .attr("y2", function(d) {
            if(init_flag){
                return source.x;
            }else {
                return source.x0;
            }
        });


    let linkUpdate = linkEnter.merge(link);
    linkUpdate
        .transition()
        .duration(duration)
        .attr("x1", function(d) {
            return d.source.y;
        })
        .attr("y1", function(d) {
            return d.source.x;
        })
        .attr("x2", function(d) {
            return d.target.y;
        })
        .attr("y2", function(d) {
            return d.target.x;
        });


    if(move_flag){
        link
            .exit()
            .transition()
            .duration(duration)
            .attr("x1", function(d) {
                return (d.source.y + d.target.y) / 2;
            })
            .attr("y1", function(d) {
                return (d.source.x + d.target.x) / 2;
            })
            .attr("x2", function(d) {
                return (d.source.y + d.target.y) / 2;
            })
            .attr("y2", function(d) {
                return (d.source.x + d.target.x) / 2;
            })
            .remove();
    }else {
        link
            .exit()
            .transition()
            .duration(duration)
            .attr("x1", function(d) {
                return source.y;
            })
            .attr("y1", function(d) {
                return source.x;
            })
            .attr("x2", function(d) {
                return source.y;
            })
            .attr("y2", function(d) {
                return source.x;
            })
            .remove();
    }

    if(init_flag){
        current_gx = ibis_width/2 - source.y;
        current_gy = ibis_height/2 - source.x;
        g.attr("transform", "translate("+ current_gx +"," + current_gy +")");

        init_flag = false;
    }else{
        if(!move_flag){
            current_gx = (ibis_width/2 - source.y * scale) - translate_x;
            current_gy = (ibis_height/2 - source.x * scale) - translate_y;

            g.transition()
                .duration(duration)
                .attr("transform", "translate("+ (ibis_width/2 - source.y * scale) +"," + (ibis_height/2 - source.x * scale) + ")"
                    + "scale(" + scale + ")");
        }
    }

    root.each(function(d) {
        d.x0 = d.x;
        d.y0 = d.y;
    });
}

function toggle(d) {
    if(d.children) {
        d._children = d.children;
        d.children = undefined;
    } else {
        d.children = d._children;
        d._children = undefined;
    }
}