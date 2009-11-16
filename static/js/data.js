/* This library being on its own 'data.js' file no longer
  makes sense. Each area (communications, profile, room)
  needs to know how to interact with its own api.
  
  Remember to move the code accordingly
*/

/* getters */
get_map = function() {
    $.getJSON("api/world/map.json", function(map){
        document.map = map;
    });
}

get_player = function() {
    $.getJSON("/api/players/me.json", function(player) {
        document.player = player;
    });
}

get_communications = function() {
    $.getJSON("/api/messages.json")
}

/* modifiers */

modify_player = function(data) {
    $.ajax({
        type: "PUT",
        url: "/api/players/me.json",
        data: data,
        dataType: "json",
        success: function(player) {
            document.player = player
        }
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

move_to = function(x, y) {
    $.ajax({
        type: "PUT",
        url: "/api/players/me.json",
        data: { xpos: x, ypos: y },
        dataType: "json",
        success: function(player) {
            document.player = player;
            render_room();
            get_map();
        }
    });
}

/* deleters */
delete_room = function(data) {
        $.ajax({
            type: "DELETE",
            url: "api/world/rooms/" + data.id + ".json",
            dataType: "json",
        });
}


