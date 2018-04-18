
class DrawAlgorithm {

    constructor(algo) {
        // Get canvas from dom
        this.canvas = document.getElementById('myCanvas');
        this.context = this.canvas.getContext('2d');

        // Initialise class variables
        this.algo = algo;
        this.drawnodes = [];
        this.drawlinks = [];
        this.offsetx = 0;
        this.offsety = 0;

        // Create & store array of drawnodes
        for (var i = 0; i < algo._Nodes.length; i++) {
            this.drawnodes.push(new DrawNode(this.context, algo._Nodes[i]));
        }

        // Create & store array of drawlinks
        for (var i = 0; i < algo._Links.length; i++) {
            this.drawlinks.push(new DrawLink(this.context, algo._Links[i]));
        }
    }

    set_offsetx(x) {
        this.offsetx += x;
    }

    set_offsety(y) {
        this.offsety += y;
    }

    get_offsetx() {
        return this.offsetx;
    }

    get_offsety() {
        return this.offsety;
    }


    drawGrid() {
        var bw = parseInt(this.canvas.width);
        var bh = parseInt(this.canvas.height);
        //padding around grid
        var p = 10;
        //size of canvas
        var cw = bw + (p*2) + 1;
        var ch = bh + (p*2) + 1;

        for (var x = 0; x <= bw; x += 40) {
            this.context.moveTo(0.5 + x + p, p);
            this.context.lineTo(0.5 + x + p, bh + p);
        }

        for (var x = 0; x <= bh; x += 40) {
            this.context.moveTo(p, 0.5 + x + p);
            this.context.lineTo(bw + p, 0.5 + x + p);
        }
        this.context.shadowBlur=0;
        this.context.strokeStyle = 'black';
        this.context.lineWidth = 2;
        this.context.strokeStyle = "#f0f0f0";
        this.context.stroke();
    }

    draw() {
        this.context.save();
        this.context.setTransform(1, 0, 0, 1, 0, 0);
        this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.drawGrid();
        //this.context.restore();
        this.context.translate(this.offsetx, this.offsety);
        // Draw nodes
        var drawlast = null;
        for (var i = 0; i < this.drawnodes.length; i++) {
            if (!this.drawnodes[i].selected) {
                this.drawnodes[i].draw();
            } else {
                drawlast = this.drawnodes[i];
            }
        }
        // draw selected node last
        if (drawlast != null) {
            drawlast.draw();
        }
        // Draw links
        for (var i = 0; i < this.drawlinks.length; i++) {
            this.drawlinks[i].draw();
        }


    }

    add_link(link) {
        this.drawlinks.push(link);
        // Need to algorithm data strcture
    }

    // Check if xy are in a node, return node
    check_hit(x, y) {

        // Check Sockets
        for (var i = 0; i < this.drawnodes.length; i++) {
            var sockets = this.drawnodes[i].get_input_sockets();
            for (var j = 0; j < sockets.length; j++) {
                var result = sockets[j].check_inside(x, y);
                if (result) {
                    return result;
                }
            }
            sockets = this.drawnodes[i].get_output_sockets();
            for (var j = 0; j < sockets.length; j++) {
                var result = sockets[j].check_inside(x, y);
                if (result) {
                    return result;
                }
            }
        }

        // Check Nodes
        for (var i = 0; i < this.drawnodes.length; i++) {
            var result = this.drawnodes[i].check_inside(x, y)
            if (result) {
                return result;
            }
        }

        // Check Links
        for (var i = 0; i < this.drawlinks.length; i++) {
            var result = this.drawlinks[i].check_inside(x, y)
                if (result) {
                return result;
            }
        }

        return false;
    }

    destroy_node(node) {
        // Find node in array of nodes
        for (var i = 0; i < this.drawnodes.length; i++) {
            if (this.drawnodes[i] == node) {
                // Destroy node
                this.algo.destroy_node(node.node);
                // Remove from array
                this.drawnodes.splice(i, 1);
                return true;
            }
        }
        console.log("Could not delete node!");
        return false;
    }

    destroy_link(link) {
        // Find node in array of nodes
        for (var i = 0; i < this.drawlinks.length; i++) {
            if (this.drawlinks[i] == link) {
                // Remove from array
                this.drawlinks.splice(i, 1);
                // Destroy node
                link.destroy_link();
                return true;
            }
        }
        console.log("Could not delete link!");
        return false;
    }

    get_drawnode_by_node(node) {
        for (var i = 0; i < this.drawnodes.length; i++) {
            if (this.drawnodes[i].node == node) {
                return this.drawnodes[i];
            }
        }
    }

}


class DrawableObject {

    constructor(context) {
        this.context = context;
        this.x;
        this.y;
        this.selected = false;
    }

    draw() {}

