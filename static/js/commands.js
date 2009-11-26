/* utility functions */

move_to = function(x, y) {
    // assume the move went through so that directions can be spammed
    document.player.room.xpos = x;
    document.player.room.ypos = y;
    
    $.ajax({
        type: "PUT",
        url: "/api/players/me.json",
        data: { xpos: x, ypos: y },
        dataType: "json",
        success: function(player) {
            document.player = player;
            render_room();
            get_map();
            if (player.builder_mode) {
                render_builder();
            }
            render_profile();
        },
        error: function(resp) {
            
            split_resp = resp.responseText.split(':')
            split_resp.shift(); // this pops for example 'BAD REQUEST'
            var processed_response = split_resp.join(':');
            
            $("#input_feedback").show();
            $("#input_feedback").html(processed_response);            
        }
    });
}

/* bindings & command execution */

setup_commands = function() {
    $("#command_text").focus();
    $("#submit_command").click(function () { process_command($("#command_text").val()); });
    $("#command_text").keypress(function (e) { if (e.which == 13) { process_command($(this).val()) } });
    
    $("#move_north").click(function () { process_command('north'); });
    $("#move_east").click(function () { process_command('east'); });
    $("#move_south").click(function () { process_command('south'); });
    $("#move_west").click(function () { process_command('west'); });
    
}

process_command = function(command){
    var t = command.split(' ');
    $("#input_feedback").html('');
    $("#input_feedback").hide();

    $("#command_text").val('');   

    first = t[0].toLowerCase();

    // directions
    if (first == 'north' || first == 'nort' || first == 'nor' || first == 'no' || first == 'n') {
        move_to(document.player.room.xpos, document.player.room.ypos - 1);
        return
    } else if (first == 'east' || first == 'ea' || first == 'e') {
        move_to(document.player.room.xpos + 1, document.player.room.ypos);
        return
    } else if (first == 'south' || first == 'sout' || first == 'sou' || first == 'so' || first == 's') {        
        move_to(document.player.room.xpos, document.player.room.ypos + 1);
        return
    } else if (first == 'west' || first == 'wes' || first == 'we' || first == 'w') {        
        move_to(document.player.room.xpos - 1, document.player.room.ypos);
        return
    }
    
    // set
    else if (first == 'set') {
        if (document.player.builder_mode && t[1] == 'room' && t[2] && t[3]) {
            var attribute = t[2];
            
            if (attribute == 'xpos' || attribute == 'ypos') {
                $("#input_feedback").show();
                $("#input_feedback").html("Too dangerous!");
            }
            
            t.shift();
            t.shift();
            t.shift();
            
            var data = {};
            data['id'] = document.player.room.id;
            data[attribute] = t;
            modify_room(data);
            return
        }
    }
    
    // chat
    else if (first == 'chat') {
        t.shift();
        if (t != '') {
            send_communication('chat', t.join(' '));
        }
        return
    }
    
    // get / drop
    else if (first == 'get' || first == 'drop') {
        t.shift();
        if (document.player.room) {
            var player_items = document.player.items;
            var room_items = document.player.room.items;
            
            var items = null;
            if (first == 'get') { items = room_items; }
            else if (first == 'drop') { items = player_items; }
            
            $.each(items, function () {
                split_name = this.name.split(' ');
                for (var i = 0 ; i < split_name.length ; i++) {
                    if (t[0] == this.id ||
                        split_name[i] != 'a' &&
                        split_name[i] != 'the' &&
                        split_name[i] == t[0]) {
                        if (first == 'get') {
                            modify_item({id: this.id, owner_type: 'player', owner_id: document.player.id});
                            break;
                        } else if (first == 'drop') {
                            modify_item({id: this.id, owner_type: 'room', owner_id: document.player.room.id});
                            break;
                        }
                    }
                }
            });
        }
        return
    }
    
    else if (first == 'help') {
        $("#input_feedback").show();
        $("#input_feedback").html("Commands: chat north east south west");
        return
    }
    

    $("#input_feedback").show();
    $("#input_feedback").html("Invalid command: '" + command + "'");

    
}