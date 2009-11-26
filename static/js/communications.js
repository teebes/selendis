get_communications = function() {
    $.getJSON("/api/messages.json")
}

render_communications = function() {
    $.getJSON("/api/messages.json", function(communications) {
        var previous_html = $("#communications").html();
        
        // see if this user is scrolling or if he's at the bottom
        var scroll_down = false;
        var comm_div = document.getElementById("communications");
        if (comm_div.scrollTop - (comm_div.scrollHeight - comm_div.offsetHeight) > 0) {
            scroll_down = true;
        }
        
        var html = '';
        $.each(communications, function() {
            html += "<div class='comm_" + this.type + "'>";
            if (this.type == 'chat') {
                html += '<strong>' + this.source + "</strong>: ";                
            }
            html += this.content;
            html += "</div>\n";
        });
        $("#communications").html(html);
        
        if (scroll_down) {  comm_div.scrollTop = comm_div.scrollHeight; }

    });
}

send_communication = function(type, content) {
        var data = {};
        data['content'] = content;
        data['type'] = type;
        $.ajax({
            type: "POST",
            url: "/api/messages.json",
            data: data,
            dataType: "json",
            success: function(communication) {
                // for now, we re-render when something is sent
                //render_communications();
            }
        });
}