    set_x(x) {
        this.x = x;
    }

    set_y(y) {
        this.y = y;
    }

    get_x() {
        return this.x;
    }

    get_y() {
        return this.y;
    }

    // Check if xy is inside this node
    check_inside(x, y) {
        var minx = parseInt(this.get_x());
        var maxx = parseInt(this.get_x()) + parseInt(this.width);
        var miny = parseInt(this.get_y());
        var maxy = parseInt(this.get_y()) + parseInt(this.height);
        var posx = parseInt(x) - g_drawalgo.get_offsetx();
        var posy = parseInt(y) - g_drawalgo.get_offsety();
        if (posx > minx && posx < maxx && posy > miny && posy < maxy) {
            return this;
        }
        return false;
    }

    set_selected(state) {
        this.selected = state;
    }

    get_context() {
        return this.context;
    }

}


class DrawNode extends DrawableObject {
    constructor(context, node) {
        super(context);
        this.node = node;

        // Add node drawing settings
        this.title = {};
        this.title.size = 25;
        this.title.offsetx = 5;
        this.title.offsety = 17;
        this.width = 230;
        this.height = 120;

        // Initialise socket arrays
        this._InputSockets = [];
        this._OutputSockets = [];

        // Create & store array of drawsockets
        for (var i = 0; i < node._InputSockets.length; i++) {
            this._InputSockets.push(new DrawSocket(context, node._InputSockets[i], 'input'));
        }
        for (var i = 0; i < node._OutputSockets.length; i++) {
            this._OutputSockets.push(new DrawSocket(context, node._OutputSockets[i], 'output'));
        }
    }

    draw() {
        // Get own xy
        var x = this.node.get_x();
        var y = this.node.get_y();

        // Draw shadow
        this.context.beginPath();
        this.context.rect(x, y, this.width, this.height);
        this.context.shadowBlur=20;
        this.context.shadowColor="black";
        this.context.lineWidth = 2;
        this.context.strokeStyle = 'black';
        this.context.stroke();
        this.context.shadowBlur=0;
        // Draw the rectangle
        this.context.beginPath();
        this.context.rect(x, y, this.width, this.height);
        // Change background colour if node is selected
        if (this.selected) {
            this.context.fillStyle = 'lightgreen';
        } else {
            this.context.fillStyle = 'lightgrey';
        }
        this.context.fill();
        this.context.lineWidth = 2;
        this.context.strokeStyle = 'black';
        this.context.stroke();
        // Draw title underline
        this.context.beginPath();
        this.context.rect(x, y, this.width, this.title.size);
        this.context.fillStyle = 'white';
        this.context.fill();
        this.context.lineWidth = 2;
        this.context.strokeStyle = 'black';
        this.context.stroke();
        // Draw the node name
        this.context.textAlign = 'left';
        this.context.font = '12pt Calibri';
        this.context.fillStyle = 'black';
        this.context.fillText(this.node.get_display_name(), x + this.title.offsetx, y + this.title.offsety);

        // Draw array of sockets
        for (var i = 0; i < this._InputSockets.length; i++) {
            this._InputSockets[i].draw(x, y, this.width);
        }
        for (var i = 0; i < this._OutputSockets.length; i++) {
            this._OutputSockets[i].draw(x, y, this.width);
        }

        // Draw the image depending on node type
        // Images come from page
        if (this.selected) {
            // Value Node
            if (this.node instanceof ValueNode) {
                var img = document.getElementById("floppy-selected");
                this.context.drawImage(img, x + 15, y + 45);
            }
            // Resource Node
            if (this.node instanceof ResourceNode) {
                var img = document.getElementById("picture-selected");
                this.context.drawImage(img, x + 15, y + 45);
            }
            // Ouput Node
            if (this.node instanceof OutputNode) {
                var img = document.getElementById("hdd-selected");
                // Image goes on right hand side
                this.context.drawImage(img, x - 55 + this.width, y + 45);
            }
        } else {
            // Value Node
            if (this.node instanceof ValueNode) {
                var img = document.getElementById("floppy");
                this.context.drawImage(img, x + 15, y + 45);
            }
            // Resource Node
            if (this.node instanceof ResourceNode) {
                var img = document.getElementById("picture");
                this.context.drawImage(img, x + 15, y + 45);
            }
            // Ouput Node
            if (this.node instanceof OutputNode) {
                var img = document.getElementById("hdd");
                // Image goes on right hand side
                this.context.drawImage(img, x - 55 + this.width, y + 45);
            }
        }
    }

    // xy gets & sets are different in node because we store them in algo class
    set_x(x) {
        this.node._PosX = x;
    }

    set_y(y) {
        this.node._PosY = y;
    }

    get_x() {
        return this.node.get_x();
    }

    get_y() {
        return this.node.get_y();
    }

