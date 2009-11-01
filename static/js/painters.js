setup_menu = function() {
    $("#room_link").click(function () {
        $("#room_box").show();
        $("#profile_box").hide();
    });
    $("#profile_link").click(function() {
        $("#profile_box").show();
        $("#room_box").hide();
    })
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