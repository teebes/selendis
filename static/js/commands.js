/* Imports:
  from DOM: document.player
  from room.js: render_room
  from data.js: get_map
  from builder.js: render_builder
  from player.js: render_profile
  from builder.js: modify_room
  from item.js: modify_item
  from communications.js: send_communications
*/

/* utility functions */

feedback = function(msg) {
    $("#input_feedback").show();
    $("#input_feedback").html(msg);    
}

var commands = {
    help: 0,
    north: 0,
    east: 0,
    south: 0,
    west: 0,
    chat: 0,
    get: 0,
    drop: 0,
    put: 0,
    kill: 0,
    wield: 0,
    wear: 0,
    remove: 0
}

match_command = function(user_input) {
    /*
     Takes in a command and matches it against the list of possible commands,
     returning the canonical command name for further processing.
     Starts with each command, and takes one letter off the right until
     there is a match or no more letters.
     
     For example, the candidates for "north" are:
     'north', 'nort', 'nor', 'no', and 'n'
    */

    for (command in commands) {
        var cmd_tokens = command.split('');
        for (var i = 0 ; i < cmd_tokens.length ; i++) {
            var candidate = cmd_tokens.slice(0, cmd_tokens.length - i).join('');
            if (user_input.toLowerCase() == candidate) {
                return command;
            }
        }
    }
    return false;
}

move_to = function(x, y) {
    
    // if the player has enough moves,
    // assume the move went through so that directions can be spammed
    if (document.player.mp > 2) {   
        document.player.room.xpos = x;
        document.player.room.ypos = y;
    }
    
    $.ajax({
        type: "PUT",
        url: "/api/me.json",
        data: { xpos: x, ypos: y },
        dataType: "json",
        success: function(player) {
            document.player = player;
            render_room();

            if (player.builder_mode) {
                render_builder();
            }
            render_profile();
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

    first = match_command(tokens[0]);

    // directions
    if (first == 'north') {
        move_to(document.player.room.xpos, document.player.room.ypos - 1);
        return
    } else if (first == 'east') {
        move_to(document.player.room.xpos + 1, document.player.room.ypos);
        return
    } else if (first == 'south') {
        move_to(document.player.room.xpos, document.player.room.ypos + 1);
        return
    } else if (first == 'west') {
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
    else if (first == 'get') {
        
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
    else if (first == 'put') {
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
    else if (first == 'drop') {
        
        if (tokens.length == 1) {
            feedback("Drop syntax: drop object");
            return
        }
        
        move_item(document.player.items, tokens[1], 'room', document.player.room.id);        
        return
    }
    
    // ----- give --------
    else if (first == 'give') {
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
    else if (first == 'kill') {
        if (tokens.length < 2) {
            feedback('Syntax: kill target')
        } else {
            $.each(document.player.room.player_related, function() {
                if (this.name != document.player.name && (this.id == tokens[1] || this.name == tokens[1])) {
                    $.ajax({
                        type: "PUT",
                        url: "/api/me.json",
                        data: { target_type: 'player', target_id: this.id },
                        dataType: "json"
                    });
                }
            });
            $.each(document.player.room.mob_related, function() {
                if (this.id == tokens[1] || tokens[1] in oc(this.name.split(' '))) {
                    $.ajax({
                        type: "PUT",
                        url: "/api/me.json",
                        data: { target_type: 'mob', target_id: this.id },
                        dataType: "json"
                    });
                }
            });
        }        
        return
    }
    
    // ----- wield -----------------
    /*
    else if (first == 'wield') {
        if (tokens.length < 2) {
            feedback('Syntax: wield weapon');
        } else {
            $.each(document.player.items, function() {
                if (this.id == tokens[1] || tokens[1] in oc(this.name.split(' '))) {
                    modify_player({main_hand: this.id});
                }
            });
        }
        return
    }
    */
    
    else if (first == 'wear' || first == 'wield') {
        if (tokens.length < 2) {
            feedback('Syntax: wear item');
        } else {
            $.each(document.player.items, function() {
                if (this.id == tokens[1] || tokens[1] in oc(this.name.split(' '))) {
                    modify_player({wear: this.id});
                }
            });
        }
        return
    }
    
    else if (first == 'remove') {
        if (tokens.length < 2) {
            feedback('Syntax: remove item');
        } else {
            //var equipment = new Array();
            //if (document.player.main_hand) { equipment.push(document.player.main_hand); }
            var equipment = document.player.equipment;
            $.each(equipment, function() {
                if (this.id == tokens[1] || tokens[1] in oc(this.name.split(' '))) {
                    //modify_player({main_hand: ''});
                    modify_player({remove: this.id});
                    //alert("Want to send " + this.name);
                }
            });
        }
        return
    }
    
    else if (first == 'help') {
        var help = "Commands: north east south west <br />";
        help += "chat get drop put kill wield wear remove";
        feedback(help);
        return
    }
    
    feedback("Invalid command: '" + command + "' (try 'help')");
    
}