// imports:
//
// from DOM: document.player
// from room.js: render_room
// from data.js: get_map
// from builder.js: render_builder
// from player.js: render_profile
// from builder.js: modify_room
// from item.js: modify_item
// from communications.js: send_communications

/* utility functions */

feedback = function(msg) {
    $("#input_feedback").show();
    $("#input_feedback").html(msg);    
}

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
            
            feedback(processed_response);
        }
    });
}

move_item = function(container, identifier, owner_type, owner_id) {
    // Moves an item from a container to a new owner, according to a 'keyword'
    // argument which can be an ID, 'all', or a search word

    $.each(container, function(){
        if (identifier == 'all'
            || identifier == this.id
            || identifier in oc(this.name.split(' '))) {
            
            modify_item({id: this.id, owner_type: owner_type, owner_id: owner_id});

            if (identifier != 'all'){ return false; }
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
    var t = tokens = command.split(' '); // t for tokens
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
        tokens.shift();
        if (tokens.length > 0) {
            send_communication('chat', tokens.join(' '));
        } else {
            feedback("Chat syntax: chat msg");
        }
        return
    }
    
    // ----- get -----------------
    else if (tokens[0] == 'get') {
        
        if (tokens.length == 1) {
            feedback("Get syntax: get object [container]");
        }
        
        else if (tokens.length == 2) {
            move_item(document.player.room.items, tokens[1], 'player', document.player.id);
        }

        
        else if (tokens.length == 3) {
            // get in container

            // try the player
            var found = false;
            $.each(document.player.items, function() {
                if (tokens[2] == this.id
                    || tokens[2] in oc(this.name.split(' '))) {
                    if (this.capacity > 0) {
                        move_item(this.contains, tokens[1], 'player', document.player.id);
                        found = true;
                        return false;
                    }
                }
            });
            
            // try the room
            if (!found) { 
                $.each(document.player.room.items, function() {
                    if (tokens[2] == this.id
                        || tokens[2] in oc(this.name.split(' '))) {
                        if (this.capacity > 0) {
                            move_item(this.contains, tokens[1], 'player', document.player.id);
                            return false;
                        }
                    }
                });
            }
        }
        
        return
    }
    
    // ----- put -----------------
    else if (tokens[0] == 'put') {
        // put in container
        if (tokens.length < 3) {
            feedback('Put syntax: put object container')
        } else {
            // try the player
            var found = false;
            $.each(document.player.items, function() {
                if (tokens[2] == this.id
                    || tokens[2] in oc(this.name.split(' '))) {
                    if (this.capacity > 0) {
                        move_item(document.player.items, tokens[1], 'iteminstance', this.id);
                        found = true;
                        return false;
                    }
                }
            });
            
            // try the room
            if (!found) {
                $.each(document.player.room.items, function() {
                    if (tokens[2] == this.id
                        || tokens[2] in oc(this.name.split(' '))) {
                        if (this.capacity > 0) {
                            move_item(document.player.items, tokens[1], 'iteminstance', this.id);
                            return false;
                        }
                    }
                });
            }
        }
        return
        
    }
    
    // ----- drop -----------------
    else if (tokens[0] == 'drop') {
        
        if (tokens.length == 1) {
            feedback("Drop syntax: drop object");
            return
        }
        
        move_item(document.player.items, tokens[1], 'room', document.player.room.id);        
        return
    }
    
    // ----- give --------
    else if (tokens[0] == 'give') {
        if (tokens.length < 3) {
            feedback("Give syntax: give object target");
        } else {
            // find the right player
            var found = false;
            $.each(document.player.room.player_related, function() {
                if (tokens[2] == this.name) {
                    move_item(document.player.items, tokens[1], 'player', this.id);
                    found = true;
                    return false;
                }
            });
            
            // if no player was found, try to find a mob
            if (!found) {
                $.each(document.player.room.mob_related, function() {
                   if (tokens[2] in oc(this.split(' '))) {
                        move_item(document.player.items, tokens[1], 'mob', this.id);
                        found = true;
                        return false;
                   }
                });
            }
            
            if (!found) { feedback('give: invalid item or target'); }
        }
        
        return
    }
    
    // ----- kill -----------------
    else if (tokens[0] == 'kill') {
        if (tokens.length < 2) {
            feedback('Syntax: kill target')
        } else {
            $.each(document.player.room.player_related, function() {
                if (this.name != document.player.name && (this.id == tokens[1] || this.name == tokens[1])) {
                    $.ajax({
                        type: "PUT",
                        url: "/api/players/me.json",
                        data: { target_type: 'player', target_id: this.id },
                        dataType: "json"
                    });
                }
            });
            $.each(document.player.room.mob_related, function() {
                if (this.id == tokens[1] || tokens[1] in oc(this.name.split(' '))) {
                    $.ajax({
                        type: "PUT",
                        url: "/api/players/me.json",
                        data: { target_type: 'mob', target_id: this.id },
                        dataType: "json"
                    });
                }
            });
        }        
        return
    }
    
    // ----- wield -----------------
    else if (tokens[0] == 'wield') {
        if (tokens.length < 2) {
            feedback('Syntax: wield weapon')
        } else {
            $.each(document.player.items, function() {
                if (this.id == tokens[1] || tokens[1] in oc(this.name.split(' '))) {
                    modify_player({main_hand: this.id});
                }
            });
        }
        return
    }
    
    
    else if (first == 'help') {
        feedback("Commands: chat north east south west get put drop kill wield");
        return
    }
    
    feedback("Invalid command: '" + command + "' (try 'help')");
    
}