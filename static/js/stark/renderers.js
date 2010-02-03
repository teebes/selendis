render_log = function() {
        
        var previous_html = $("#communications").html();
        
        // see if this user is scrolling or if he's at the bottom
        var scroll_down = false;
        var comm_div = document.getElementById("communications");
        if (comm_div.scrollTop - (comm_div.scrollHeight - comm_div.offsetHeight) > 0) {
            scroll_down = true;
        }
        
        var html = '';
        $.each(stark.log, function() {
            html += '<div class="comm_' + this.type + '">';
            if (this.type == 'chat') {
                html += '<strong>' + this.source + '</strong>: ';
            }
            html += this.content;
            html += '</div>\n';
        });

        if (previous_html != html) {
            $("#communications").html(html);
        }
        
        if (scroll_down) {  comm_div.scrollTop = comm_div.scrollHeight; }


}

render_room = function() {
    if (typeof(stark) == 'undefined') { return; }
    
    var room = stark.room;
    
    $("#room_title").html(room.name);
    
    $("#room_desc").html(room.description);
    
    $("#room_items").empty();
    $.each(room.items, function() {
        var line = $("<div></div>");
        line.append(item_link(this));
        line.append(" is here");

        line.appendTo("#room_items");
    });
    
    var players = ""
    $.each(room.player_related, function() {
        if (this.name != stark.player.name) {
            players += this.name + " is here<br />";
        }
    });
    $("#room_players").html(players);
    
    var mobs = ""
    $.each(room.mob_related, function() {
        mobs += this.name + " is here<br />";
    });
    $("#room_mobs").html(mobs);
    
    if (stark.player && stark.player.builder_mode) {
        render_builder();
    }
    
}

render_player = function() {
    $("#player_name").html(stark.player.name);
    $("#player_level").html(stark.player.level);
    $("#player_experience").html(str_format("{0} / {1}",
                                 stark.player.experience,
                                 stark.player.next_level));

    $("#current_hp").html(stark.player.hp);
    $("#perc_hp").html(Math.round(stark.player.hp / stark.player.max_hp * 100));
    $("#current_mp").html(stark.player.mp);
    $("#perc_mp").html(Math.round(stark.player.mp / stark.player.max_mp * 100));

    // equipment
    $.each(stark.player.equipment, function(key, value) {
        var span_id = "player_" + key;
        if (value) {
            var link = item_link(value);
            link.attr('id', span_id);
            $("#"+span_id).replaceWith(link);
        } else {
            var empty = str_format("<span id='{0}'>&lt;empty&gt;</span>",
                                   span_id);
            $("#"+span_id).replaceWith(empty);
        }
    });

    //inventory
    $("#player_inventory").empty();
    $.each(stark.player.inventory, function() {
        var line = $("<div></div>");
        line.append(item_link(this));

        line.appendTo("#player_inventory");
    });
}

// -- Rooms --

render_builder = function() {
    $("#builder_box").show();
    
    $("#builder_x").html(stark.player.room.xpos);
    $("#builder_y").html(stark.player.room.ypos);
    
    $("#builder_room_name").val(stark.player.room.name);
    $("#builder_room_name").unbind();
    $("#builder_room_name").blur(function() {
        modify_room({name: $(this).val(), id: stark.player.room.id});
    });
    
    $("#builder_room_description").val(stark.player.room.description);
    $("#builder_room_description").unbind();
    $("#builder_room_description").blur(function() {
        modify_room({description: $(this).val(), id: stark.player.room.id});
    });
    
    // connectors
    var dirs = ['north', 'east', 'south', 'west'];
    $.each(dirs, function() {
        var dir = this;
        if (stark.player.room[dir] == 'Normal') {
            $("#builder_"+dir).attr('checked', true);
        } else {
            $("#builder_"+dir).attr('checked', false);
        }

        $("#builder_"+dir).unbind();
        $("#builder_"+dir).click(function() {
            var data = {};
            data[dir] = 'toggle';
            data['id'] = stark.player.room.id;
            //alert(dir);
            modify_room(data);
        });
    });
    
    // room types
    $.each($("#builder_room_type").children(), function() {
        if ($(this).attr('value') == stark.player.room.type) {
            $(this).attr('selected', true);
        }
    });
    
    // jump to
    $("#jump_x").val(stark.player.room.xpos);
    $("#jump_y").val(stark.player.room.ypos);
}
