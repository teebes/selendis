create_room = function(x, y) {
    $.ajax({
        type: "POST",
        url: "/api/world/rooms/create/",
        data: { xpos: x, ypos: y }
    /*dataType: "json",
    success: function(room) { }*/
    });
}

modify_room = function(data) {
    $.ajax({
        type: "PUT",
        url: "/api/world/rooms/" + data.id + ".json",
        data: data,
        dataType: "json",
        success: function(room) {
            document.player.room = room;
            render_room();
            get_map();
        }
    });
}

delete_room = function(data) {
    $.ajax({
        type: "DELETE",
        url: "api/world/rooms/" + data.id + ".json",
        dataType: "json"
    });
}