// Setup variables
var g_canvas = null;
var g_is_canvas_dirty = false;
var g_selected = {};
var g_drawalgo = null;
var g_algo = null;
var g_destroy = null;
var g_modules_selector = null;
var g_canvas_drag_on = false;
var g_drag_offsetx = 0;
var g_drag_offsety = 0;
var g_edit_node = null;

// Return mouse position
function get_mouse_position(canvas, evt) {
    var rect = canvas.getBoundingClientRect();
    return {
        x: evt.clientX - rect.left,
        y: evt.clientY - rect.top
    };
}

function on_mouse_down(evt) {
    context_menu_reset();
    if (g_drawalgo == null) {
        return;
    }
    if (evt.button == 2) {
        return;
    }
    // Get mouse position
    var mousePos = get_mouse_position(g_canvas, evt);
    // Determine if a node is moving
    if (g_is_canvas_dirty == false) {
        g_selected.object = g_drawalgo.check_hit(mousePos.x, mousePos.y);
        if (g_selected.object) {
            // Store node reference
            g_selected.object.set_selected(true);
            // Calculate mouse offset on node
            g_selected.offsetx = mousePos.x;// - g_selected.object.get_x();
            g_selected.offsety = mousePos.y;// - g_selected.object.get_y();
            // Re-draw algorithm with node selected
            g_drawalgo.draw();
            // Check if selected object is a socket
            if (g_selected.object instanceof DrawSocket) {
                // Create a temp Link
                var link = {};
                link._In_Socket = g_selected.object.get_socket();
                link._Out_Socket = null;
                g_selected.newlink = new DrawLink(g_selected.object.get_context(), link);
                // Update Link position
                g_selected.newlink.set_x(g_selected.object.get_x);
                g_selected.newlink.set_y(g_selected.object.get_y);
                // Draw over the top of algorithm
                g_selected.newlink.draw();
            }
            // Turn moving on
            g_is_canvas_dirty = true;
            g_canvas_drag_on = false;
        } else {
            g_canvas_drag_on = true;
            g_drag_offsetx = mousePos.x;
            g_drag_offsety = mousePos.y;
        }
    } else {
        // Turn off selection
        g_selected.object.set_selected(false);
        // Turn off moving
        g_is_canvas_dirty = false;
        g_canvas_drag_on = false;
        // Re-draw algorithm with node in final position
        g_drawalgo.draw();
    }
}

function on_mouse_up(evt) {
    context_menu_reset();
    if(g_drawalgo == null) {
        return;
    }
    // Get mouse position
    var mousePos = get_mouse_position(g_canvas, evt);
    // If node is moving then stop it
    if (g_is_canvas_dirty) {
        // Check if a new Link needs to be created
        if (g_selected.object instanceof DrawSocket) {
            // Check if there is an end Node
            if (g_selected.endnode != null) {
                // Unselect Socket
                g_selected.endnode.set_selected(false);
                // Set the Socket from algo data structure to Link out socket
                g_selected.newlink.set_link_out_socket(g_selected.endnode.get_socket());
                // Check which is input
                var input_sock = null;
                var output_sock = null;
                if (g_selected.endnode.get_socket().get_socket_io_type() == "input") {
                    input_sock = g_selected.endnode.get_socket();
                    output_sock = g_selected.object.get_socket();
                } else {
                    input_sock = g_selected.object.get_socket();
                    output_sock = g_selected.endnode.get_socket();
                }
                // Try to add the link to algo data structure
                var new_data_link = g_algo.add_link(output_sock, input_sock);
                // Check that it added
                if (new_data_link != null && new_data_link != false) {
                    // Set the data link in the draw link
                    g_selected.newlink.set_link(new_data_link);
                    // Add the draw link to the draw algo
                    g_drawalgo.add_link(g_selected.newlink);
                    // var algo2 = g_algo.serialize_json();
                    // console.log(algo2);
                }
                reset_draw_algo();
            }
            g_selected.newlink = null;
        }
        // Turn off selection
        g_selected.object.set_selected(false);
        // Turn off moving
        g_is_canvas_dirty = false;
        // Re-draw algorithm with node in final position
        //var algo2 = g_algo.serialize_json();
        //console.log(algo2);
    }
    g_is_canvas_dirty = false;
    g_canvas_drag_on = false;
    g_drawalgo.draw();
}

