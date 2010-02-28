render_log = function() {
    
    var previous_html = $("#communications").html();
    
    // see if this user is scrolling or if he's at the bottom
    var scroll_down = false;
    var comm_div = document.getElementById("communications");
    if (comm_div.scrollTop - (comm_div.scrollHeight - comm_div.offsetHeight) > 0) {
        scroll_down = true;
    }
    
    var html = '';
    $.each(stark.log, function(i, message) {
        html += '<div class="log_msg comm_' + message.type + '"> * &gt; ';
        html += message.content.replace(/\n/g, "<br />");
        html += '</div>\n';
    });
    
    if (previous_html != html) {
        $("#communications").html(html);
    }
    
    if (scroll_down) {  comm_div.scrollTop = comm_div.scrollHeight; }


}

render_room = function() {
    $("#room_box").attr('style', str_format('width: {0}px', canvas_width));
    
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
    $.each(stark.player.inventory, function(index, value) {
        var line = $("<div></div>");
        line.append(item_link(value));

        line.appendTo("#player_inventory");
    });


}

// -- Rooms --

render_builder = function() {
    $("#builder_box").show();

    $("#builder_room_id").html(stark.room.id);
    $("#builder_x").html(stark.room.xpos);
    $("#builder_y").html(stark.room.ypos);
    
    $("#builder_room_name").val(stark.room.name);
    $("#builder_room_name").unbind();
    $("#builder_room_name").blur(function() {
        modify_room({name: $(this).val(), id: stark.room.id});
    });
    
    $("#builder_room_description").val(stark.room.description);
    $("#builder_room_description").unbind();
    $("#builder_room_description").blur(function() {
        modify_room({description: $(this).val(), id: stark.room.id});
    });
    
    // connectors
    var dirs = ['north', 'east', 'south', 'west'];
    $.each(dirs, function() {
        var dir = this;
        if (stark.room[dir] == 'Normal') {
            $("#builder_"+dir).attr('checked', true);
        } else {
            $("#builder_"+dir).attr('checked', false);
        }

        $("#builder_"+dir).unbind();
        $("#builder_"+dir).click(function() {
            var data = {};
            data[dir] = 'toggle';
            data['id'] = stark.room.id;
            //alert(dir);
            modify_room(data);
        });
    });
    
    // room types
    $.each($("#builder_room_type").children(), function() {
        if ($(this).attr('value') == stark.room.type) {
            $(this).attr('selected', true);
        }
    });
    
    // jump to
    $("#jump_x").val(stark.room.xpos);
    $("#jump_y").val(stark.room.ypos);
}
