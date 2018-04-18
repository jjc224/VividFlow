

class ResourceForm {


    constructor($container) {
        this.$container = $container;
        this.selected = null; // index of resources
        this.resources = null;
        this.user_id = null;
        this.retrieve_resources();
    }

    set_container($container) {
        this.$container = $container;
    }

    set_user_id(id) {
        this.user_id = id;
    }

    set_selected(index) {
        this.selected = index;
        $(".resource_item").addClass("resource_not_selected");
        $(".resource_item").removeClass("resource_selected");
        $("#r" + index).removeClass("resource_not_selected");
        $("#r" + index).addClass("resource_selected");
    }

    get_container() {
        return this.$container;
    }

    get_selected() {
        return this.resources[this.selected];
    }

    get_download() {
        if (this.resources == null || this.selected == null) {
            return null;
        }
        return "/static/data/resources/" +this.resources[this.selected].id + "/" + this.resources[this.selected].filename;
    }

    set_resources(data) {
        this.resources = JSON.parse(data);
        this.generate_form();
    }

    retrieve_resources() {
        $.ajax({
            context: this,
            url: "/resource/list",
            type: "GET",
            success: function(data) {
                this.set_resources(data);
            }
        });
    }

    reset() {
        // Clear form and refresh from db
        this.retrieve_resources();
        this.generate_form();
    }

    generate_form() {
        var html = "";
        //html += "<h3>Resources</h3>";
        html += "<div id='resource_items'>"
        html += "</div>"
        this.$container.html(html);
        this.display();
    }

    display() {
        // display all the resources
        var html = "";
        if (this.resources == null) {
            html = "No Resources";
        } else {
            for (var i = 0; i < this.resources.length; i++) {
                html += this.display_resource(i);
            }
        }
        $("#resource_items").html(html);
        var self = this;
        var funct = function() {
            self.set_selected($("#" + this.id).attr("index"));
        }

        $(".resource_item").click(funct);
        $(".resource_item").mouseenter(function() {
            $(this).css("border", "3px solid lightblue");
        });
        $(".resource_item").mouseleave(function() {
            $(this).css("border", "0px");
        });
    }

    display_resource(i) {
        var html = "";
        html += "<div class='unselectable resource_item' index='" + i + "' id='r" + i + "'>";
        html += this.resources[i].resource_name;
        html += "</div>";
        return html;
    }

    add_resource(form_data) {
        // submit json object to add to database
        $.ajax({
            context: this,
            url: g_url.resource_add,
            data: form_data,
            method: "POST",
            success: function(data) {
                console.log(data);
                this.reset();
            },
            cache: false,
            contentType: false,
            processData: false
        });
        this.reset();
    }
}