function on_mouse_move(evt) {
    if(g_drawalgo == null) {
        return;
    }
    // Get mouse position
    var mousePos = get_mouse_position(g_canvas, evt);
    // If node is moving then update screen
    if (g_canvas_drag_on === true) {

        g_drawalgo.set_offsetx((parseInt(g_drag_offsetx)-parseInt(mousePos.x))*-1);
        g_drawalgo.set_offsety((parseInt(g_drag_offsety)-parseInt(mousePos.y))*-1);
        g_drag_offsetx = mousePos.x;
        g_drag_offsety = mousePos.y;
        g_drawalgo.draw();
    }
    if (g_is_canvas_dirty) {

        if (g_selected.object) {
            // If a new Link then update and draw
            if (g_selected.object instanceof DrawSocket) {
                // Update Link position
                g_selected.newlink.set_x(g_selected.object.get_x() + (mousePos.x - g_selected.offsetx));
                g_selected.newlink.set_y(g_selected.object.get_y() + (mousePos.y - g_selected.offsety));
                // Draw Link
                g_drawalgo.draw();
                g_selected.newlink.draw();
                // Unselect Socket in case mouse is no longer over
                if (g_selected.endnode != null) {
                    g_selected.endnode.set_selected(false);
                }
                // Check if mouse is over a Socket
                g_selected.endnode = g_drawalgo.check_hit(mousePos.x, mousePos.y);
                // Check that it isn't start Socket
                if (g_selected.endnode == g_selected.object) {
                    g_selected.endnode = null;
                }
                // Check hit is a Socket
                if (g_selected.endnode instanceof DrawSocket) {
                    // Select socket
                    g_selected.endnode.set_selected(true);
                } else {
                    g_selected.endnode = null;
                }

            } else {
                // Update node position
                g_selected.object.set_x(g_selected.object.get_x() + (mousePos.x - g_selected.offsetx));
                g_selected.object.set_y(g_selected.object.get_y() + (mousePos.y - g_selected.offsety));
                g_selected.offsetx = mousePos.x;
                g_selected.offsety = mousePos.y;
                // Re-draw algorithm with node in new position
                g_drawalgo.draw();
            }

        }
    }
}

// Resets the context menu
function context_menu_reset() {
    $("#contextmenu").remove();
}

// Function called from context menu button
function destroy_link() {
    context_menu_reset();
    g_drawalgo.destroy_link(g_destroy);
    reset_draw_algo();
    reset_draw_algo();
    g_is_canvas_dirty = false;
}

// Function called from context menu button
function destroy_node() {
    context_menu_reset();
    g_drawalgo.destroy_node(g_destroy);
    reset_draw_algo();
}

function add_module(x, y) {
    context_menu_reset();
    var new_node = new ModuleNode();
    g_algo.add_node(new_node);
    reset_draw_algo();
    var drawnode = g_drawalgo.get_drawnode_by_node(new_node);
    drawnode.set_x(parseInt(x) - g_drawalgo.get_offsetx());
    drawnode.set_y(parseInt(y) - g_drawalgo.get_offsety());
    g_drawalgo.draw();
}

function add_resource(x, y) {
    context_menu_reset();
    var new_node = new ResourceNode();
    var resource = g_resource_form.get_selected();
    new_node.set_resource(resource.id, resource.resource_name, resource.file_type);
    new_node.add_socket();
    g_algo.add_node(new_node);
    reset_draw_algo();
    var drawnode = g_drawalgo.get_drawnode_by_node(new_node);
    drawnode.set_x(parseInt(x) - g_drawalgo.get_offsetx());
    drawnode.set_y(parseInt(y) - g_drawalgo.get_offsety());
    g_drawalgo.draw();
}

function add_output(x, y) {
    context_menu_reset();
    var new_node = new OutputNode();
    var name = $("#output_name").val();
    var output_type = $("#output_type").val();
    $("#output_name").val("");
    $("#output_type").val("");
    new_node.set_name(name);
    new_node.set_output_type(output_type);
    new_node.add_socket();
    g_algo.add_node(new_node);
    reset_draw_algo();
    var drawnode = g_drawalgo.get_drawnode_by_node(new_node);
    drawnode.set_x(parseInt(x) - g_drawalgo.get_offsetx());
    drawnode.set_y(parseInt(y) - g_drawalgo.get_offsety());
    g_drawalgo.draw();
}

