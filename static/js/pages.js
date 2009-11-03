render_room = function() {
    var room = document.player.room;
    
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
    
    if (document.player.builder_mode) {
        render_builder()
    }
}


render_profile = function() {
    $("#player_name").html(document.player.name);
}

render_builder = function() {
    $("#builder_box").show();
    
    $("#builder_x").html(document.player.room.xpos);
    $("#builder_y").html(document.player.room.ypos);
    
    $("#builder_room_title").val(document.player.room.title);
    $("#builder_room_title").unbind();
    $("#builder_room_title").blur(function() {
        modify_room({title: $(this).val(), id: document.player.room.id});
    });
    
    $("#builder_room_description").val(document.player.room.description);
    $("#builder_room_description").unbind();
    $("#builder_room_description").blur(function() {
        modify_room({description: $(this).val(), id: document.player.room.id});
    });
    
    // connectors
    var dirs = ['north', 'east', 'south', 'west'];
    $.each(dirs, function() {
        var dir = this;
        if (document.player.room[dir] == 'Normal') {
            $("#builder_"+dir).attr('checked', true);
        } else {
            $("#builder_"+dir).attr('checked', false);
        }

        $("#builder_"+dir).unbind();
        $("#builder_"+dir).click(function() {
            var data = {};
            data[dir] = 'toggle';
            data['id'] = document.player.room.id;
            //alert(dir);
            modify_room(data);
        });
    });
}

setup_builder = function () {
    $("#delete_room").click(function() {
    var confirmation = confirm("Press Ok to delete. You'll need ro manually reload afterwards.");
    if (confirmation) {
        delete_room(document.player.room);
    }
    });
    $("#jump_to").click(function() {
        move_to($("#jump_x").val(), $("#jump_y").val());
    });
    
}