render_room = function() {
    room = document.player.room;
    
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
    $("#builder_room_title").val(document.player.room.title);
    $("#builder_room_title").blur(function() {
        modify_room({title: $(this).val(), id: document.player.room.id});
    });
    
    $("#builder_room_description").val(document.player.room.description);
    $("#builder_room_description").blur(function() {
        modify_room({description: $(this).val(), id: document.player.room.id});
    });

    alert(document.player.room.getAttribute('title'));
    
    var directions = ['north', 'east', 'south', 'west'];
    $.each(directions, function() {
        $("#builder_room_" + this).attr('checked', true);
    });
}