function add_value(x, y) {
    context_menu_reset();
    var new_node = new ValueNode();
    var name = $("#value_name").val();
    var value_type = $("#value_type").val();
    var value = $("#value_value").val();
    $("#value_name").val("");
    $("#value_type").val("");
    $("#value_value").val("");
    new_node.set_value(value);
    new_node.set_name(name);
    new_node.set_value_type(value_type);
    new_node.add_socket();
    g_algo.add_node(new_node);
    reset_draw_algo();
    var drawnode = g_drawalgo.get_drawnode_by_node(new_node);
    drawnode.set_x(parseInt(x) - g_drawalgo.get_offsetx());
    drawnode.set_y(parseInt(y) - g_drawalgo.get_offsety());
    g_drawalgo.draw();
}

function reset_draw_algo() {
    // Retain offset
    var tempx = g_drawalgo.get_offsetx();
    var tempy = g_drawalgo.get_offsety();
    g_drawalgo = new DrawAlgorithm(g_algo);
    g_drawalgo.set_offsetx(tempx);
    g_drawalgo.set_offsety(tempy);
    g_drawalgo.draw();
}

function on_context_menu(evt) {
    context_menu_reset();
    // Stop the browsers default context menu
    evt.preventDefault();
    var mousePos = get_mouse_position(g_canvas, evt);
    var obj = g_drawalgo.check_hit(mousePos.x, mousePos.y);
    // Create context menu
    if (obj != false) {
        var menu_html = "<div style='width: 150px; border: solid 1px black' id='contextmenu'>";
        if (obj instanceof DrawLink) {
            g_destroy = obj;
            menu_html += "<button onclick='destroy_link()' style='width: 100%'>Delete Link</button>";
        }
        if (obj instanceof DrawNode) {
            g_destroy = obj;
            menu_html += "<button onclick='destroy_node()' style='width: 100%'>Delete Node</button>";
            if (obj.get_node() instanceof OutputNode) {
                g_edit_node = obj;
                menu_html += "<button onclick='edit_output_node()' style='width: 100%'>Edit</button>";
            }
            if (obj.get_node() instanceof ValueNode) {
                g_edit_node = obj;
                menu_html += "<button onclick='edit_value_node()' style='width: 100%'>Edit</button>";
            }
        }
        menu_html += "</div>";

        // Add to page
        $("body").append(menu_html);
        // Position menu to mouse
        $("#contextmenu").offset({top:evt.clientY,left:evt.clientX});
    } else {
        var menu_html = "<div style='width: 150px; border: solid 1px black' id='contextmenu'>";
        menu_html += "<button data-toggle='modal' data-target='#modal_value' style='width: 100%'>Add Value</button>";
        menu_html += "<button data-toggle='modal' data-target='#modal_resource' style='width: 100%'>Add Resource</button>";
        menu_html += "<button data-toggle='modal' data-target='#modal_output' style='width: 100%'>Add Ouput</button>";
        menu_html += "</div>";
        $("#value_button").attr("onclick", "add_value(" + mousePos.x + ", " + mousePos.y + ")");
        $("#resource_button").attr("onclick", "add_resource(" + mousePos.x + ", " + mousePos.y + ")");
        $("#output_button").attr("onclick", "add_output(" + mousePos.x + ", " + mousePos.y + ")");
        // Add to page
        $("body").append(menu_html);
        // Position menu to mouse
        $("#contextmenu").offset({top:evt.clientY,left:evt.clientX});
    }
}

// Start is called in the html file when document loads so that the dom already exists
function init_algorithm_canvas() {
    g_selected.object = null;
    g_selected.offsetx = 0;
    g_selected.offsety = 0;
    g_selected.newlink = null;
    g_canvas = document.getElementById('myCanvas');

    // register event handlers
    g_canvas.addEventListener('mousedown', on_mouse_down, false);
    g_canvas.addEventListener('mouseup', on_mouse_up, false);
    g_canvas.addEventListener('mousemove', on_mouse_move, false);
    g_canvas.addEventListener('contextmenu', on_context_menu);
    $("#algo_name").change(update_algo_name);
}

