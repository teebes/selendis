get_communications = function() {
    $.getJSON("/api/messages.json")
}

render_communications = function() {
    $.getJSON("/api/messages.json", function(communications) {
        var previous_html = $("#communications").html()
        
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
        
        if (html.value != previous_html.value) {
            var communications_div = document.getElementById("communications");
            communications_div.scrollTop = communications_div.scrollHeight;
        }

    });
}

send_communication = function(type, content) {
        var data = {}
        data['content'] = content
        data['type'] = type
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