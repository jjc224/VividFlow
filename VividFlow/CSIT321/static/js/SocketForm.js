class SocketForm {

    constructor() {
        this.$container = null;
        this.sockets = null;
    }

    set_sockets(sockets) {
        this.sockets = sockets;
    }

    set_container(container) {
        this.$container = container;
    }

    html_controls() {
        var socket_form = this;
        var html = "";
        html += "<button id='button_" + this.$container.attr("id") + "' class='btn btn-default' style='float:right;'>Add Socket</button>";
        return html;
    }

    html_socket_table() {
        var html = "";
        html += "<table class='sockets_table'>";
        html += "<tr><th width='30px'>Arg#</th><th width='200px'>Name</th><th width='150px'>Type</th><th></th></tr>";
        return html;
    }

    html_socket_table_row(index) {
        var html = "";
        html += "<tr><td>" + this.sockets[index]._ArgumentNumber;
        html += "</td><td><input type='text' maxlength='11' class='form-control' value='" + this.sockets[index]._Name + "'>";
        html += "</td><td>" + this.html_socket_select_type(this.sockets[index]._DataType);
        console.log(this.$container.attr("id"));
        html += "</td><td><span id='" + index + "' class='glyphicon glyphicon-remove remove_" + this.$container.attr("id") + "' onclick=''></span></td></tr>";
        return html;
    }

    html_socket_select_type(socket_type) {
        var types = SocketDataTypes.get_list();
        var html = "";
        html += "<select class='form-control'>";
        for (var i = 0; i < types.length; i++) {
            html += "<option ";
            if (types[i] == socket_type) {
                html += "selected";
            }
            html += ">";
            html += types[i];
            html += "</option>";
        }
        html += "<option>";
        html += "</select>";
        return html;
    }

    generate_form() {
        if (this.$container == null) {
            console.log("Socket Form: No container is set, cannot draw form.");
            return false;
        }

        var html = "";
        html += "<div style='width:450px;'>";
        html += this.html_socket_table();
        for (var i = 0; i < this.sockets.length; i++) {
            html += this.html_socket_table_row(i);
        }
        html += "</table>";
        html += "<br>";
        html += this.html_controls();
        html += "</div>";
        this.$container.html(html);
        var class_obj = this;
        var add_funct = function() {
            mark_module_as_modified();
            var data = class_obj.extract_data();
            var new_socket = new NodeIOSocket();
            new_socket.set_argument_number("99");
            class_obj.sockets.push(new_socket);
            class_obj.update_socket_data(data);
            class_obj.sort_socket_array();
            class_obj.generate_form();
        }
        $('#button_' + this.$container.attr("id")).click(add_funct);

        var remove_funct = function() {
            mark_module_as_modified();
            class_obj.sockets.splice(parseInt($(this).attr("id")),1);
            class_obj.sort_socket_array();
            class_obj.generate_form();
        }
        $(".remove_" + class_obj.$container.attr("id")).click(remove_funct);
        console.log(this.sockets);
    }

    extract_data() {
        var table = this.$container.children("div").children("table");
        var data = [];
        table.find('tr').each(function (rowIndex, r) {
            var cols = [];
            $(this).find('td').each(function (colIndex, c) {
                var value = null
                // Argument Number
                if (colIndex == 0) {
                    value = c.textContent;
                }
                // Socket Name
                if (colIndex == 1) {
                    value = $(c).children("input").val();
                }
                // Socket Type
                if (colIndex == 2) {
                    value = $(c).children("select").val();
                }
                if (value != null) {
                    cols.push(value);
                }
            });
            if (rowIndex != 0) {
                cols.push(g_module_id);
                data.push(cols);
            }
        });
        return data;
    }

    update_socket_data(data) {
        if (data == null || data[0] == null) {
            return false;
        }
        for (var i = 0; i < data.length; i++) {
            this.sockets[i]._ArgumentNumber = data[i][0];
            this.sockets[i]._Name = data[i][1];
            this.sockets[i]._DataType = data[i][2];
            this.sockets[i]._OwnerNodeId = data[i][3];
            console.log(this.sockets[i]._DataType);
        }
    }

    swap_socket_positions(sock1, sock2) {
        sock_num = sock1._ArgumentNumber;
        sock1._ArgumentNumber = sock2._ArgumentNumber;
        sock2._ArgumentNumber = sock_num;
        this.sort_socket_array();
    }

    sort_socket_array() {
        this.sockets.sort(function(a,b) { return a._ArgumentNumber - b._ArgumentNumber;});
        this.renumber_sockets();
    }

    renumber_sockets() {
        for(let i = 0; i < this.sockets.length; i++)
        {
            this.sockets[i]._ArgumentNumber = i + 1;
        }
    }

    remove_socket(sock1) {
        let index = this.sockets.indexOf(sock1);
        if(index != -1) {
            this.sockets.splice(i, 1);
        }
        this.renumber_sockets();
    }
}
