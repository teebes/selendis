load_map = function() {
    $.getJSON("api/world/map.json", function(data){
        document.map = data;
    });
}

get_player = function() {
    $.getJSON("/api/players/me.json", function(data){
        document.player = data;
        render_room(data.room);
    });
}

render_room = function(room) {
    $("#room_title").html(room.title);
    $("#room_desc").html(room.description);
    
    var players = ""
    $.each(room.player_related, function() {
        players += this.name + " is here<br />";
    })
    $("#room_players").html(players);
    
    var mobs = ""
    $.each(room.mob_related, function() {
        mobs += this.name + " is here<br />";
    });
    $("#room_mobs").html(mobs);
}

process_command = function(command){
    var tokens = command.split(' ');
    var xpos = 0;
    var ypos = 0;
    if (tokens[0] == 'north' || tokens[0] == 'east' || tokens[0] == 'west' || tokens[0] == 'south') {
        if (tokens[0] == 'north') {
            xpos = document.player.room.xpos;
            ypos = document.player.room.ypos - 1;
        } else if (tokens[0] == 'east') {
            xpos = document.player.room.xpos + 1;
            ypos = document.player.room.ypos;
        } else if (tokens[0] == 'west') {
            xpos = document.player.room.xpos - 1;
            ypos = document.player.room.ypos;
        } else if (tokens[0] == 'south') {
            xpos = document.player.room.xpos;
            ypos = document.player.room.ypos + 1;
        }
        $.ajax({
            type: "PUT",
            url: "/api/players/me.json",
            data: { xpos: xpos, ypos: ypos },
            dataType: "json",
            success: function(player) {
                document.player = player;
                render_room(document.player.room);
                load_map();
            }
        });
    }
}

send_command = function(command) {
    $.ajax({
        type: "PUT",
        url: "/api/commands/send.json",
        data: { command: command },
        dataType: "json",
        success: function(data) {
            document.player = data;
        }
    });
}

