load_map = function() {
    $.getJSON("api/world/map.json", function(data){
        document.map = data;
    });
}

get_player = function() {
    $.getJSON("/api/players/me.json", function(data){
        document.player = data;
        $("#profile_link").text(data.name);
        render_room(data.room);
        render_profile(document.player);
    });
}

render_room = function(room) {
    $("#room_title").html(room.title);
    if (document.player && document.player.builder_mode) {
        $("#room_title").click(function() {
            if (document.player && document.player.level > 99) {
                $("#room_title").hide();
                $("#room_title_edit").show();
                $("#room_title_edit").val($("#room_title").text());
                $("#room_title_edit").focus();
            }
        });
        $("#room_title_edit").blur(function() {
            modify_room({title: $(this).val(), id: document.player.room.id});
            $("#room_title_edit").hide();
            $("#room_title").show();
            $("#command_text").focus();
        });
    }    
    
    
    /*
     maybd add if > 99:
      + " (" + room.xpos + "), (" + room.ypos + ")"
    */
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

render_profile = function(player) {
    if (document.player.level > 99) {
        $("#profile_builder").show();
        if (document.player.builder_mode) {
            $("#builder_checkbox").attr('checked', true);
        }
        $("#builder_checkbox").click(function(){
            modify_player({builder_mode: $(this).attr('checked')});
        });        
    } else {
        $("#profile_builder").hide();
    }
}

modify_player = function(data) {
    $.ajax({
        type: "PUT",
        url: "/api/players/me.json",
        data: data,
        dataType: "json",
        success: function(player) {
            get_player();
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
            render_room(room);
            //alert('back');
            //get_player();
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
            render_room(document.player.room);
            load_map();
        }
    });
}

process_command = function(command){
    var t = command.split(' ');
    $("#input_feedback").html('');
    $("#input_feedback").hide();

    if (t[0] == 'north' || t[0] == 'nort' || t[0] == 'nor' || t[0] == 'no' || t[0] == 'n') {
        move_to(document.player.room.xpos, document.player.room.ypos - 1);
    } else if (t[0] == 'east' || t[0] == 'ea' || t[0] == 'e') {
        move_to(document.player.room.xpos + 1, document.player.room.ypos);
    } else if (t[0] == 'south' || t[0] == 'sout' || t[0] == 'sou' || t[0] == 'so' || t[0] == 's') {        
        move_to(document.player.room.xpos, document.player.room.ypos + 1);
    } else if (t[0] == 'west' || t[0] == 'wes' || t[0] == 'we' || t[0] == 'w') {        
        move_to(document.player.room.xpos - 1, document.player.room.ypos);
    } else {
        $("#input_feedback").show();
        $("#input_feedback").html("Invalid command: '" + command + "'");
    }
    
    $("#command_text").val('');
    
}