// Updates the algorithm name
function update_algo_name() {
    var new_name = $("#algo_name").val();
    g_algo.set_algorithm_name(new_name);
    console.log("New Algorithm Name: " + new_name);
}


function algorithm_ajax_request_complete(algo_json){
    var jsonParsed = JSON.parse(algo_json);
    g_algo = SerialObjectTypes.build_object_from_json(jsonParsed);
    g_algo.relink_algorithm();
    // Create draw object with algorithm
    g_drawalgo = new DrawAlgorithm(g_algo);
    // Draw algorithm
    g_drawalgo.draw();
    // Set algorithm name
    $("#algo_name").val(g_algo.get_algorithm_name());
    hide_ajax_loader();
}

function retrieve_algorithm(algorithm_id) {
    $.ajax({
        url: g_urls.algorithm_json_url,
        method: "GET",
        success: algorithm_ajax_request_complete
    });
}

function save_algorithm() {
    let string_algo = g_algo.serialize_json();
    $.ajax({
        url: g_urls.algorithm_json_url,
        type: "POST",
        data: {algo:string_algo},
        //dataType: "text",
        success: function(data) {
            console.log("Algorithm saved");
            display_info_alert("Algorithm saved!");
        },
        error: function(data) {
            console.log("Algorithm failed to save");
            display_error_alert("Could not save algorithm!");
        }
    });
}

function resize_canvas() {
    var width = $("#canvas_td").width();
    var height = $("#canvas_td").height();
    $("#myCanvas").attr("width", width);
    $("#myCanvas").attr("height", height);
}

function init_module_selector() {
    g_modules_selector = new ModuleSelector();
    g_modules_selector.set_container($("#node_selector"));
    g_modules_selector.retrieve_modules();
}

function add_new_module(index) {
    // Get module to copy
    var selector_module = g_modules_selector.get_module(index);
    var new_node = selector_module.create_node_instance();
    g_algo.add_node(new_node);
    g_algo.relink_algorithm();
    // Create draw object with algorithm
    reset_draw_algo();
    // Update node position
    var draw_new_node = g_drawalgo.get_drawnode_by_node(new_node);
    draw_new_node.set_x(parseInt(parseInt($("#myCanvas").attr("width"))/2-160-g_drawalgo.get_offsetx()));
    draw_new_node.set_y(parseInt(parseInt($("#myCanvas").attr("height"))/2-160-g_drawalgo.get_offsety()));
    // Draw algorithm
    g_drawalgo.draw();
}

function run_algorithm(algorithm_id) {
    $.ajax({
        url: g_urls.run_algorithm_url,
        method: "GET",
        success: function(data) {
            console.log("Algorithm scheduled to run");
            display_info_alert("Algorithm scheduled to run!");
        },
        error: function(data) {
            console.log("Couldn't schedule run");
            display_error_alert("Couldn't schedule run!");
        }
    });
}

function populate_output_type() {
    //var html = "<select id='output_type'>";
    var html = "";
    var items = SocketDataTypes.get_list();
    for (var i = 0; i < items.length; i++) {
        html += "<option>" + items[i] + "</option>";
    }
    $(".socket_types").append(html);
}

function edit_output_node() {
    var node = g_edit_node.get_node();
    $("#edit_output_name").val(node.get_display_name());
    $("#edit_output_type").val(node.get_output_type());
    $('#modal_output_edit').modal('show');
}

function edit_value_node() {
    var node = g_edit_node.get_node();
    $("#edit_value_name").val(node.get_display_name());
    $("#edit_value_type").val(node.get_value_type());
    $("#edit_value_value").val(node.get_value());
    $('#modal_value_edit').modal('show');
}

function update_output() {
    var node = g_edit_node.get_node();
    node.set_name($("#edit_output_name").val());
    node.set_output_type($("#edit_output_type").val());
    context_menu_reset();
    reset_draw_algo();
}

function update_value() {
    var node = g_edit_node.get_node();
    node.set_name($("#edit_value_name").val());
    node.set_value_type($("#edit_value_type").val());
    node.set_value($("#edit_value_value").val());
    context_menu_reset();
    reset_draw_algo();
}
