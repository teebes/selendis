render_communications = function() {
    $.getJSON("/api/messages.json", function(communications) {    
        var html = '';
        $.each(communications, function() {
            html += "<div class='comm_" + this.type + "'>" + this.source + ": " + this.content + "</div>\n";
        });
        $("#communications").html(html);
        var communications_div = document.getElementById("communications");
        communications_div.scrollTop = communications_div.scrollHeight;

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
                render_communications();
            }
        });
}