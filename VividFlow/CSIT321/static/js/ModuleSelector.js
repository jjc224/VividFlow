
class ModuleSelector {


    constructor() {
        this.$container = null;
        this.modules_displayed = 0;
        this.module_display_offset = 0;
        this.modules = null;
        this.module_strings = null;
    }

    retrieve_modules() {
        $.ajax({
            context: this,
            url: "/module/list/json",
            type: "GET",
            success: function(data) {
                this.add_modules_to_list(data);
            }
        });
    }

    add_modules_to_list(data) {
        this.modules = [];
        this.module_strings = JSON.parse(data);
        for (var i = 0; i < this.module_strings.length; i++) {
            var json_obj = JSON.parse(this.module_strings[i]);
            this.modules.push(new ModuleNode(json_obj));
            this.modules[i].reconstruct_from_json(json_obj);
        }
        this.display_modules();
    }

    display_modules() {
        if (this.$container == null) {
            console.log("Module Selector: No container set, cannot display.");
            return false;
        }
        if (this.modules == null) {
            console.log("Module Selector: No modules")
            this.$container.html("No Modules");
            return false;
        }

        this.$container.html == "";

        var html = "";
        html += "<table border='1' width='100%' class='table'>";
        for (var i = 0; i < this.modules.length; i++) {
            html += "<tr><td class='module-select-button' onclick='add_new_module(" + i + ")'>";
            //html += "<tr><button class='btn btn-default btn-module' onclick='add_new_module(" + i + ")'>";
            //html += "ID " + this.modules[i].get_id();
            //html += ": ";
            //html += "V" + this.modules[i].get_version();
            //html += ": ";
            html += this.modules[i].get_display_name();
            //html += "</button></tr>";
            html += "</td></tr>";
        }
        html += "</table>";

        this.$container.html(html);
    }

    set_container(container) {
        this.$container = container;
    }

    get_module(i) {
        return this.modules[i];
    }

}