    get_input_sockets() {
        return this._InputSockets;
    }

    get_output_sockets() {
        return this._OutputSockets;
    }

    get_node() {
        return this.node;
    }

    destroy_node() {
        this.node.destroy_node();
    }
}


class DrawSocket extends DrawableObject {

    constructor(context, socket, type) {
        super(context);

        this.sockettype = type;
        this.socket = socket;
        this.socket.set_drawable(this);

        // Add socket drawing settings
        this.spacing = 30;
        this.offsetx = 0;
        this.offsety = 40;
        this.size = 6;
        this.width = this.size * 2;
        this.height = this.size * 2;
    }

    // Draws socket on node, width is node width
    draw(x, y, width) {
        // Draw socket
        var num = this.socket._ArgumentNumber;

        this.context.beginPath();
        // Change position based on socket type & update socket xy
        // Input is on left side of node, output is on right side
        if (this.sockettype == 'input') {
            this.x = x + this.offsetx;
            this.y = y + this.offsety + this.spacing * (num - 1);
            this.context.arc(this.x, this.y, this.size, 0, 2 * Math.PI);
        } else if (this.sockettype == 'output') {
            this.x = x + width - this.offsetx;
            this.y = y + this.offsety + this.spacing * (num - 1);
            this.context.arc(this.x, this.y, this.size, 0, 2 * Math.PI);
        }
        this.context.closePath();
        this.context.lineWidth = 1;
        if (this.selected) {
            this.context.fillStyle = 'red';
        } else {
            if (g_selected.newlink != null) {
                if (g_selected.object.get_socket().get_socket_io_type() != this.socket.get_socket_io_type()) {
                    if (g_selected.object.get_socket()._DataType == this.socket._DataType) {
                        this.context.fillStyle = 'red';
                    } else {
                        if (g_selected.object.get_socket()._DataType == "AnyDataType" || this.socket._DataType == "AnyDataType") {
                            this.context.fillStyle = 'red';
                        } else {
                            this.context.fillStyle = 'lightgrey';
                        }
                    }
                } else {
                    this.context.fillStyle = 'lightgrey';
                }
            } else {
                this.context.fillStyle = 'white';
            }

        }
        this.context.fill();
        this.context.strokeStyle = '#550000';
        this.context.stroke();
        // Draw name of socket

        this.context.fillStyle = 'black';
        // Change text alignment based on socket type
        if (this.sockettype == 'input') {
            this.context.textAlign = 'left';
            this.context.font = 'bold 12pt Calibri';
            var type_x = x + this.offsetx + 8;
            var type_y = y + this.offsety + 5 + this.spacing * (num-1)
            this.draw_type(type_x, type_y);
            this.context.font = '12pt Calibri';
            this.context.fillStyle = 'black';
            this.context.fillText(this.socket._Name, x + this.offsetx + 20, y + this.offsety + 5 + this.spacing * (num-1));
        } else if (this.sockettype == 'output') {
            this.context.textAlign = 'right';
            var type_x = x + width - this.offsetx - 8;
            var type_y = y + this.offsety + 5 + this.spacing * (num-1)
            this.draw_type(type_x, type_y);
            this.context.font = '12pt Calibri';
            this.context.fillStyle = 'black';
            this.context.fillText(this.socket._Name, x + width - this.offsetx - 20, y + this.offsety + 5 + this.spacing * (num-1));
        }
        this.context.stroke();
    }

    draw_type(type_x, type_y) {
        this.context.font = 'bold 12pt Calibri';
        switch (this.socket._DataType) {
            case "AnyDataType":
                this.context.fillStyle = 'blue';
                this.context.fillText("A", type_x, type_y);
                break;
            case "String":
                this.context.fillStyle = 'red';
                this.context.fillText("S", type_x, type_y);
                break;
            case "UnsupportedDataType":
                this.context.fillStyle = 'white';
                this.context.fillText("U", type_x, type_y);
                break;
            case "Integer":
                this.context.fillStyle = 'green';
                this.context.fillText("I", type_x, type_y);
                break;
            case "Float":
                this.context.fillStyle = 'green';
                this.context.fillText("F", type_x, type_y);
                break;
            case "Image":
                this.context.fillStyle = 'yellow';
                this.context.fillText("I", type_x, type_y);
                break;
            case "Video":
                this.context.fillStyle = 'yellow';
                this.context.fillText("V", type_x, type_y);
                break;
            case "Text":
                this.context.fillStyle = 'red';
                this.context.fillText("T", type_x, type_y);
                break;
            default:
        }
    }

    // Check if xy is inside this node
    check_inside(x, y) {
    var minx = parseInt(this.get_x()) - this.size;
    var maxx = parseInt(this.get_x()) + parseInt(this.width) - this.size;
    var miny = parseInt(this.get_y() - this.size);
    var maxy = parseInt(this.get_y()) + parseInt(this.height) - this.size;
    var posx = parseInt(x) - g_drawalgo.get_offsetx();;
    var posy = parseInt(y) - g_drawalgo.get_offsety();;
    if (posx > minx && posx < maxx && posy > miny && posy < maxy) {
        return this;
    }
        return false;
    }

    set_selected(state) {
        this.selected = state;
    }

    get_socket() {
        return this.socket;
    }

}


class DrawLink extends DrawableObject {

    constructor(context, link) {
        super(context);
        this.link = link;
        this.x1 = 0;
        this.y1 = 0;
        this.x2 = 0;
        this.y2 = 0;
    }

    draw() {
        // Find line start & end
        this.update_start_end();
        var x1 = this.x1;
        var y1 = this.y1;
        var x2 = this.x2;
        var y2 = this.y2;

        // Draw link
        this.context.beginPath();
        this.context.moveTo(x1, y1);
        this.context.lineTo(x2, y2);
        this.context.lineWidth = 2;
        if (this.selected) {
            this.context.strokeStyle="red";
        } else {
            this.context.strokeStyle="black";
        }
        this.context.shadowBlur=10;
        if (this.selected) {
            this.context.shadowColor="red";
        } else {
            this.context.shadowColor="black";
        }
        this.context.stroke();
    }

    //function converted from here
    //http://ericleong.me/research/circle-line/#static-circle-and-static-line-segment
    closestpointonline(x0, y0) {
        var lx1 = this.x1;
        var ly1 = this.y1;
        var lx2 = this.x2;
        var ly2 = this.y2;
        var A1 = ly2 - ly1;
        var B1 = lx1 - lx2;
        var C1 = (ly2 - ly1)*lx1 + (lx1 - lx2)*ly1;
        var C2 = -B1*x0 + A1*y0;
        var det = A1*A1 - -B1*B1;
        var cx = 0;
        var cy = 0;
        if(det != 0){
            cx = ((A1*C1 - B1*C2)/det);
            cy = ((A1*C2 - -B1*C1)/det);
        }else{
            cx = x0;
            cy = y0;
        }
        var point = [cx, cy];
        return point;
    }

    // Check if xy is on line
    check_inside(x, y) {
        // Get sockets for line start & end
        this.update_start_end();
        var x1 = this.x1;
        var y1 = this.y1;
        var x2 = this.x2;
        var y2 = this.y2;

        // Find min and max x
        var minx = x1 - 5;
        var maxx = x2 + 5;
        if (x1 > x2) {
            minx = x2 - 5;
            maxx = x1 + 5;
        }
        // Find min and max y
        var miny = y1;
        var maxy = y2;
        if (y1 > y2) {
            miny = y2;
            maxy = y1;
        }

        //calculate offset mouse position
        var posx = parseInt(x) - g_drawalgo.get_offsetx();
        var posy = parseInt(y) - g_drawalgo.get_offsety();

        // AABB test
        if (posx < minx || posx > maxx) {
            if (miny > posy || maxy < posy) {
                //position is not within the AABB so fail early
                return false;
            }
        }

        var closestpoint = this.closestpointonline(posx,posy);
        var deltaPoint = [closestpoint[0] - posx, closestpoint[1] - posy];
        //vector magnitude calc
        var deltaPointMagnitude = Math.pow(deltaPoint[0], 2) + Math.pow(deltaPoint[1], 2);
        deltaPointMagnitude = Math.sqrt(deltaPointMagnitude);

        if(Math.abs(deltaPointMagnitude) < 20) {
            return this;
        }
        return false;
    }

    update_start_end() {
        if (this.link._In_Socket != null && this.link._Out_Socket != null) {
            var sock1 = this.link._In_Socket.get_drawable();
            var sock2 = this.link._Out_Socket.get_drawable();
            this.x1 = sock1.get_x();
            this.y1 = sock1.get_y();
            this.x2 = sock2.get_x();
            this.y2 = sock2.get_y();
        } else {
            var obj1 = null;
            if (this.link._In_Socket == null) {
                obj1 = this;
            } else {
                obj1 = this.link._In_Socket.get_drawable();
            }
            var obj2 = null;
            if (this.link._Out_Socket == null) {
                obj2 = this;
            } else {
                obj2 = this.link._Out_Socket.get_drawable();
            }
            this.x1 = obj1.get_x();
            this.y1 = obj1.get_y();
            this.x2 = obj2.get_x();
            this.y2 = obj2.get_y();
        }
    }

    set_link_out_socket(sock) {
        this.link._Out_Socket = sock;
    }

    set_link(link) {
        this.link = link;
    }

    destroy_link() {
        this.link.destroy_link();
    }


}
